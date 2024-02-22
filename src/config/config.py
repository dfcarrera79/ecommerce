import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
db_uri = os.getenv("DEV_DB_URI")

# Configuración de la base de datos MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_NOVEDAD = os.getenv("MONGO_NOVEDAD")
MONGO_RECEPCION = os.getenv("MONGO_RECEPCION")