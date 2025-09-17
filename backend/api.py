from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from database.operations import get_nota_by_id, get_all_notas
from database.models.nota import NotaORM, ItemORM
from database.mappers import NotaMapper, ItemMapper
from api.schemas import NotaResponse, ItemResponse

app = FastAPI(title="Notas API")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Criar as tabelas se não existirem
Base.metadata.create_all(bind=engine)


@app.get("/notas", response_model=List[NotaResponse])
async def list_notas(db: Session = Depends(get_db)):
    """
    Lista todas as notas fiscais cadastradas no banco de dados.
    """
    notas_orm = db.query(NotaORM).all()
    return notas_orm


@app.get("/items", response_model=List[ItemResponse])
async def list_items(
    db: Session = Depends(get_db),
    nota_id: int = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Lista os itens cadastrados no banco de dados.
    
    Parâmetros:
    - nota_id: Filtra itens por nota fiscal (opcional)
    - skip: Número de registros para pular (paginação)
    - limit: Número máximo de registros para retornar
    """
    query = db.query(ItemORM)
    
    # Filtrar por nota se especificado
    if nota_id is not None:
        query = query.filter(ItemORM.nota_id == nota_id)
    
    # Aplicar paginação
    items = query.offset(skip).limit(limit).all()
    return items


@app.get("/items/search", response_model=List[ItemResponse])
async def search_items(
    q: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Pesquisa itens por descrição ou código.
    
    Parâmetros:
    - q: Termo de busca (descrição ou código do item)
    - skip: Número de registros para pular (paginação)
    - limit: Número máximo de registros para retornar
    """
    query = db.query(ItemORM).filter(
        (ItemORM.item_descricao.ilike(f"%{q}%")) |
        (ItemORM.item_codigo.ilike(f"%{q}%"))
    )
    
    # Aplicar paginação
    items = query.offset(skip).limit(limit).all()
    return items


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Recupera um item específico pelo ID.
    """
    item = db.query(ItemORM).filter(ItemORM.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@app.get("/notas/{nota_id}", response_model=NotaResponse)
async def get_nota(nota_id: int, db: Session = Depends(get_db)):
    """
    Recupera uma nota fiscal específica pelo ID.
    """
    from sqlalchemy.orm import joinedload
    nota = db.query(NotaORM).options(joinedload(NotaORM.items)).filter(NotaORM.id == nota_id).first()
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return nota

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
