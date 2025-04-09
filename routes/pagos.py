from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.pago import Pago
from app.models.reserva import Reserva
from app import db

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/payment', methods=['POST'])
@jwt_required()
def process_payment():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Verificar que la reserva existe y pertenece al usuario
    reserva = Reserva.query.get(data['reserva_id'])
    if not reserva or reserva.cliente_id != current_user_id:
        return jsonify({'error': 'Reserva no encontrada o no autorizada'}), 404
    
    # Verificar que la reserva esté confirmada
    if reserva.estado != 'confirmado':
        return jsonify({'error': 'Solo se pueden pagar reservas confirmadas'}), 400
    
    # Verificar que no haya un pago previo
    if Pago.query.filter_by(reserva_id=reserva.id).first():
        return jsonify({'error': 'Esta reserva ya tiene un pago registrado'}), 400
    
    # Calcular comisión (ejemplo: 10%)
    comision = reserva.monto_total * 0.1
    monto_propietario = reserva.monto_total - comision
    
    # Simular integración con pasarela de pago (fuera de alcance)
    # Aquí iría el código para la integración real
    referencia_externa = f"PAYMENT-{reserva.id}-{int(datetime.now().timestamp())}"
    
    # Registrar pago
    pago = Pago(
        reserva_id=reserva.id,
        monto=reserva.monto_total,
        comision=comision,
        monto_propietario=monto_propietario,
        metodo_pago=data.get('metodo_pago', 'tarjeta'),
        estado='completado',
        referencia_externa=referencia_externa
    )
    
    # Actualizar estado de la reserva
    reserva.estado = 'pagado'
    
    db.session.add(pago)
    db.session.commit()
    
    return jsonify({
        'message': 'Pago procesado exitosamente',
        'pago': pago.to_dict()
    }), 201