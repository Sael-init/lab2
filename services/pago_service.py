from app import db
from app.models.pago import Pago
from app.models.reserva import Reserva
from datetime import datetime
import uuid

class PagoService:
    @staticmethod
    def process_payment(reserva_id, cliente_id, metodo_pago='tarjeta'):
        # Verificar que la reserva existe y pertenece al usuario
        reserva = Reserva.query.get(reserva_id)
        if not reserva or reserva.cliente_id != cliente_id:
            return None, "Reserva no encontrada o no autorizada"
        
        # Verificar que la reserva esté confirmada
        if reserva.estado != 'confirmado':
            return None, "Solo se pueden pagar reservas confirmadas"
        
        # Verificar que no haya un pago previo
        if Pago.query.filter_by(reserva_id=reserva.id).first():
            return None, "Esta reserva ya tiene un pago registrado"
        
        # Calcular comisión (ejemplo: 10%)
        comision = reserva.monto_total * 0.1
        monto_propietario = reserva.monto_total - comision
        
        # Simular integración con pasarela de pago (fuera de alcance)
        # Aquí iría el código para la integración real
        referencia_externa = f"PAYMENT-{uuid.uuid4()}"
        
        # Registrar pago
        pago = Pago(
            reserva_id=reserva.id,
            monto=reserva.monto_total,
            comision=comision,
            monto_propietario=monto_propietario,
            metodo_pago=metodo_pago,
            estado='completado',
            referencia_externa=referencia_externa
        )
        
        # Actualizar estado de la reserva
        reserva.estado = 'pagado'
        
        db.session.add(pago)
        db.session.commit()
        
        return pago, None
    
    @staticmethod
    def get_pago_by_reserva(reserva_id):
        return Pago.query.filter_by(reserva_id=reserva_id).first()
    
    @staticmethod
    def get_pagos_by_cliente(cliente_id):
        # Obtener todos los pagos asociados a las reservas del cliente
        pagos = Pago.query.join(Reserva).filter(Reserva.cliente_id == cliente_id).all()
        return pagos
    
    @staticmethod
    def get_pagos_by_owner(owner_id):
        # Obtener todas las cocheras del propietario
        cocheras_ids = [c.id for c in Cochera.query.filter_by(owner_id=owner_id).all()]
        
        if not cocheras_ids:
            return []
        
        # Obtener pagos asociados a reservas en esas cocheras
        pagos = Pago.query.join(Reserva).filter(Reserva.cochera_id.in_(cocheras_ids)).all()
        return pagos