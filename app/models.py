from pydantic import BaseModel, AwareDatetime


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


class Cliente(BaseModel):
    name: str
    email: str
    password: str
    telefono: str
    direccion: str


class ClientLogin(BaseModel):
    email: str
    password: str


class ImagenProductoCreate(BaseModel):
    producto_id: int
    is_principal_image: bool = False


class Oferta(BaseModel):
    producto_id: int
    discount: int
    date_start: AwareDatetime
    date_end: AwareDatetime
