from app import db
from app.models.cochera import Cochera
from sqlalchemy import or_

class CocheraService:
    @staticmethod
    def get_all_cocheras(filters=None):
        query = Cochera.query
        
        if filters:
            if 'distrito' in filters and filters['distrito']:
                query = query.filter(Cochera.distrito == filters['distrito'])
            
            if 'disponible' in filters:
                query = query.filter(Cochera.disponible == filters['disponible'])
        
        return query.all()
    
    @staticmethod
    def get_cochera_by_id(cochera_id):
        return Cochera.query.get(cochera_id)
    
    @staticmethod
    def get_cocheras_by_owner(owner_id):
        return Cochera.query.filter_by(owner_id=owner_id).all()
    
    @staticmethod
    def create_cochera(data, owner_id):
        cochera = Cochera(
            owner_id=owner_id,
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
        
        return cochera
    
    @staticmethod
    def update_cochera(cochera_id, data, owner_id):
        cochera = Cochera.query.get(cochera_id)
        
        if not cochera or cochera.owner_id != owner_id:
            return None, "Cochera no encontrada o no autorizado"
        
        # Campos permitidos para actualizar
        updatable_fields = ['titulo', 'descripcion', 'direccion', 'distrito', 
                           'precio_hora', 'disponible', 'latitud', 'longitud']
        
        for field in updatable_fields:
            if field in data:
                setattr(cochera, field, data[field])
        
        db.session.commit()
        return cochera, None
    
    @staticmethod
    def delete_cochera(cochera_id, owner_id):
        cochera = Cochera.query.get(cochera_id)
        
        if not cochera or cochera.owner_id != owner_id:
            return False, "Cochera no encontrada o no autorizado"
        
        # Verificar si tiene reservas activas
        active_reservas = any(r.estado in ['pendiente', 'confirmado'] for r in cochera.reservas)
        if active_reservas:
            return False, "No se puede eliminar una cochera con reservas activas"
        
        db.session.delete(cochera)
        db.session.commit()
        
        return True, None
    
    @staticmethod
    def search_cocheras(query_text=None, distrito=None, disponible=True):
        filters = []
        
        if disponible:
            filters.append(Cochera.disponible == True)
        
        if distrito:
            filters.append(Cochera.distrito == distrito)
        
        if query_text:
            search_filter = or_(
                Cochera.titulo.ilike(f'%{query_text}%'),
                Cochera.descripcion.ilike(f'%{query_text}%'),
                Cochera.direccion.ilike(f'%{query_text}%')
            )
            filters.append(search_filter)
        
        return Cochera.query.filter(*filters).all()