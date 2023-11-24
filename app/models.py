from pydantic import BaseModel, AwareDatetime


class Producto(BaseModel):
    name: str
    price: int
    desc: str
    stock: int
    category_id: int
    estado: str = "disponible"


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


class Client(BaseModel):
    name: str
    email: str
    telefono: str
    direccion: str


class ClientUser(BaseModel):
    name: str
    email: str
    user: str
    password: str
    telefono: str
    direccion: str

class ClientLogin(BaseModel):
    user: str
    password: str


class ImagenProductoCreate(BaseModel):
    producto_id: int
    is_principal_image: bool = False


class Oferta(BaseModel):
    producto_id: int
    discount: int
    date_start: AwareDatetime
    date_end: AwareDatetime


class Review(BaseModel):
    producto_id: int
    cliente_id: int
    puntuacion: int
    review: str

class Purchase(BaseModel):
    id_compra: int
    producto_id: int
    nombre_producto: str
    precio_unitario: int
    cantidad_comprada: int
    total_producto: int
