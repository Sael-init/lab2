from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.cochera import Cochera
from app import db

cocheras_bp = Blueprint('cocheras', __name__)

@cocheras_bp.route('/search', methods=['GET'])
def search_cocheras():
    query = request.args.get('q', '')
    distrito = request.args.get('distrito')
    disponible = request.args.get('disponible', 'true').lower() == 'true'
    
    filters = []
    
    if disponible:
        filters.append(Cochera.disponible == True)
    
    if distrito:
        filters.append(Cochera.distrito == distrito)
    
    cocheras = Cochera.query.filter(*filters).all()
    
    return jsonify({
        'cocheras': [c.to_dict() for c in cocheras]
    }), 200

@cocheras_bp.route('/manageCocheras', methods=['GET'])
@jwt_required()
def get_cocheras():
    current_user_id = get_jwt_identity()
    cocheras = Cochera.query.filter_by(owner_id=current_user_id).all()
    
    return jsonify({
        'cocheras': [c.to_dict() for c in cocheras]
    }), 200

@cocheras_bp.route('/manageCocheras', methods=['POST'])
@jwt_required()
def create_cochera():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    cochera = Cochera(
        owner_id=current_user_id,
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        direccion=data['direccion'],
        distrito=data['distrito'],
        precio_hora=float(data['precio_hora']),
        disponible=data.get('disponible', True),
        latitud=data.get('latitud'),
        longitud=data.get('longitud')
    )
    
    db.session.add(cochera)
    db.session.commit()
    
    return jsonify({
        'message': 'Cochera creada exitosamente',
        'cochera': cochera.to_dict()
    }), 201

@cocheras_bp.route('/manageCocheras', methods=['PATCH'])
@jwt_required()
def update_cochera():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    cochera_id = data.get('id')
    
    if not cochera_id:
        return jsonify({'error': 'Se requiere el ID de la cochera'}), 400
        
    cochera = Cochera.query.get(cochera_id)
    
    if not cochera or cochera.owner_id != current_user_id:
        return jsonify({'error': 'Cochera no encontrada o no autorizado'}), 404
    
    # Actualizar campos
    updatable_fields = ['titulo', 'descripcion', 'direccion', 'distrito', 
                        'precio_hora', 'disponible', 'latitud', 'longitud']
    
    for field in updatable_fields:
        if field in data:
            setattr(cochera, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Cochera actualizada exitosamente',
        'cochera': cochera.to_dict()
    }), 200

@cocheras_bp.route('/manageCocheras', methods=['DELETE'])
@jwt_required()
def delete_cochera():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    cochera_id = data.get('id')
    
    if not cochera_id:
        return jsonify({'error': 'Se requiere el ID de la cochera'}), 400
        
    cochera = Cochera.query.get(cochera_id)
    
    if not cochera or cochera.owner_id != current_user_id:
        return jsonify({'error': 'Cochera no encontrada o no autorizado'}), 404
    
    db.session.delete(cochera)
    db.session.commit()
    
    return jsonify({
        'message': 'Cochera eliminada exitosamente'
    }), 200