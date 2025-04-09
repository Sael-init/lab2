from app import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pagos'
    
    id_pago = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float(precision=2), nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_pago = db.Column(db.String(50))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_dueno = db.Column(db.Integer, db.ForeignKey('duenos.id_dueno'))
    
    def to_dict(self):
        return {
            'id_pago': self.id_pago,
            'monto': self.monto,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'metodo_pago': self.metodo_pago,
            'id_usuario': self.id_usuario,
            'id_dueno': self.id_dueno
        }