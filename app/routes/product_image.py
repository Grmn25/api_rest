import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from app.models import ImagenProductoCreate
from starlette.responses import StreamingResponse
from app.database import database
import uuid
import shutil
from typing import List
from pathlib import Path
import tinify
import base64






router = APIRouter()


@router.get("/image/{product_id}/principal", tags=['product_image'])
async def get_product_image(product_id: int):
    try:
        product = """
            SELECT * FROM imagen_producto WHERE producto_id = :product_id and
            es_imagen_principal = :bool
        """
        value_product = {"product_id": product_id, "bool": True}
        result_product = await database.fetch_all(query=product,
                                                  values=value_product)

        if not result_product:
            raise HTTPException(
                status_code=404, detail="Imagen del producto {} no encontrada".format(product_id))
        else:
            for row in result_product:
                imagen_url = row[2]

                return FileResponse(imagen_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/{product_id}", tags=['product_image'])
async def get_product_images(product_id: int):
    try:
        product = """
             SELECT imagen_id, imagen_url FROM imagen_producto WHERE producto_id = :product_id
        """
        value_product = {"product_id": product_id}
        result_product = await database.fetch_all(query=product, values=value_product)
        
        if not result_product:
            raise HTTPException(
                status_code=404, detail="Imagen del producto {} no encontrada".format(product_id))

        images = []
        for row in result_product:
            imagen_id, imagen_url = row[0], row[1]
            image_path = Path(imagen_url)
            if image_path.exists() and image_path.is_file():
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
                    images.append({"imagen_id": imagen_id, "imagen_data": image_base64})

        if not images:
            raise HTTPException(
                status_code=404, detail="No se encontraron imágenes para el producto con ID: {}".format(product_id))

        return JSONResponse(content={"imagenes": images})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/images", tags=['product_image'])
async def get_images(
    producto_id: int,
    file: UploadFile,
    es_imagen_principal: bool
):
    try:
        first_query = "SELECT * FROM producto WHERE producto_id = :producto_id"
        first_values = {"producto_id": producto_id}  # Cambia a un diccionario
        product = await database.fetch_one(query=first_query, values=first_values)

        if product is None:
            raise HTTPException(
                status_code=404, detail="Producto no encontrado")

        image_folder = "img_products"
        os.makedirs(image_folder, exist_ok=True)
        file_extension = os.path.splitext(file.filename)[1]
        image_filename = str(uuid.uuid4()) + file_extension
        image_path = os.path.join(image_folder, image_filename)
        with open(image_path, "wb") as image_file:
            shutil.copyfileobj(file.file, image_file)

        query = """
            INSERT INTO imagen_producto (producto_id, imagen_url, es_imagen_principal)
            VALUES (:producto_id, :imagen, :is_principal_image)
            RETURNING imagen_id, uploaded_at
        """

        values = {
            "producto_id": producto_id,
            "imagen": image_path,
            "is_principal_image": es_imagen_principal
        }

        created_image = await database.fetch_one(query=query, values=values)

        if created_image:
            return created_image
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear la imagen")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images/multiple", tags=['product_image'])
async def create_product_images(
    files: List[UploadFile],
):
    try:
        first_query = "SELECT MAX(producto_id) FROM producto"

        max_id_record = await database.fetch_one(first_query)
        if max_id_record and max_id_record[0] is not None:
            producto_id = max_id_record[0]
        else:
            raise HTTPException(
                status_code=500, detail="Error al intentar cargar las imagenes"
            )

        first_principal_image_found = False

        for file in files:
            image_folder = "img_products"
            os.makedirs(image_folder, exist_ok=True)
            file_extension = os.path.splitext(file.filename)[1]
            image_filename = str(uuid.uuid4()) + file_extension
            image_path = os.path.join(image_folder, image_filename)
            with open(image_path, "wb") as image_file:
                shutil.copyfileobj(file.file, image_file)

            is_principal_image = not first_principal_image_found

            query = """
                INSERT INTO imagen_producto (producto_id, imagen_url, es_imagen_principal)
                VALUES (:producto_id, :imagen, :is_principal_image)
                RETURNING imagen_id, uploaded_at
            """

            values = {
                "producto_id": producto_id,
                "imagen": image_path,
                "is_principal_image": is_principal_image
            }

            images = await database.fetch_one(query=query, values=values)
            if not images:
                raise HTTPException(
                    status_code=500, detail="Error al crear la imagen")

            if is_principal_image:
                first_principal_image_found = True

        return {"message": "Imágenes de productos creadas exitosamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
