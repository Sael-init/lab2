from app import db
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = 'reserva'
    
    id_reserva = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(50), default='pendiente')
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_cochera = db.Column(db.Integer, db.ForeignKey('cochera.id_cochera'))
    
    __table_args__ = (
        db.CheckConstraint('fecha_fin > fecha_inicio', name='check_fechas'),
    )
    
    def to_dict(self):
        return {
            'id_reserva': self.id_reserva,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'estado': self.estado,
            'id_usuario': self.id_usuario,
            'id_cochera': self.id_cochera
        }