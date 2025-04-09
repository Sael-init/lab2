from app import db
from datetime import datetime

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cochera_id = db.Column(db.Integer, db.ForeignKey('cocheras.id'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)  # 1-5
    comentario = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'autor_id': self.autor_id,
            'cochera_id': self.cochera_id,
            'puntuacion': self.puntuacion,
            'comentario': self.comentario,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }