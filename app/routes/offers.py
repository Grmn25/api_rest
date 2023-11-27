
from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import Oferta

router = APIRouter()


@router.get("/offers", tags=['offers'])
async def get_offers():
    try:
        query = "SELECT * FROM oferta"
        offers = await database.fetch_all(query=query)
        return {"offers": offers}

    except Exception as e:
        return {"error": str(e)}


@router.get("/offers/{producto_id}", tags=['offers'])
async def get_offer(producto_id):
    try:
        query = "SELECT * FROM oferta WHERE producto_id = :producto_id"
        value = {"producto_id": producto_id}
        offer = await database.fetch_one(query, value)
        return {"offer": offer}

    except Exception as e:
        return {"error": str(e)}


@router.post("/offers", tags=['offers'])
async def create_offer(offer: Oferta):
    try:
        query = """
                INSERT INTO oferta (producto_id, descuento, fecha_inicio, fecha_termino)
                VALUES (:producto_id, :descuento, :fecha_inicio, :fecha_termino)
                RETURNING producto_id, descuento, fecha_inicio, fecha_termino
                """
        values = {"producto_id": offer.producto_id,
                  "descuento": offer.discount,
                  "fecha_inicio": offer.date_start,
                  "fecha_termino": offer.date_end
                  }

        create_offer = await database.fetch_one(query, values)

        if create_offer:
            return create_offer
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear la oferta")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/offers/{producto_id}", tags=['offers'])
async def modify_offer(offer: Oferta):
    try:
        query = """
                UPDATE oferta
                SET porcentaje_descuento = :porcentaje, fecha_inicio = :fecha_inicio, fecha_termino = :fecha_termino
                WHERE producto_id = :producto_id
            """
        values = {"porcentaje": offer.discount,
                  "fecha_inicio": offer.date_start,
                  "fecha_termino": offer.date_end,
                  "producto_id": offer.producto_id,
                  }

        update_offer = await database.fetch_one(query, values)

        if update_offer:
            return update_offer
        else:
            raise HTTPException(
                status_code=500, detail="Error al crear la oferta")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
