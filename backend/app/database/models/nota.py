from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.parser.model.item import NotaModel, ItemModel


class NotaORM(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String)
    chave = Column(String, unique=True, index=True)
    numero = Column(String)
    serie = Column(String)
    emissao = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with ItemORM
    items = relationship("ItemORM", back_populates="nota", cascade="all, delete-orphan")

    @classmethod
    def from_model(cls, model: NotaModel) -> "NotaORM":
        """Convert from domain model to ORM model"""
        return cls(
            empresa=model.empresa,
            chave=model.chave,
            numero=model.numero,
            serie=model.serie,
            emissao=datetime.fromisoformat(model.emissao),
        )

    def to_model(self) -> NotaModel:
        """Convert from ORM model to domain model"""
        nota = NotaModel(
            empresa=self.empresa,
            chave=self.chave,
            numero=self.numero,
            serie=self.serie,
            emissao=self.emissao.isoformat()
        )
        for item in self.items:
            nota.add_item(item.to_model())
        return nota


class ItemORM(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_codigo = Column(String)
    item_descricao = Column(String)
    item_quantidade = Column(Numeric(10, 2))
    item_tipo_unidade = Column(String)
    item_valor_unidade = Column(Numeric(10, 2))
    item_valor_total = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key to NotaORM
    nota_id = Column(Integer, ForeignKey("notas.id"))
    nota = relationship("NotaORM", back_populates="items")

    @classmethod
    def from_model(cls, model: ItemModel) -> "ItemORM":
        """Convert from domain model to ORM model"""
        return cls(
            item_codigo=model.item_codigo,
            item_descricao=model.item_descricao,
            item_quantidade=float(model.item_quantidade),
            item_tipo_unidade=model.item_tipo_unidade,
            item_valor_unidade=float(model.item_valor_unidade),
            item_valor_total=float(model.item_valor_total)
        )

    def to_model(self) -> ItemModel:
        """Convert from ORM model to domain model"""
        return ItemModel(
            item_codigo=self.item_codigo,
            item_descricao=self.item_descricao,
            item_quantidade=str(self.item_quantidade),
            item_tipo_unidade=self.item_tipo_unidade,
            item_valor_unidade=str(self.item_valor_unidade),
            item_valor_total=str(self.item_valor_total)
        )
