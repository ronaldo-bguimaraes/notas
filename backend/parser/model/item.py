from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Nota:
    empresa: str
    chave: str
    numero: str
    serie: str
    emissao: str

    items: list["Item"] = field(default_factory=list)

    def add_item(self, item: "Item"):
        self.items.append(item)
        item.nota = self


@dataclass
class Item:
    item_codigo: str
    item_descricao: str
    item_quantidade: str
    item_tipo_unidade: str
    item_valor_unidade: str
    item_valor_total: str
    
    nota: Optional[Nota] = None
