from app import db
from datetime import datetime

class Cochera(db.Model):
    __tablename__ = 'cocheras'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(200), nullable=False)
    distrito = db.Column(db.String(100), nullable=False)
    precio_hora = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    reservas = db.relationship('Reserva', backref='cochera', lazy=True, cascade="all, delete-orphan")
    calificaciones = db.relationship('Calificacion', backref='cochera', lazy=True, cascade="all, delete-orphan")
    
    def promedio_calificacion(self):
        if not self.calificaciones:
            return 0
        return sum(c.puntuacion for c in self.calificaciones) / len(self.calificaciones)
    
    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'direccion': self.direccion,
            'distrito': self.distrito,
            'precio_hora': self.precio_hora,
            'disponible': self.disponible,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'calificacion_promedio': self.promedio_calificacion(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }