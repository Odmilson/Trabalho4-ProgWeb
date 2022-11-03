from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from exceptions import UsuarioException, VendaException, DrogaException, ItemVendaException
from database import get_db, engine
import crud, models, schemas
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# login
@app.post("/api/signup", tags=["usuario"])
async def create_usuario_signup(usuario: schemas.UsuarioCreate = Body(...), db: Session = Depends(get_db)):
    try:
        crud.create_usuario(db, usuario)
        return signJWT(usuario.email)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.post("/api/login", tags=["usuario"])
async def user_login(usuario: schemas.UsuarioLoginSchema = Body(...), db: Session = Depends(get_db)):
    if crud.check_usuario(db, usuario):
        return signJWT(usuario.email)
    raise HTTPException(status_code=400, detail="USUARIO_INCORRETO")

# usuário

@app.get("/api/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())])
def get_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/usuarios", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedUsuario)
def get_all_usuarios(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_usuarios = crud.get_all_usuarios(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_usuarios}
    return response

@app.post("/api/usuarios", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_usuario(db, usuario_id, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())])
def delete_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

# droga

@app.get("/api/droga/{droga_id}", dependencies=[Depends(JWTBearer())])
def get_droga_by_id(droga_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_droga_by_id(db, droga_id)
    except DrogaException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/droga", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedDroga)
def get_all_drogas(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_drogas = crud.get_all_drogas(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_drogas}
    return response

@app.post("/api/drogas", dependencies=[Depends(JWTBearer())], response_model=schemas.Droga)
def create_droga(droga: schemas.DrogaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_droga(db, droga)
    except DrogaException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/drogas/{droga_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Droga)
def update_droga(droga_id: int, droga: schemas.DrogaCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_droga(db, droga_id, droga)
    except DrogaException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/drogas/{droga_id}", dependencies=[Depends(JWTBearer())])
def delete_droga_by_id(droga_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_droga_by_id(db, droga_id)
    except DrogaException as cie:
        raise HTTPException(**cie.__dict__)


# venda

@app.post("/api/venda", dependencies=[Depends(JWTBearer())], response_model=schemas.Venda)
def create_venda(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_venda(db, venda)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/vendas/{venda_id}", dependencies=[Depends(JWTBearer())])
def get_venda_by_id(venda_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_venda_by_id(db, venda_id)
    except VendaException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/vendas", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedVenda)
def get_all_vendas(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_vendas = crud.get_all_vendas(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_vendas}
    return response

# item venda

@app.post("/api/itens-venda", dependencies=[Depends(JWTBearer())], response_model=schemas.ItemVenda)
def create_item_venda(item_venda: schemas.ItemVendaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_item_venda(db, item_venda)
    except DrogaException as cie:
        raise HTTPException(**cie.__dict__)
    except VendaException as cie:
        raise HTTPException(**cie.__dict__)
    except ItemVendaException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/itens-venda/{venda_id}/{droga_id}", dependencies=[Depends(JWTBearer())])
def delete_item_venda_by_id(venda_id: int, droga_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_item_venda_by_id(db, venda_id, droga_id)
    except ItemVendaException as cie:
        raise HTTPException(**cie.__dict__)
