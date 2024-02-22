import json
import fastapi
from src.config import config
from pymongo import MongoClient
from sqlalchemy.orm import Session
from src.utils.utils import serializer
from sqlalchemy import create_engine, text
from src.config.controllers import SessionHandler

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


async def get_recepciones():
    recepciones = recepcion_collection.find()
    recepciones_json = []
    for recepcion in recepciones:
        recepciones_json.append(json.loads(json.dumps(recepcion, default=serializer)))
    return recepciones_json

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
        print('[NOVEDAD]: ', formulario_arcsa["_id"])
        
        secuencia = novedad["secuencia"]
        no_formulario = novedad["formulario"]
        
        # Convertir el objeto JSON a cadena de texto
        json_string = json.dumps(formulario_arcsa).replace("'", "''")  # Escapa las comillas simples
        
        
        if "trn_codigo" in novedad:
            trn_codigo = novedad["trn_codigo"]
            sql = f"""
            INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
            VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}', {trn_codigo})"""
        else:
            sql = f"""
            INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario)
            VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}') RETURNING id_formulario"""
        
        # print('[SQL]: ', sql)
        
        with Session(engine) as session:
            session.execute(text(sql)).fetchall()
            session.commit()

    return "Migración de novedades completada satisfactoriamente"    


@router.post("/migracion/recepcion_productos")
async def migracion_novedad():  
    recepciones = recepcion_collection.find()
    
    version = "APROMED_v01"
    modelo = "APROMED"
    tipo_formulario = "NOVEDAD"

    for recepcion in recepciones:
        # Eliminar el campo __v si existe
        recepcion.pop('__v', None)
        formulario_arcsa = json.loads(json.dumps(recepcion, default=serializer))
        print('[RECEPCION]: ', formulario_arcsa["_id"])
        
        secuencia = recepcion["secuencia"]
        no_formulario = recepcion["formulario"]
        
        # Convertir el objeto JSON a cadena de texto
        json_string = json.dumps(formulario_arcsa).replace("'", "''")  # Escapa las comillas simples
        
        
        if "trn_codigo" in recepcion:
            trn_codigo = recepcion["trn_codigo"]
            sql = f"""
            INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
            VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}', {trn_codigo})"""
        else:
            sql = f"""
            INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario)
            VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}') RETURNING id_formulario"""
        
        
        with Session(engine) as session:
            session.execute(text(sql)).fetchall()
            session.commit()

    return "Migración de recepciones completada satisfactoriamente" 
    
    # novedades = await get_novedades()
    # print('[NOVEDADES LENGTH]: ', len(novedades))
    # for novedad in novedades:
    #     no_formulario = novedad["formulario"]
    #     secuencia = novedad["secuencia"]
    #     version = "APROMED_v01"
    #     modelo = "APROMED"
    #     tipo_formulario = "NOVEDAD"
        
    #     sql = f"""
    #     INSERT INTO comun.tformularioarcsa (no_formulario, secuencia, formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
    #     VALUES ({no_formulario}, {secuencia}, {novedad}, {version}, {modelo}, {tipo_formulario})"""
    #     return query_handler.execute_sql(sql,  "Migración completada") 
    
    
    # try:
    #     for novedad in novedades:
    #         no_formulario = novedad["formulario"]
    #         secuencia = novedad["secuencia"]
    #         version = "APROMED_v01"
    #         modelo = "APROMED"
    #         tipo_formulario = "NOVEDAD"
            
    #         sql = f"""
    #         INSERT INTO comun.tformularioarcsa (no_formulario, secuencia, formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
    #         VALUES ({no_formulario}, {secuencia}, {novedad}, {version}, {modelo}, {tipo_formulario})"""
    #         query_handler.execute_sql(sql,  "Migración completada satisfactoriamente")
    #     return "Migración de novedades completada satisfactoriamente"
    # except Exception as e:
    #     return {"error": e}

# @router.post("/migracion/recepcion_productos")
# async def start_recepcion_migration():
#     recepciones = await get_recepciones()
#     try:
#         for recepcion in recepciones:
#             no_formulario = recepcion["formulario"]
#             secuencia = recepcion["secuencia"]
#             version = "APROMED_v01"
#             modelo = "APROMED"
#             tipo_formulario = "RECEPCION"
            
#             sql = f"""
#             INSERT INTO comun.tformularioarcsa (no_formulario, secuencia, formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
#             VALUES ({no_formulario}, {secuencia}, {recepcion}, {version}, {modelo}, {tipo_formulario})"""
#             query_handler.execute_sql(sql,  "Migración completada satisfactoriamente")
#         return "Migración de recepciones completada satisfactoriamente"
#     except Exception as e:
#         return {"error": e}

















# import fastapi
# import pymongo
# from src.config import config
# from sqlalchemy import create_engine
# from src.config.controllers import SessionHandler

