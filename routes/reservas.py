from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.reserva import Reserva
from app.models.cochera import Cochera
from app import db
from datetime import datetime

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/manageReserva', methods=['POST'])
@jwt_required()
def create_reserva():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
    fecha_fin = datetime.fromisoformat(data['fecha_fin'])
    
    # Verificar disponibilidad de la cochera
    cochera = Cochera.query.get(data['cochera_id'])
    if not cochera or not cochera.disponible:
        return jsonify({'error': 'Cochera no disponible'}), 400
    
    # Calcular monto total
    duracion_horas = (fecha_fin - fecha_inicio).total_seconds() / 3600
    monto_total = duracion_horas * cochera.precio_hora
    
    # Crear reserva
    reserva = Reserva(
        cliente_id=current_user_id,
        cochera_id=data['cochera_id'],
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado='pendiente',
        monto_total=monto_total
    )
    
    db.session.add(reserva)
    db.session.commit()
    
    return jsonify({
        'message': 'Reserva creada exitosamente',
        'reserva': reserva.to_dict()
    }), 201

@reservas_bp.route('/manageReserva', methods=['PATCH'])
@jwt_required()
def update_reserva():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    reserva_id = data.get('id')
    
    if not reserva_id:
        return jsonify({'error': 'Se requiere el ID de la reserva'}), 400
        
    reserva = Reserva.query.get(reserva_id)
    
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404
    
    # Verificar si es el cliente o el dueño de la cochera
    is_client = reserva.cliente_id == current_user_id
    cochera = Cochera.query.get(reserva.cochera_id)
    is_owner = cochera and cochera.owner_id == current_user_id
    
    if not (is_client or is_owner):
        return jsonify({'error': 'No autorizado para modificar esta reserva'}), 403
    
    # Cliente solo puede cancelar, dueño puede confirmar o cancelar
    if 'estado' in data:
        if is_client and data['estado'] not in ['cancelado']:
            return jsonify({'error': 'Cliente solo puede cancelar reservas'}), 400
            
        if is_owner and data['estado'] not in ['confirmado', 'cancelado']:
            return jsonify({'error': 'Propietario solo puede confirmar o cancelar reservas'}), 400
            
        reserva.estado = data['estado']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Reserva actualizada exitosamente',
        'reserva': reserva.to_dict()
    }), 200

@reservas_bp.route('/manageReserva', methods=['DELETE'])
@jwt_required()
def delete_reserva():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    reserva_id = data.get('id')
    
    if not reserva_id:
        return jsonify({'error': 'Se requiere el ID de la reserva'}), 400
        
    reserva = Reserva.query.get(reserva_id)
    
    if not reserva or reserva.cliente_id != current_user_id:
        return jsonify({'error': 'Reserva no encontrada o no autorizado'}), 404
    
    # Solo se pueden eliminar reservas pendientes
    if reserva.estado != 'pendiente':
        return jsonify({'error': 'Solo se pueden eliminar reservas pendientes'}), 400
    
    db.session.delete(reserva)
    db.session.commit()
    
    return jsonify({
        'message': 'Reserva eliminada exitosamente'
    }), 200