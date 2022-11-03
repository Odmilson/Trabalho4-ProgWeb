
from sqlalchemy.orm import Session
from sqlalchemy import and_
from exceptions import UsuarioAlreadyExistError, UsuarioNotFoundError, VendaNotFoundError, DrogaNotFoundError, ItemVendaAlreadyExistError, ItemVendaNotFoundError
import models, schemas

# usuário

def check_usuario(db: Session, usuario: schemas.UsuarioLoginSchema):
    db_usuario = db.query(models.Usuario).filter(and_(models.Usuario.email == usuario.email, models.Usuario.senha == usuario.senha)).first()
    if db_usuario is None:
        return False
    return True

def get_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).get(usuario_id)
    if db_usuario is None:
        raise UsuarioNotFoundError
    return db_usuario

def get_all_usuarios(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).offset(offset).limit(limit).all()

def get_usuario_by_email(db: Session, usuario_email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == usuario_email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_email(db, usuario.email)
    if db_usuario is not None:
        raise UsuarioAlreadyExistError
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db_usuario.nome = usuario.nome
    db_usuario.email = usuario.email
    if usuario.senha is not "":
        db_usuario.senha = usuario.senha
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db.delete(db_usuario)
    db.commit()
    return

# livro

def get_droga_by_id(db: Session, droga_id: int):
    db_droga = db.query(models.Droga).get(droga_id)
    if db_droga is None:
        raise DrogaNotFoundError
    return db_droga

def get_all_drogas(db: Session, offset: int, limit: int):
    return db.query(models.Droga).offset(offset).limit(limit).all()

def create_droga(db: Session, droga: schemas.DrogaCreate):
    db_droga = models.Droga(**droga.dict())
    db.add(db_droga)
    db.commit()
    db.refresh(db_droga)
    return db_droga

def update_droga(db: Session, droga_id: int, droga: schemas.DrogaCreate):
    db_droga = get_droga_by_id(db, droga_id)
    db_droga.nome = droga.nome
    db_droga.descricao = droga.descricao
    db.commit()
    db.refresh(db_droga)
    return db_droga

def delete_droga_by_id(db: Session, droga_id: int):
    db_droga = get_droga_by_id(db, droga_id)
    db.delete(db_droga)
    db.commit()
    return

# empréstimo

def create_venda(db: Session, venda: schemas.VendaCreate):
    get_usuario_by_id(db, venda.id_cliente)
    get_usuario_by_id(db, venda.id_funcionario)
    db_venda = models.Venda(**venda.dict())
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda

def get_venda_by_id(db: Session, venda_id: int):
    db_venda = db.query(models.Venda).get(venda_id)
    if db_venda is None:
        raise VendaNotFoundError
    return db_venda

def get_all_vendas(db: Session, offset: int, limit: int):
    return db.query(models.Venda).offset(offset).limit(limit).all()

# item empréstimo

def create_item_venda(db: Session, item_venda: schemas.ItemVendaCreate):
    get_venda_by_id(db, item_venda.id_venda)
    get_droga_by_id(db, item_venda.id_droga)

    db_item_venda = get_item_venda_by_ids_create(db, item_venda.id_venda, item_venda.id_droga)
    if db_item_venda is not None:
        raise ItemVendaAlreadyExistError

    db_item_venda = models.ItemVenda(**item_venda.dict())
    db.add(db_item_venda)
    db.commit()
    db.refresh(db_item_venda)
    return db_item_venda

def delete_item_venda_by_id(db: Session, id_venda: int, id_droga: int):
    db_item_venda = get_item_venda_by_ids(db, id_venda, id_droga)
    db.delete(db_item_venda)
    db.commit()
    return

def get_item_venda_by_ids_create(db: Session, id_venda: int, id_droga: int):
    return db.query(models.ItemVenda).filter(and_(models.ItemVenda.id_venda == id_venda, models.ItemVenda.id_droga == id_droga)).first()

def get_item_venda_by_ids(db: Session, id_venda: int, id_droga: int):
    db_item_venda = db.query(models.ItemVenda).filter(and_(models.ItemVenda.id_venda == id_venda, models.ItemVenda.id_droga == id_droga)).first()
    if db_item_venda is None:
        raise ItemVendaNotFoundError
    return db_item_venda