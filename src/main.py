import uvicorn
from fastapi import FastAPI
from src.routers import category
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="E-Commerce API",
    description="Back end desarrollado para plataforma de E-Commerce",
    version="1.0.0",
    contact={
        "name": "Diego Carrera",
        "url": "https://loxasoluciones.com/",
        "email": "dfcarrera@outlook.com",
    }
)

# API endpoints
app.include_router(category.router)

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