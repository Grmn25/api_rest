from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import Review

router = APIRouter()

@router.get("/reviews", tags=['reviews'])
async def get_reviews():
    try:
        query = "SELECT * FROM producto_review"
        reviews = await database.fetch_all(query=query)
        return {"reviews": reviews}

    except Exception as e:
        return {"error": str(e)}
    
@router.get("/reviews/{producto_id}", tags=['reviews'])
async def get_review(producto_id):
    try:
        query = "SELECT * FROM producto_review WHERE producto_id = :producto_id"
        value = {"producto_id": producto_id}
        review = await database.fetch_one(query, value)
        return {"review": review}

    except Exception as e:
        return {"error": str(e)}
    
@router.post("/reviews", tags=['reviews'])
async def create_review(review : Review):
    try:
        query = """
                INSERT INTO producto_review (producto_id, cliente_id, puntuacion, review_texto)
                VALUES (:producto_id, :cliente, :puntuacion, :review)
                RETURNING producto_id, cliente_id, puntuacion, review_texto, review_date
                """
        values = {"producto_id":review.producto_id,
                  "cliente": review.cliente_id,
                  "puntuacion": review.puntuacion,
                  "review": review.review,
                  }
        
        create_review = await database.fetch_one(query, values)

        if create_review:
            return create_review
        else: 
            raise HTTPException(status_code=500, detail="Error al crear la reseña")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


