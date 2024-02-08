from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

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