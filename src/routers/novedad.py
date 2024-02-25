import json
import fastapi
from config import config
from pymongo import MongoClient
from sqlalchemy.orm import Session
from utils.utils import serializer
from sqlalchemy import create_engine, text
from config.controllers import SessionHandler


client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]
novedad_collection = db[config.MONGO_NOVEDAD]
recepcion_collection = db[config.MONGO_RECEPCION]


engine = create_engine(config.db_uri)
query_handler = SessionHandler(engine)


# API Route Definitions
router = fastapi.APIRouter()


async def get_novedades():
    novedades = novedad_collection.find()
    novedades_json = []
    for novedad in novedades:
        novedades_json.append(json.loads(json.dumps(novedad, default=serializer)))
    return novedades_json


@router.post("/migracion/novedad_productos")
async def migracion_novedad():  
    novedades = novedad_collection.find()
    
    version = "APROMED_v01"
    modelo = "APROMED"
    tipo_formulario = "NOVEDAD"

    for novedad in novedades:
        # Eliminar el campo __v si existe
        novedad.pop('__v', None)
        formulario_arcsa = json.loads(json.dumps(novedad, default=serializer))     
        secuencia = novedad["secuencia"]
        no_formulario = novedad["formulario"]
        
        # Convertir el objeto JSON a cadena de texto
        json_string = json.dumps(formulario_arcsa).replace("'", "''")  # Escapa las comillas simples
        
        
        if "trn_codigo" in novedad:
            trn_codigo = novedad["trn_codigo"]
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

    return "Migración de novedades completada satisfactoriamente"  


# async def get_recepciones():
#     recepciones = recepcion_collection.find()
#     recepciones_json = []
#     for recepcion in recepciones:
#         recepciones_json.append(json.loads(json.dumps(recepcion, default=serializer)))
#     return recepciones_json


# @router.post("/migracion/recepcion_productos")
# async def migracion_recepcion():  
#     recepciones = recepcion_collection.find()
    
#     version = "APROMED_v01"
#     modelo = "APROMED"
#     tipo_formulario = "NOVEDAD"

#     for recepcion in recepciones:               
#         # Eliminar el campo __v si existe
#         recepcion.pop('__v', None)
#         formulario_arcsa = json.loads(json.dumps(recepcion, default=serializer))
#         secuencia = recepcion["secuencia"]
#         no_formulario = recepcion["formulario"]
        
#         # Convertir el objeto JSON a cadena de texto
#         json_string = json.dumps(formulario_arcsa).replace("'", "''")  # Escapa las comillas simples
        
        
#         if "trn_codigo" in recepcion:
#             trn_codigo = recepcion["trn_codigo"]
#             sql = f"""
#             INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
#             VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}', {trn_codigo}) RETURNING id_formulario"""
#         else:
#             sql = f"""
#             INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario)
#             VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}') RETURNING id_formulario"""

        
#         with Session(engine) as session:
#             session.execute(text(sql)).fetchall()
#             session.commit()

#     return "Migración de recepciones completada satisfactoriamente"  