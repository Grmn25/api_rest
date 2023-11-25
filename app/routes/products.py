from fastapi import APIRouter, HTTPException

from app.database import database
from app.models import Producto

router = APIRouter()


@router.get("/products", tags=['products'])
async def get_products():
    try:
        query = "SELECT * FROM producto"
        result = await database.fetch_all(query)
        return {"products": result}

    except Exception as e:
        return {"error": str(e)}


@router.get("/products/display", tags=['products'])
async def get_products_display():
    try:
        query = "SELECT * FROM producto WHERE estado = 'disponible'"
        result = await database.fetch_all(query)
        return {"products": result}

    except Exception as e:
        return {"error": str(e)}


@router.get("/products/{category}", tags=['products'])
async def get_products_category(category: str):
    try:
        first_query = "SELECT categoria_id FROM categoria WHERE categoria = :categoria"
        first_value = {"categoria": category}
        categoria_id = await database.fetch_one(query=first_query, values=first_value)

        query = "SELECT * FROM producto WHERE categoria_id = :categoria_id"
        values = {"categoria_id": categoria_id["categoria_id"]}
        result = await database.fetch_all(query=query, values=values)
        return {"products": result}

    except Exception as e:
        return {"error": str(e)}


@router.get("/products/{category}/display", tags=['products'])
async def get_products_category(category: str):
    try:
        first_query = "SELECT categoria_id FROM categoria WHERE categoria = :categoria and estado = 'disponible'"
        first_value = {"categoria": category}
        categoria_id = await database.fetch_one(query=first_query, values=first_value)

        query = "SELECT * FROM producto WHERE categoria_id = :categoria_id"
        values = {"categoria_id": categoria_id["categoria_id"]}
        result = await database.fetch_all(query=query, values=values)
        return {"products": result}

    except Exception as e:
        return {"error": str(e)}


@router.get("/product/{id}", tags=['products'])
async def get_product(id: int):
    try:
        first_query = "SELECT * FROM producto WHERE producto_id = :producto"
        first_value = {"producto": id}
        producto = await database.fetch_one(query=first_query, values=first_value)
        return {"product": producto}

    except Exception as e:
        return {"error": str(e)}


@router.post("/products", tags=['products'])
async def create_product(product: Producto):
    try:
        query = """
        INSERT INTO producto (nombre_producto, precio, descripcion, stock,
        categoria_id, estado)
        VALUES (:name, :price, :desc, :stock, :category_id, :estado)
        RETURNING producto_id, nombre_producto, precio, descripcion, stock,
        categoria_id
        """
        values = {
            "name": product.name,
            "price": product.price,
            "desc": product.desc,
            "stock": product.stock,
            "category_id": product.category_id,
            "estado": product.estado
        }

        created_product = await database.fetch_one(query=query, values=values)

        if created_product:
            return created_product
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear el producto")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/products/{id}", tags=['products'])
async def update_product(product: Producto, id: int):
    try:
        query = """
        UPDATE producto SET nombre_producto = :name, precio = :price, 
        descripcion = :desc, stock = :stock, categoria_id = :category_id, estado = :estado
        WHERE producto_id = :id
        RETURNING producto_id, nombre_producto, precio, descripcion, stock,
        categoria_id
        """
        values = {
            "name": product.name,
            "price": product.price,
            "desc": product.desc,
            "stock": product.stock,
            "category_id": product.category_id,
            "estado": product.estado,
            "id": id
        }

        created_product = await database.fetch_one(query=query, values=values)

        if created_product:
            return created_product
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear el producto")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
