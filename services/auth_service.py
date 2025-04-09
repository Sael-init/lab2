from app import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token
import datetime

class AuthService:
    @staticmethod
    def register_user(username, email, password, user_type, phone=None):
        # Verificar si el usuario ya existe
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            return None, "El usuario o email ya está registrado"
        
        # Crear nuevo usuario
        user = User(
            username=username,
            email=email,
            user_type=user_type,
            phone=phone
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, None
    
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return None, "Credenciales inválidas"
        
        if not user.is_active:
            return None, "Cuenta desactivada"
        
        # Generar token JWT
        access_token = create_access_token(identity=user.id)
        
        return {"user": user, "access_token": access_token}, None
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuario no encontrado"
        
        # Actualizar campos permitidos
        if 'username' in data:
            user.username = data['username']
        
        if 'phone' in data:
            user.phone = data['phone']
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        return user, None