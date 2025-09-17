from typing import Optional, List
from database import SessionLocal
from database.mappers import NotaMapper, ItemMapper
from database.models.nota import NotaORM
from parser.model.item import NotaModel


def save_nota_to_db(nota_model: NotaModel) -> NotaModel:
    """
    Salva uma nota fiscal e seus itens no banco de dados.
    
    Args:
        nota_model: Objeto do modelo de domínio (parser.model.item.Nota)
    
    Returns:
        NotaModel: Objeto do modelo de domínio atualizado com o ID
    """
    db = SessionLocal()
    try:
        # Converter nota para modelo ORM usando o mapper
        nota_orm = NotaMapper.to_orm(nota_model)
        
        # Adicionar itens usando o mapper
        for item_model in nota_model.items:
            item_orm = ItemMapper.to_orm(item_model)
            nota_orm.items.append(item_orm)
        
        # Salvar no banco
        db.add(nota_orm)
        db.commit()
        
        # Atualizar objeto com ID gerado
        db.refresh(nota_orm)
        
        # Retornar o modelo de domínio atualizado
        return get_nota_by_id(nota_orm.id)
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_nota_by_id(nota_id: int) -> Optional[NotaModel]:
    """
    Recupera uma nota fiscal do banco de dados pelo ID.
    
    Args:
        nota_id: ID da nota fiscal
    
    Returns:
        Optional[NotaModel]: Objeto do modelo de domínio ou None se não encontrado
    """
    db = SessionLocal()
    try:
        from sqlalchemy.orm import joinedload
        nota_orm = db.query(NotaORM).options(joinedload(NotaORM.items)).filter(NotaORM.id == nota_id).first()
        if nota_orm is None:
            return None
        # Converter para modelo de domínio enquanto a sessão está ativa
        nota_model = NotaMapper.to_model(nota_orm)
        return nota_model
    finally:
        db.close()


def get_all_notas() -> List[NotaModel]:
    """
    Recupera todas as notas fiscais do banco de dados.
    
    Returns:
        List[NotaModel]: Lista de objetos do modelo de domínio
    """
    db = SessionLocal()
    try:
        notas_orm = db.query(NotaORM).all()
        return [NotaMapper.to_model(nota_orm) for nota_orm in notas_orm]
    finally:
        db.close()