from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import Purchase

router = APIRouter()

@router.get("/purchases", tags=['purchases'])
async def get_purchases():
    try:
        query = "SELECT * FROM compra"
        compras = await database.fetch_all(query=query)
        return {"compras": compras}

    except Exception as e:
        return {"error": str(e)}
    
@router.get("/purchases/{producto_id}", tags=['purchases'])
async def get_purchase(producto_id):
    try:
        query = "SELECT * FROM compra WHERE producto_id = :producto_id"
        value = {"producto_id": producto_id}
        compra = await database.fetch_one(query, value)
        return {"compra": compra}

    except Exception as e:
        return {"error": str(e)}
    
@router.post("/purchases", tags=['purchases'])
async def create_purchase(compra : Purchase):
    try:
        query = """
                INSERT INTO compra (id_compra, id_producto, nombre_producto, precio_unitario, cantidad_comprada, total_por_producto)
                VALUES (:id_compra, :producto_id, :nombre_producto, :precio, :cantidad, :total)
                RETURNING id_producto, nombre_producto, precio_unitario, cantidad_comprada, total_por_producto, fecha_compra
                """
        values = {"id_compra": compra.id_compra,
                  "producto_id":compra.producto_id,
                  "nombre_producto": compra.nombre_producto,
                  "precio": compra.precio_unitario,
                  "total": compra.total_producto,
                  }
        
        create_purchase = await database.fetch_one(query, values)

        if create_purchase:
            return create_purchase
        else: 
            raise HTTPException(status_code=500, detail="Error al crear la compra")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



