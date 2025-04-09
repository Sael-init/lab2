import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables de entorno desde el archivo .env

class Config:
    # URL de conexión a la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///kuadra.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Otras configuraciones...