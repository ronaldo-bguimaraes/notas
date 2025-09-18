from pydantic import BaseModel
from datetime import datetime
from typing import List


class ItemResponse(BaseModel):
    id: int
    item_codigo: str
    item_descricao: str
    item_quantidade: float
    item_tipo_unidade: str
    item_valor_unidade: float
    item_valor_total: float
    nota_id: int

    class Config:
        from_attributes = True


class NotaResponse(BaseModel):
    id: int
    empresa: str
    chave: str
    numero: str
    serie: str
    emissao: datetime
    items: List[ItemResponse]

    class Config:
        from_attributes = True
