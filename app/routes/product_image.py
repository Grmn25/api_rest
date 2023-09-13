from fastapi import APIRouter, HTTPException, UploadFile, File

from app.models import ImagenProductoCreate
from app.database import database

router = APIRouter()




@router.post("/images", tags=['product_image'])
async def get_images(
  image_data: ImagenProductoCreate  
):
    try:
        first_query = "SELECT * FROM producto WHERE producto_id = %s"
        first_values = (image_data.producto_id)
        product = await database.fetch_one(query=first_query, values=first_values)
        if product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
                

        query = """
            INSERT INTO imagen_producto (producto_id, imagen, es_imagen_principal)
            VALUES (:producto_id, :imagen, :is_principal_image)
            RETURNING (imagen_id, uploaded_at)
      
        """
        values = {
            "producto_id": image_data.producto_id,
            "imagen": image_data.imagen,
            "is_principal_image": image_data.is_principal_image
        }
        created_image = await database.fetch_one(query=query, values=values)
        if created_image:
            return created_image
        else: 
            raise HTTPException(status_code = 500, detail = "Error al crear la imagen")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
