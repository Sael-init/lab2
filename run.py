from app import create_app, db

app = create_app()

# Opcionalmente, puedes crear las tablas directamente si no usas migraciones
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)