# # Establish connections to PostgreSQL database 
# engine = create_engine(config.db_uri)

# # API Route Definitions
# router = fastapi.APIRouter()

# # Crear una instancia de la clase con tu motor de base de datos
# query_handler = SessionHandler(engine)

# @router.post("/migracion/novedad_productos")
# async def start_migration():
#     # Establish connections to Mongo database inside the function
#     client = pymongo.MongoClient(config.MONGO_URI)
#     db = client[config.MONGO_DB]
#     collection = db[config.MONGO_NOVEDAD]

#     mongo_documents = collection.find({})
    
#     for document in mongo_documents:
#         print('[DOCUMENT]: ', document)
#         no_formulario = document.get("formulario")
#         secuencia = document.get("secuencia")
#         version = "APROMED_v01"
#         modelo = "APROMED"
#         tipo_formulario = "NOVEDAD"
        
#         sql = f"""
#         INSERT INTO comun.tformularioarcsa (no_formulario, secuencia, formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
#         VALUES ({no_formulario}, {secuencia}, {document}, {version}, {modelo}, {tipo_formulario})"""
#         query_handler.execute_sql(sql,  "Migración completada satisfactoriamente")
        
#     client.close()  # Close MongoDB connection after migration
    
#     return "Migración completada satisfactoriamente"    

# @router.post("/migracion/recepcion_productos")
# async def start_migration():
#     # Establish connections to Mongo database inside the function
#     client = pymongo.MongoClient(config.MONGO_URI)
#     db = client[config.MONGO_DB]
#     collection = db[config.MONGO_RECEPCION]

#     mongo_documents = collection.find({})
    
#     for document in mongo_documents:
#         print('[DOCUMENT]: ', document)
#         no_formulario = document.get("formulario")
#         secuencia = document.get("secuencia")
#         version = "APROMED_v01"
#         modelo = "APROMED"
#         tipo_formulario = "RECEPCION"
        
#         sql = f"""
#         INSERT INTO comun.tformularioarcsa (no_formulario, secuencia, formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
#         VALUES ({no_formulario}, {secuencia}, {document}, {version}, {modelo}, {tipo_formulario})"""
#         query_handler.execute_sql(sql,  "Migración completada satisfactoriamente")
        
#     client.close()  # Close MongoDB connection after migration
    
#     return "Migración completada satisfactoriamente"    










# import json
# import fastapi
# from src.config import config
# from pymongo import MongoClient
# from sqlalchemy.orm import Session
# from src.utils.utils import serializer
# from sqlalchemy import create_engine, text
# from src.config.controllers import SessionHandler

# with open('src/routers/novedadproductos.json', 'r', encoding='utf-8') as f:
#     novedades = json.load(f)

# engine = create_engine(config.db_uri)
# query_handler = SessionHandler(engine)

# # API Route Definitions
# router = fastapi.APIRouter()

# # def get_novedades():
# #     novedades_json = []
# #     for novedad in novedades:
# #         novedades_json.append(json.loads(json.dumps(novedad, default=serializer)))
# #     return novedades_json


# # async def get_recepciones():
# #     recepciones_json = []
# #     for recepcion in recepciones:
# #         recepciones_json.append(json.loads(json.dumps(recepcion, default=serializer)))
# #     return recepciones_json

# @router.post("/migracion/novedad_productos")
# async def migracion_novedad():  
#     version = "APROMED_v01"
#     modelo = "APROMED"
#     tipo_formulario = "NOVEDAD"

#     for novedad in novedades:
#         print('[NOVEDAD]: ', novedad)
#         # Eliminar el campo __v si existe
#         novedad.pop('__v', None)
#         formulario_arcsa = json.loads(json.dumps(novedad, default=serializer))
#         # print('[NOVEDAD]: ', formulario_arcsa["_id"])
        
#         secuencia = novedad["secuencia"]
#         no_formulario = novedad["formulario"]
        
#         # Convertir el objeto JSON a cadena de texto
#         json_string = json.dumps(formulario_arcsa).replace("'", "''")  # Escapa las comillas simples

#         if "trn_codigo" in novedad:
#             trn_codigo = novedad["trn_codigo"]
#             sql = f"""
#             INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario, trn_codigo)
#             VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}', {trn_codigo})"""
#         else:
#             sql = f"""
#             INSERT INTO comun.tformularioarcsa (secuencia, no_formulario,  formulario_arcsa, version, modelo, tipo_formulario)
#             VALUES ({secuencia}, '{no_formulario}', '{json_string}', '{version}', '{modelo}', '{tipo_formulario}') RETURNING id_formulario"""
        
#         # print('[SQL]: ', sql)
        
#         with Session(engine) as session:
#             session.execute(text(sql)).fetchall()
#             session.commit()

#     return "Migración de novedades completada satisfactoriamente"    