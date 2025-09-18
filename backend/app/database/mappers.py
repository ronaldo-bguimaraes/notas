from pydantic import BaseModel
from datetime import datetime
from app.parser.model.item import NotaModel, ItemModel
from app.database.models.nota import NotaORM, ItemORM


class NotaMapper(BaseModel):
    @staticmethod
    def to_orm(model: NotaModel) -> NotaORM:
        return NotaORM(
            empresa=model.empresa,
            chave=model.chave.replace(" ", ""),
            numero=model.numero,
            serie=model.serie,
            emissao=datetime.strptime(model.emissao, "%d/%m/%Y %H:%M:%S")
        )
    
    @staticmethod
    def to_model(orm: NotaORM) -> NotaModel:
        nota = NotaModel(
            empresa=orm.empresa,
            chave=orm.chave,
            numero=orm.numero,
            serie=orm.serie,
            emissao=orm.emissao.strftime("%d/%m/%Y %H:%M:%S")
        )
        for item_orm in orm.items:
            nota.add_item(ItemMapper.to_model(item_orm))
        return nota


class ItemMapper(BaseModel):
    @staticmethod
    def to_orm(model: ItemModel) -> ItemORM:
        return ItemORM(
            item_codigo=model.item_codigo,
            item_descricao=model.item_descricao,
            item_quantidade=float(model.item_quantidade.replace(",", ".")),
            item_tipo_unidade=model.item_tipo_unidade,
            item_valor_unidade=float(model.item_valor_unidade.replace(",", ".")),
            item_valor_total=float(model.item_valor_total.replace(",", "."))
        )
    
    @staticmethod
    def to_model(orm: ItemORM) -> ItemModel:
        return ItemModel(
            item_codigo=orm.item_codigo,
            item_descricao=orm.item_descricao,
            item_quantidade=str(orm.item_quantidade),
            item_tipo_unidade=orm.item_tipo_unidade,
            item_valor_unidade=str(orm.item_valor_unidade),
            item_valor_total=str(orm.item_valor_total)
        )