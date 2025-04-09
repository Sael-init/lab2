from app import db
from datetime import datetime

class Calificacion(db.Model):
    __tablename__ = 'calificacion'
    
    id_calificacion = db.Column(db.Integer, primary_key=True)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_cochera = db.Column(db.Integer, db.ForeignKey('cochera.id_cochera'))
    
    __table_args__ = (
        db.CheckConstraint('puntuacion >= 1 AND puntuacion <= 5', name='check_puntuacion'),
    )
    
    def to_dict(self):
        return {
            'id_calificacion': self.id_calificacion,
            'puntuacion': self.puntuacion,
            'comentario': self.comentario,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'id_usuario': self.id_usuario,
            'id_cochera': self.id_cochera
        }