import json
import fastapi
from src.config import config
from fastapi import Request
from sqlalchemy import create_engine
from src.config.controllers import SessionHandler

# Establish connections to PostgreSQL databases for "reclamos" and "apromed" respectively
engine = create_engine(config.db_uri)

# API Route Definitions
router = fastapi.APIRouter()

# Crear una instancia de la clase con tu motor de base de datos
query_handler = SessionHandler(engine)

@router.get("/categorias/listar")
async def get_categories():
    sql = "SELECT * FROM tcategory"
    return query_handler.execute_sql(sql, "Categorías consultadas exitosamente")

@router.post("/categorias/registrar")
async def registrar_categoria(request: Request):
    request_body = await request.body()
    data = json.loads(request_body)
    category_name = data["category_name"]
    description = data["description"]
    image_url = data["image_url"]
    sql = f"INSERT INTO tcategory (categoryName, description, imageUrl) VALUES ('{category_name}', '{description}', '{image_url}') RETURNING id"
    return query_handler.execute_sql(sql, "Categoría registrada exitosamente")

@router.put("/categorias/actualizar")
async def actualizar_categoria(request: Request):
    request_body = await request.body()
    data = json.loads(request_body)
    category_id = data["id"]
    category_name = data["category_name"]
    description = data["description"]
    image_url = data["image_url"]
    sql = f"UPDATE tcategory SET categoryName = '{category_name}', description = '{description}', imageUrl = '{image_url}' WHERE id = {category_id} RETURNING id"
    return query_handler.execute_sql(sql, "Categoría actualizada exitosamente")