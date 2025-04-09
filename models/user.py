from app import db, bcrypt
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    reservas = db.relationship('Reserva', backref='usuario', lazy=True)
    calificaciones = db.relationship('Calificacion', backref='usuario', lazy=True)
    pagos = db.relationship('Pago', backref='usuario', lazy=True)
    
    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }