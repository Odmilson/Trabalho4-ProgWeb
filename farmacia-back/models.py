from sqlalchemy import SmallInteger, Date, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    senha = Column(String(255))
    cargo = Column(String(11))
    vendas = relationship("Venda", back_populates="usuario")

class Venda(Base):
    __tablename__ = 'vendas'
    
    id = Column(Integer, primary_key=True, index=True)
    data_venda = Column(Date)
    id_cliente = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_funcionario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="vendas")
    itens_venda = relationship("ItemEmprestimo", back_populates="venda")

class Droga(Base):
    __tablename__ = 'drogas'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    descricao = Column(String(1000))
    itens_venda = relationship("ItemVenda", back_populates="droga")

class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id_droga = Column(Integer, ForeignKey('drogas.id'), primary_key=True, nullable=False)
    id_venda = Column(Integer, ForeignKey('vendas.id'), primary_key=True, nullable=False)
    droga = relationship("Droga", back_populates="itens_venda")
    venda = relationship("Vendas", back_populates="itens_venda")
