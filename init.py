from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Crear instancias de las extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar SQLAlchemy con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints y demás configuraciones...
    
    return app