from fastapi import APIRouter, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Cliente, ClientLogin
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


@router.post("/clients/", tags=['clients'])
async def create_user(client: Cliente):
    try:
        # Verificar si el cliente ya existe en la base de datos
        first_query = "SELECT cliente_id FROM cliente WHERE email= :email"
        first_value = {"email": client.email}
        client_exist = await database.fetch_one(first_query, first_value)
        if client_exist:
            raise HTTPException(
                status_code=500, detail="Error al crear el usuario, email ya registrado")

        query = """
            INSERT INTO cliente (nombre, email, cliente_password, telefono, direccion)
            VALUES (:name, :email, :password, :telefono, :direccion)
            RETURNING cliente_id, nombre, email, fecha_registro
        """
        values = {
            "name": client.name,
            "email": client.email,
            "password": generate_password_hash(client.password),
            "telefono": client.telefono,
            "direccion": client.direccion
        }
        created_client = await database.fetch_one(query=query, values=values)
        
        if created_client:
            payload = {"sub": created_client[0], 'email': created_client[2]}
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
             SELECT * FROM cliente WHERE email = :email
      """
        first_value = {
            "email": client.email
        }
        result = await database.fetch_one(query=first_query, values=first_value)
        if result is None:
            raise HTTPException(
                status_code=401, detail="Credenciales incorrectas")
        elif not check_password_hash(result[3], client.password):
            raise HTTPException(
                status_code=401, detail="Credenciales incorrectas")
        payload = {'sub': result[0], 'email': result[2]}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return {"token": token}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error al intentar verificar las credenciales")
