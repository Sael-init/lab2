from app import db
from datetime import datetime

class Distrito(db.Model):
    __tablename__ = 'distrito'
    
    id_distrito = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(10))
    ciudad = db.Column(db.String(100))
    
    # Relaciones
    cocheras = db.relationship('Cochera', backref='distrito', lazy=True)
    
    def to_dict(self):
        return {
            'id_distrito': self.id_distrito,
            'nombre': self.nombre,
            'codigo_postal': self.codigo_postal,
            'ciudad': self.ciudad
        }