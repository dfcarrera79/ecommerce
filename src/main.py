import uvicorn
from fastapi import FastAPI
from src.routers import migracion
# from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API para migración de datos MongoDB a PostgreSQL",
    description="Back end desarrollado para la migración de datos MongoDB a PostgreSQL",
    version="1.0.0",
    contact={
        "name": "Diego Carrera",
        "url": "https://loxasoluciones.com/",
        "email": "dfcarrera@outlook.com",
    }
)

# API endpoints
app.include_router(migracion.router)

# Allow all origins in CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="src/public/images"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# import json
# from fastapi import FastAPI
# from pymongo import MongoClient
# from src.utils.utils import serializer


# # Conexión a la base de datos MongoDB local
# client = MongoClient('mongodb://localhost:27017/')
# db = client.get_database("emilia_apps")
# novedad_collection = db.get_collection("novedadproductos")

# # Configuración de FastAPI
# app = FastAPI()

# # Ruta para obtener todos los documentos de la colección novedadproducto
# @app.get("/novedades")
# async def get_novedades():
#     novedades = novedad_collection.find()
#     novedades_json = []
#     for novedad in novedades:
#         novedades_json.append(json.loads(json.dumps(novedad, default=serializer)))
#     return novedades_json
