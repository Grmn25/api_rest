from fastapi import APIRouter, HTTPException

from app.database import database
from app.models import Categoria

router = APIRouter()


@router.get("/categorys", tags=['categorys'])
async def get_categorys():
    try:
        query = "SELECT * FROM categoria"
        result = await database.fetch_all(query)
        return {"categorys": result}

    except Exception as e:
        return {"error": str(e)}


@router.get("/categorys/display", tags=['categorys'])
async def get_categorys_display():
    try:
        query = "SELECT * FROM categoria WHERE estado = 'Habilitado'"
        result = await database.fetch_all(query)
        return {"categorys": result}
    except Exception as e:
        return {"error": str(e)}


@router.post("/categorys", tags=['categorys'])
async def create_category(category: Categoria):
    try:
        query = """
            INSERT INTO categoria (categoria, estado)
            VALUES (:category, :estado)
            RETURNING categoria_id, categoria
        """
        values = {
            "category": category.category,
            "estado": category.estado
        }

        created_category = await database.fetch_one(query=query, values=values)

        if created_category:
            return created_category
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear la categoria")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/categorys/{category_id}", tags=['categorys'])
async def update_category(category: Categoria, category_id: int):
    try:
        query = """
            UPDATE categoria SET categoria = :category, estado = :estado
            WHERE categoria_id = :category_id
        """
        values = {
            "category": category.category,
            "estado": category.estado,
            "category_id": category_id
        }

        updated_category = await database.fetch_one(query=query, values=values)

        if updated_category:
            return updated_category
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear la categoria")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
