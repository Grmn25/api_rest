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


@router.post("/categorys", tags=['categorys'])
async def create_category(category: Categoria):
    try:
        query = """
            INSERT INTO categoria (categoria)
            VALUES (:category)
            RETURNING categoria_id, categoria
        """
        values = {
            "category": category.category
        }

        created_category = await database.fetch_one(query=query, values=values)

        if created_category:
            return created_category
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear la categoria")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
