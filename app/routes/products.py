from fastapi import APIRouter, HTTPException

from app.database import database
from starlette.responses import StreamingResponse
from app.models import Producto

router = APIRouter()



@router.get("/products", tags=['products'])
async def get_products():
    try:
        query = "SELECT * FROM productos"
        result = await database.fetch_all(query)
        return {"products": result}

    except Exception as e:
        return {"error": str(e)}
 
@router.get("/products/{category}", tags=['products'])
async def get_products_category(category: str):
    try:
        query = "SELECT * FROM productos WHERE category_id = %s"
        values = (category,)
        result = await database.fetch_all(query, values=values)
        return {"products": result}

    except Exception as e:
        return {"error": str(e)}


@router.get("/products/{id}", tags=['products'])
async def get_product(id: int):
    try:
        query = "SELECT * FROM productos WHERE producto_id = %s"
        values = (id,)
        result = await database.fetch_one(query, values=values)
        return {"products": result}

    except Exception as e:
        return {"error": str(e)}
    

@router.get("/products/{product_id}/image/", tags=['products'])
async def get_product_image(
    product_id: int
):
    try:
        product = """
             SELECT * FROM imagen_producto WHERE producto_id = :product_id
    
        """
        value_product = {"product_id": product_id}
        result_product = await database.fetch_all(query=product, values=value_product)
        if not result_product:
            raise HTTPException(status_code=404, detail="Imagen de producto no encontrada")
        imagen_producto = """
            SELECT imagen FROM imagen_producto WHERE producto_id = :product_id
          """
        value = {"product_id": product_id}
        result_img = await database.fetch_all(query=imagen_producto, values=value)
        if not result_img:
            raise HTTPException(status_code=404, detail="Imagen de producto no encontrada")
        image_list = [result["imagen"] for result in result_img]
        return [StreamingResponse(content=image, media_type="image/jpeg") for image in image_list]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    

    

@router.post("/products", tags=['products'])
async def create_product(product: Producto):
    try:
        query = """
        INSERT INTO producto (nombre_producto, precio, descripcion, stock, categoria_id)
        VALUES (:name, :price, :desc, :stock, :category_id)
        RETURNING producto_id, nombre_producto, precio, descripcion, stock, categoria_id
        """
        values = {
            "name": product.name,
            "price": product.price,
            "desc": product.desc,
            "stock": product.stock,
            "category_id":product.category_id
        }

        created_product = await database.fetch_one(query=query, values=values)

        if created_product:
            return created_product
        else: 
            raise HTTPException(status_code = 500, detail = "Error al crear el producto")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 