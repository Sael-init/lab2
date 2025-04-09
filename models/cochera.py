from app import db
from datetime import datetime

class Cochera(db.Model):
    __tablename__ = 'cochera'
    
    id_cochera = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(255), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    precio_hora = db.Column(db.Float(precision=2), nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    id_distrito = db.Column(db.Integer, db.ForeignKey('distrito.id_distrito'))
    id_dueno = db.Column(db.Integer, db.ForeignKey('duenos.id_dueno'))
    
    # Relaciones
    reservas = db.relationship('Reserva', backref='cochera', lazy=True)
    calificaciones = db.relationship('Calificacion', backref='cochera', lazy=True)
    registros = db.relationship('RegistroCochera', backref='cochera', lazy=True)
    
    def to_dict(self):
        return {
            'id_cochera': self.id_cochera,
            'direccion': self.direccion,
            'capacidad': self.capacidad,
            'precio_hora': self.precio_hora,
            'disponible': self.disponible,
            'id_distrito': self.id_distrito,
            'id_dueno': self.id_dueno
        }