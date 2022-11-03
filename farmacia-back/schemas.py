from datetime import date
from typing import List
from pydantic import BaseModel

class DrogaBase(BaseModel):
    titulo: str
    resumo: str
class DrogaCreate(DrogaBase):
    pass
class Droga(DrogaBase):
    id: int
    class Config:
        orm_mode = True

class PaginatedDroga(BaseModel):
    limit: int
    offset: int
    data: List[Droga]

class ItemVendaBase(BaseModel):
    id_droga: str
    id_venda: str
class ItemVendaCreate(ItemVendaBase):
    pass
class ItemVenda(ItemVendaBase):
    pass
    class Config:
        orm_mode = True

class VendaBase(BaseModel):
    id_cliente: int
    id_funcionario: int
    data_venda: date
class VendaCreate(VendaBase):
    pass
class Venda(VendaBase):
    id: int
    itens_venda: List[ItemVenda] = []
    class Config:
        orm_mode = True

class PaginatedVenda(BaseModel):
    limit: int
    offset: int
    data: List[Venda]

class UsuarioBase(BaseModel):
    nome: str
    email: str
    cargo: str
class UsuarioCreate(UsuarioBase):
    senha: str
class Usuario(UsuarioBase):
    id: int
    vendas: List[Venda] = []
    class Config:
        orm_mode = True
class UsuarioLoginSchema(BaseModel):
    email: str
    senha: str
    class Config:
        schema_extra = {
            "example": {
                "email": "x@x.com",
                "senha": "pass"
            }
        }

class PaginatedUsuario(BaseModel):
    limit: int
    offset: int
    data: List[Usuario]
