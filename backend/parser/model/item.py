from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NotaModel:
    empresa: str
    chave: str
    numero: str
    serie: str
    emissao: str

    items: list["ItemModel"] = field(default_factory=list)

    def add_item(self, item: "ItemModel"):
        self.items.append(item)
        item.nota = self


@dataclass
class ItemModel:
    item_codigo: str
    item_descricao: str
    item_quantidade: str
    item_tipo_unidade: str
    item_valor_unidade: str
    item_valor_total: str
    
    nota: Optional[NotaModel] = None
