from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validación básica
    if not all(k in data for k in ('username', 'email', 'password', 'user_type')):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    user, error = AuthService.register_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        user_type=data['user_type'],
        phone=data.get('phone')
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Se requiere email y contraseña'}), 400
    
    result, error = AuthService.login_user(data['email'], data['password'])
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({
        'access_token': result['access_token'],
        'user': result['user'].to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    user, error = AuthService.update_user(current_user_id, data)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Perfil actualizado exitosamente',
        'user': user.to_dict()
    }), 200