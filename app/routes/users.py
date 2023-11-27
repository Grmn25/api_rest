from fastapi import APIRouter, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario, Login
from app.database import database

router = APIRouter()


@router.get("/users/", tags=['users'])
async def get_users():
    try:
        query = "SELECT * FROM usuario"
        result = await database.fetch_all(query)
        return {"users": result}

    except Exception as e:
        return {"error": str(e)}


@router.post("/users/", tags=['users'])
async def create_user(user: Usuario):
    try:
        query = """
            INSERT INTO usuario (nombre, usuario, email, pass)
            VALUES (:name, :user, :email, :password)
            RETURNING usuario_id, nombre, usuario, email, created_at
        """
        values = {
            "name": user.name,
            "user": user.user,
            "email": user.email,
            "password": generate_password_hash(user.password)
        }
        created_user = await database.fetch_one(query=query, values=values)
        if created_user:
            return created_user
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear el usuario")

    except Exception:
        raise HTTPException(
            status_code=500, detail="Error al crear el usuario")


@router.post('/users/login/', tags=['users'])
async def login(user: Login):
    try:
        first_query = """
             SELECT * FROM usuario WHERE usuario = :user
      """
        first_value = {
            "user": user.user
        }
        result = await database.fetch_one(query=first_query, values=first_value)
        if result is None:
            raise HTTPException(
                status_code=401, detail="Credenciales incorrectas")
        elif not check_password_hash(result[4], user.password):
            raise HTTPException(
                status_code=401, detail="Credenciales incorrectas")
        usuario_id = result[0]
        return {"check": usuario_id}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error al intentar verificar las credenciales")


@router.put('/users/login/{usuario_id}', tags=['users'])
async def login(user: Usuario, usuario_id: int):
    try:
        first_query = """
             SELECT * FROM usuario WHERE usuario_id = :usuario_id
      """
        first_value = {
            "usuario_id": usuario_id
        }
        result = await database.fetch_one(query=first_query, values=first_value)
        if result is None:
            raise HTTPException(
                status_code=401, detail="Usuario no es válido")

        update_query = """
            UPDATE usuario SET nombre = :nombre, usuario = :usuario, email = :email, password = :password WHERE usuario_id = :usuario_id
        """
        values_update = (
            "nombre", user.name,
            "usuario", user.user,
            "email", user.email,
            "password", generate_password_hash(user.password),
            "usuario_id", usuario_id
        )

        execute_update = await database.execute(query=update_query, values=values_update)
        if execute_update is None:
            raise HTTPException(
                status_code=401, detail="Usuario no se ha podido actualizar")

        return {"check": usuario_id}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error al intentar verificar las credenciales")
