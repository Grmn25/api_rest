import datetime
from pydantic import BaseModel, AwareDatetime
from fastapi import File, UploadFile

class Producto(BaseModel):
    name: str
    price: int
    desc: str
    stock: int
    category_id: int


class Categoria(BaseModel):
    category: str

class Usuario(BaseModel):
    name: str
    user: str
    email: str
    password: str

class Login(BaseModel):
    user: str
    password: str

class ImagenProductoCreate(BaseModel):
    producto_id: int
    imagen: UploadFile
    is_principal_image: bool = False

class Oferta(BaseModel):
    producto_id: int
    discount : int
    date_start: AwareDatetime
    date_end: AwareDatetime
