import uvicorn
from fastapi import FastAPI
from routers import novedad
from routers import recepcion
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="API para migración de datos MongoDB a PostgreSQL",
    description="Back End desarrollado para la migración de datos MongoDB a PostgreSQL",
    version="1.0.0",
    contact={
        "name": "Diego Carrera",
        "url": "https://loxasoluciones.com/",
        "email": "dfcarrera@outlook.com",
    }
)


# API endpoints
app.include_router(novedad.router)
app.include_router(recepcion.router)


# Allow all origins in CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)