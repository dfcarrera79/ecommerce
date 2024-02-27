import json
import fastapi
from config import config
from sqlalchemy.orm import Session
from utils.utils import serializer
from sqlalchemy import create_engine, text
from config.controllers import SessionHandler


def clean_dict(d):
    cleaned = {}
    for key, value in d.items():
        if isinstance(value, dict):
            if '$oid' in value:
                cleaned[key] = value['$oid']
            elif '$date' in value:
                cleaned[key] = str(value['$date']).split("T")[0]
            else:
                cleaned[key] = clean_dict(value)
        elif isinstance(value, list):
            cleaned[key] = [clean_dict(item) if isinstance(item, dict) else item for item in value]
        else:
            cleaned[key] = value
            
    # Corregir formato de fecha para la clave 'auditoria'
    if 'auditoria' in cleaned:
        for item in cleaned['auditoria']:
            if 'fecha' in item:
                # Convertir a str y luego extraer la parte de la fecha
                item['fecha'] = str(item['fecha']).split("T")[0]
            
    return cleaned


with open('routers/emilia_apps.recepcionproductos.json', 'r', encoding='utf-8') as f:
    recepciones = json.load(f)
    # print('[RECEPCION]: ', recepciones[0])
    recepciones_dict = [clean_dict(recepcion) for recepcion in recepciones]
    # print('[RECEPCION CLEAN]: ', recepciones_dict[0])
    
    

engine = create_engine(config.db_uri)
query_handler = SessionHandler(engine)

# API Route Definitions
router = fastapi.APIRouter()


@router.post("/migracion/recepcion_productos")
async def migracion_recepcion():  
    version = "APROMED_v01"
    modelo = "APROMED"
    tipo_formulario = "RECEPCION"

    for recepcion in recepciones_dict:               
        # Eliminar el campo __v si existe
        recepcion.pop('__v', None)
        # formulario_arcsa = json.loads(json.dumps(recepcion, default=serializer))
        formulario_arcsa = recepcion
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




# @router.post("/migracion/recepcion_productos")
# async def migracion_recepcion():  
#     version = "APROMED_v01"
#     modelo = "APROMED"
#     tipo_formulario = "RECEPCION"

#     for recepcion in recepciones:
#         # Eliminar el campo __v si existe
#         recepcion.pop('__v', None)
#         formulario_arcsa = json.loads(json.dumps(recepcion))
        
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