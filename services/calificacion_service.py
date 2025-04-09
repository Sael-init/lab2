from app import db
from app.models.calificacion import Calificacion
from app.models.reserva import Reserva

class CalificacionService:
    @staticmethod
    def get_calificaciones_by_cochera(cochera_id):
        return Calificacion.query.filter_by(cochera_id=cochera_id).all()
    
    @staticmethod
    def get_calificacion_by_id(calificacion_id):
        return Calificacion.query.get(calificacion_id)
    
    @staticmethod
    def create_calificacion(autor_id, cochera_id, puntuacion, comentario=None):
        # Verificar que el usuario haya tenido una reserva completada en esta cochera
        has_reserva = Reserva.query.filter_by(
            cliente_id=autor_id,
            cochera_id=cochera_id,
            estado='completado'
        ).first()
        
        if not has_reserva:
            return None, "Solo pueden calificar usuarios que hayan utilizado la cochera"
        
        # Verificar que no haya calificado previamente esta cochera
        prev_review = Calificacion.query.filter_by(
            autor_id=autor_id,
            cochera_id=cochera_id
        ).first()
        
        if prev_review:
            return None, "Ya has calificado esta cochera anteriormente"
        
        # Validar puntuación
        if not 1 <= puntuacion <= 5:
            return None, "La puntuación debe estar entre 1 y 5"
        
        calificacion = Calificacion(
            autor_id=autor_id,
            cochera_id=cochera_id,
            puntuacion=puntuacion,
            comentario=comentario or ''
        )
        
        db.session.add(calificacion)
        db.session.commit()
        
        return calificacion, None
    
    @staticmethod
    def update_calificacion(calificacion_id, autor_id, data):
        calificacion = Calificacion.query.get(calificacion_id)
        
        if not calificacion or calificacion.autor_id != autor_id:
            return None, "Calificación no encontrada o no autorizado"
        
        # Actualizar puntuación si se proporciona
        if 'puntuacion' in data:
            if not 1 <= data['puntuacion'] <= 5:
                return None, "La puntuación debe estar entre 1 y 5"
            calificacion.puntuacion = data['puntuacion']
        
        # Actualizar comentario si se proporciona
        if 'comentario' in data:
            calificacion.comentario = data['comentario']
        
        db.session.commit()
        
        return calificacion, None
    
    @staticmethod
    def delete_calificacion(calificacion_id, autor_id):
        calificacion = Calificacion.query.get(calificacion_id)
        
        if not calificacion or calificacion.autor_id != autor_id:
            return False, "Calificación no encontrada o no autorizado"
        
        db.session.delete(calificacion)
        db.session.commit()
        
        return True, None
    
    @staticmethod
    def get_promedio_calificaciones(cochera_id):
        calificaciones = Calificacion.query.filter_by(cochera_id=cochera_id).all()
        
        if not calificaciones:
            return 0
        
        total = sum(c.puntuacion for c in calificaciones)
        return total / len(calificaciones)