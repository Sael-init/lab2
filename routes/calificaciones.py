from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.calificacion import Calificacion
from app.models.reserva import Reserva
from app import db

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/review', methods=['GET'])
def get_reviews():
    cochera_id = request.args.get('cochera_id')
    
    if not cochera_id:
        return jsonify({'error': 'Se requiere ID de cochera'}), 400
    
    calificaciones = Calificacion.query.filter_by(cochera_id=cochera_id).all()
    
    return jsonify({
        'reviews': [c.to_dict() for c in calificaciones]
    }), 200

@calificaciones_bp.route('/review', methods=['POST'])
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Verificar que el usuario haya tenido una reserva completada en esta cochera
    has_reserva = Reserva.query.filter_by(
        cliente_id=current_user_id,
        cochera_id=data['cochera_id'],
        estado='completado'
    ).first()
    
    if not has_reserva:
        return jsonify({'error': 'Solo pueden calificar usuarios que hayan utilizado la cochera'}), 403
    
    # Verificar que no haya calificado previamente esta cochera
    prev_review = Calificacion.query.filter_by(
        autor_id=current_user_id,
        cochera_id=data['cochera_id']
    ).first()
    
    if prev_review:
        return jsonify({'error': 'Ya has calificado esta cochera anteriormente'}), 400
    
    # Validar puntuación
    if not 1 <= data['puntuacion'] <= 5:
        return jsonify({'error': 'La puntuación debe estar entre 1 y 5'}), 400
    
    calificacion = Calificacion(
        autor_id=current_user_id,
        cochera_id=data['cochera_id'],
        puntuacion=data['puntuacion'],
        comentario=data.get('comentario', '')
    )
    
    db.session.add(calificacion)
    db.session.commit()
    
    return jsonify({
        'message': 'Calificación creada exitosamente',
        'review': calificacion.to_dict()
    }), 201

@calificaciones_bp.route('/review', methods=['PATCH'])
@jwt_required()
def update_review():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('id'):
        return jsonify({'error': 'Se requiere ID de la calificación'}), 400
    
    calificacion = Calificacion.query.get(data['id'])
    
    if not calificacion or calificacion.autor_id != current_user_id:
        return jsonify({'error': 'Calificación no encontrada o no autorizado'}), 404
    
    # Actualizar puntuación si se proporciona
    if 'puntuacion' in data:
        if not 1 <= data['puntuacion'] <= 5:
            return jsonify({'error': 'La puntuación debe estar entre 1 y 5'}), 400
        calificacion.puntuacion = data['puntuacion']
    
    # Actualizar comentario si se proporciona
    if 'comentario' in data:
        calificacion.comentario = data['comentario']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Calificación actualizada exitosamente',
        'review': calificacion.to_dict()
    }), 200

@calificaciones_bp.route('/review', methods=['DELETE'])
@jwt_required()
def delete_review():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('id'):
        return jsonify({'error': 'Se requiere ID de la calificación'}), 400
    
    calificacion = Calificacion.query.get(data['id'])
    
    if not calificacion or calificacion.autor_id != current_user_id:
        return jsonify({'error': 'Calificación no encontrada o no autorizado'}), 404
    
    db.session.delete(calificacion)
    db.session.commit()
    
    return jsonify({
        'message': 'Calificación eliminada exitosamente'
    }), 200