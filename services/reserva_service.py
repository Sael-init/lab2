from app import db
from app.models.reserva import Reserva
from app.models.cochera import Cochera
from datetime import datetime
from sqlalchemy import and_, or_

class ReservaService:
    @staticmethod
    def get_reservas_by_user(user_id, user_type, filters=None):
        query_filters = []
        
        # Si es cliente, mostrar sus reservas
        if user_type == 'cliente':
            query_filters.append(Reserva.cliente_id == user_id)
        
        # Si es propietario, mostrar reservas en sus cocheras
        elif user_type == 'owner':
            # Primero obtenemos las cocheras del propietario
            cocheras_ids = [c.id for c in Cochera.query.filter_by(owner_id=user_id).all()]
            if not cocheras_ids:
                return []
            
            query_filters.append(Reserva.cochera_id.in_(cocheras_ids))
        
        # Aplicar filtros adicionales
        if filters:
            if 'estado' in filters and filters['estado']:
                query_filters.append(Reserva.estado == filters['estado'])
            
            if 'fecha_inicio' in filters and filters['fecha_inicio']:
                try:
                    fecha_inicio_obj = datetime.fromisoformat(filters['fecha_inicio'])
                    query_filters.append(Reserva.fecha_inicio >= fecha_inicio_obj)
                except ValueError:
                    pass
            
            if 'fecha_fin' in filters and filters['fecha_fin']:
                try:
                    fecha_fin_obj = datetime.fromisoformat(filters['fecha_fin'])
                    query_filters.append(Reserva.fecha_fin <= fecha_fin_obj)
                except ValueError:
                    pass
        
        return Reserva.query.filter(and_(*query_filters)).all()
    
    @staticmethod
    def get_reserva_by_id(reserva_id):
        return Reserva.query.get(reserva_id)
    
    @staticmethod
    def create_reserva(cliente_id, cochera_id, fecha_inicio, fecha_fin):
        try:
            fecha_inicio_obj = datetime.fromisoformat(fecha_inicio)
            fecha_fin_obj = datetime.fromisoformat(fecha_fin)
        except ValueError:
            return None, "Formato de fecha inválido"
        
        # Validar fechas
        if fecha_inicio_obj >= fecha_fin_obj:
            return None, "La fecha de inicio debe ser anterior a la fecha de fin"
        
        if fecha_inicio_obj < datetime.now():
            return None, "La fecha de inicio debe ser futura"
        
        # Verificar disponibilidad de la cochera
        cochera = Cochera.query.get(cochera_id)
        if not cochera:
            return None, "Cochera no encontrada"
        
        if not cochera.disponible:
            return None, "Esta cochera no está disponible"
        
        # Verificar si ya existe una reserva para ese periodo
        conflicto = Reserva.query.filter(
            Reserva.cochera_id == cochera_id,
            Reserva.estado.in_(['pendiente', 'confirmado']),
            or_(
                and_(Reserva.fecha_inicio <= fecha_inicio_obj, Reserva.fecha_fin > fecha_inicio_obj),
                and_(Reserva.fecha_inicio < fecha_fin_obj, Reserva.fecha_fin >= fecha_fin_obj),
                and_(Reserva.fecha_inicio >= fecha_inicio_obj, Reserva.fecha_fin <= fecha_fin_obj)
            )
        ).first()
        
        if conflicto:
            return None, "Ya existe una reserva para ese periodo"
        
        # Calcular monto total
        duracion_horas = (fecha_fin_obj - fecha_inicio_obj).total_seconds() / 3600
        monto_total = duracion_horas * cochera.precio_hora
        
        # Crear reserva
        reserva = Reserva(
            cliente_id=cliente_id,
            cochera_id=cochera_id,
            fecha_inicio=fecha_inicio_obj,
            fecha_fin=fecha_fin_obj,
            estado='pendiente',
            monto_total=monto_total
        )
        
        db.session.add(reserva)
        db.session.commit()
        
        return reserva, None
    
    @staticmethod
    def update_reserva_status(reserva_id, estado, user_id, user_type):
        reserva = Reserva.query.get(reserva_id)
        
        if not reserva:
            return None, "Reserva no encontrada"
        
        # Verificar permisos según el tipo de usuario
        if user_type == 'cliente':
            if reserva.cliente_id != user_id:
                return None, "No autorizado para modificar esta reserva"
            
            # Cliente solo puede cancelar
            if estado != 'cancelado':
                return None, "Cliente solo puede cancelar reservas"
        
        elif user_type == 'owner':
            cochera = Cochera.query.get(reserva.cochera_id)
            if not cochera or cochera.owner_id != user_id:
                return None, "No autorizado para modificar esta reserva"
            
            # Propietario solo puede confirmar o cancelar
            if estado not in ['confirmado', 'cancelado']:
                return None, "Propietario solo puede confirmar o cancelar reservas"
        
        # Actualizar estado
        reserva.estado = estado
        db.session.commit()
        
        return reserva, None
    
    @staticmethod
    def delete_reserva(reserva_id, cliente_id):
        reserva = Reserva.query.get(reserva_id)
        
        if not reserva or reserva.cliente_id != cliente_id:
            return False, "Reserva no encontrada o no autorizado"
        
        # Solo se pueden eliminar reservas pendientes
        if reserva.estado != 'pendiente':
            return False, "Solo se pueden eliminar reservas pendientes"
        
        db.session.delete(reserva)
        db.session.commit()
        
        return True, None   