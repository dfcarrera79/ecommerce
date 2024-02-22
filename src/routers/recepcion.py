import json
import fastapi
from src.config import config
from sqlalchemy.orm import Session
from src.utils.utils import serializer
from sqlalchemy import create_engine, text
from src.config.controllers import SessionHandler

with open('src/routers/emilia_apps.recepcionproductos.json', 'r', encoding='utf-8') as f:
    recepciones = json.load(f)

engine = create_engine(config.db_uri)
query_handler = SessionHandler(engine)

# API Route Definitions
router = fastapi.APIRouter()


@router.post("/migracion/recepcion_productos")
async def migracion_recepcion():  
    version = "APROMED_v01"
    modelo = "APROMED"
    tipo_formulario = "RECEPCION"

    for recepcion in recepciones:
        # Eliminar el campo __v si existe
        recepcion.pop('__v', None)
        formulario_arcsa = json.loads(json.dumps(recepcion, default=serializer))
        
        secuencia = recepcion["secuencia"]
        no_formulario = recepcion["formulario"]
        
        # Convertir el objeto JSON a cadena de texto
        json_string = json.dumps(formulario_arcsa).replace("'", "''")  # Escapa las comillas simples

        if "trn_codigo" in recepcion:
            trn_codigo = recepcion["trn_codigo"]
            sql = f"""
            INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
            VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}', {trn_codigo}) RETURNING id_formulario"""
        else:
            sql = f"""
            INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario)
            VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}') RETURNING id_formulario"""
        
        with Session(engine) as session:
            session.execute(text(sql)).fetchall()
            session.commit()

    return "Migración de recepciones completada satisfactoriamente"    