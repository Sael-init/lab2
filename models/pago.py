from app import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pagos'
    
    id = db.Column(db.Integer, primary_key=True)
    reserva_id = db.Column(db.Integer, db.ForeignKey('reservas.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    comision = db.Column(db.Float, nullable=False)
    monto_propietario = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_pago = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')  # pendiente, completado, reembolsado
    referencia_externa = db.Column(db.String(100), nullable=True)  # Para referencia de la pasarela de pago
    
    def to_dict(self):
        return {
            'id': self.id,
            'reserva_id': self.reserva_id,
            'monto': self.monto,
            'comision': self.comision,
            'monto_propietario': self.monto_propietario,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'metodo_pago': self.metodo_pago,
            'estado': self.estado,
            'referencia_externa': self.referencia_externa
        }