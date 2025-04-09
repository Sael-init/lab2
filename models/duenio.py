from app import db
from datetime import datetime

class Dueno(db.Model):
    __tablename__ = 'duenos'
    
    id_dueno = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    cocheras = db.relationship('Cochera', backref='dueno', lazy=True)
    pagos = db.relationship('Pago', backref='dueno', lazy=True)
    registros = db.relationship('RegistroCochera', backref='dueno', lazy=True)
    
    def to_dict(self):
        return {
            'id_dueno': self.id_dueno,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }