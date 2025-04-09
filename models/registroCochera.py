from app import db
from datetime import datetime

class RegistroCochera(db.Model):
    __tablename__ = 'registros_cochera'
    
    id_registro = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    detalles = db.Column(db.Text)
    id_cochera = db.Column(db.Integer, db.ForeignKey('cochera.id_cochera'))
    id_dueno = db.Column(db.Integer, db.ForeignKey('duenos.id_dueno'))
    
    def to_dict(self):
        return {
            'id_registro': self.id_registro,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'detalles': self.detalles,
            'id_cochera': self.id_cochera,
            'id_dueno': self.id_dueno
        }