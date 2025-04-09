from flask import Blueprint, request, jsonify
from app.models.cochera import Cochera
from sqlalchemy import func

geo_bp = Blueprint('geolocalizacion', __name__)

@geo_bp.route('/geolocalization', methods=['GET'])
def get_geolocalization():
    # Obtener parámetros
    distrito = request.args.get('distrito')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    
    # Base query
    query = Cochera.query.filter(Cochera.disponible == True)
    
    # Filtrar por distrito si se proporciona
    if distrito:
        query = query.filter(Cochera.distrito == distrito)
    
    # Si se proporcionan coordenadas, ordenar por cercanía
    if lat and lng:
        try:
            lat_float = float(lat)
            lng_float = float(lng)
            
            # Cálculo de distancia usando fórmula de Haversine (aproximada)
            # Nota: En una implementación real, considerar usar PostGIS o similar
            distance = func.sqrt(
                func.pow(69.1 * (Cochera.latitud - lat_float), 2) +
                func.pow(69.1 * (lng_float - Cochera.longitud) * func.cos(Cochera.latitud / 57.3), 2)
            )
            
            query = query.order_by(distance)
        except ValueError:
            # Si las coordenadas no son válidas, ignorar
            pass
    
    # Obtener cocheras
    cocheras = query.all()
    
    return jsonify({
        'cocheras': [
            {
                **c.to_dict(),
                'location': {
                    'lat': c.latitud,
                    'lng': c.longitud
                } if c.latitud and c.longitud else None
            } for c in cocheras
        ]
    }), 200