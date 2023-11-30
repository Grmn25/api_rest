from fastapi import APIRouter, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Client, ClientLogin, ClientUser
from app.database import database
import jwt
from app.config import SECRET_KEY


router = APIRouter()


@router.get("/clients/", tags=['clients'])
async def get_users():
    try:
        query = "SELECT cliente_id, nombre, email, telefono, direccion, fecha_registro FROM cliente"
        result = await database.fetch_all(query)
        return {"clients": result}

    except Exception as e:
        return {"error": str(e)}


@router.post("/clients/user", tags=['clients'])
async def create_user(client: ClientUser):
    try:
        first_query = "SELECT cliente_id FROM cliente WHERE email= :email"
        first_value = {"email": client.email}
        client_exist = await database.fetch_one(first_query, first_value)
        if client_exist:
            raise HTTPException(
                status_code=500, detail="Error al crear el usuario, email ya registrado")

        query = """
            INSERT INTO cliente (nombre, email, telefono, direccion, tiene_usuario)
            VALUES (:name, :email, :telefono, :direccion, true)
            RETURNING cliente_id, nombre, email, fecha_registro
        """
        values = {
            "name": client.name,
            "email": client.email,
            "telefono": client.telefono,
            "direccion": client.direccion
        }
        created_client = await database.fetch_one(query=query, values=values)

        if created_client:
            cliente_id = created_client[0]
            nombre = created_client[1]

            create_user = """
                INSERT INTO cliente_usuario (cliente_id, nombre_usuario, password_usuario) 
                VALUES (:client_id, :user, :password)
                RETURNING cliente_id, nombre_usuario
            """
            values_user = {
                "client_id": cliente_id,
                "user": client.user,
                "password": generate_password_hash(client.password)
            }
            created_user = await database.execute(query=create_user, values=values_user)
            payload = {"sub": cliente_id, 'user': client.user, 'name': nombre}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return {"token": token}
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear el usuario")

    except Exception as e:

        raise HTTPException(
            status_code=500, detail=str(e))


@router.post('/clients/login/', tags=['clients'])
async def login(client: ClientLogin):
    try:
        first_query = """
             SELECT * FROM cliente_usuario WHERE nombre_usuario = :usuario
      """
        first_value = {
            "usuario": client.user
        }
        result = await database.fetch_one(query=first_query, values=first_value)

        if result is None:
            raise HTTPException(
                status_code=401, detail="Credenciales incorrectas")
        elif not check_password_hash(result[3], client.password):

            raise HTTPException(
                status_code=401, detail="Credenciales incorrectas")

        cliente_id = result[0]
        query = """
            SELECT nombre FROM cliente WHERE cliente_id = :client_id
        """
        values = {
            "client_id": cliente_id
        }
        name = await database.fetch_one(query=query, values=values)

        payload = {'sub': result[1], 'user': result[2], 'name': name[0]}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return {"token": token}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error al intentar verificar las credenciales")
