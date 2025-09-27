from app import create_app, db
from app.models import Usuario, Rol, TipoPersona, TipoControl, Dpto, Setting

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Usuario': Usuario, 'Rol': Rol}

# Con el contexto de la aplicación, creamos los roles iniciales y el admin si no existen.
with app.app_context():
    db.create_all()
    if Rol.query.filter_by(nombre='Administrador').first() is None:
        print("Creando rol Administrador...")
        rol_admin = Rol(nombre='Administrador')
        db.session.add(rol_admin)
    if Rol.query.filter_by(nombre='Operador').first() is None:
        print("Creando rol Operador...")
        rol_op = Rol(nombre='Operador')
        db.session.add(rol_op)
    db.session.commit()

    if Usuario.query.filter_by(username='admin').first() is None:
        print("Creando usuario administrador por defecto...")
        from app import bcrypt
        admin_role = Rol.query.filter_by(nombre='Administrador').first()
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        admin_user = Usuario(username='admin', password=hashed_password, rol=admin_role)
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario 'admin' con contraseña 'admin' creado.")
        
    # Datos iniciales para que la app sea funcional desde el inicio
    if Dpto.query.count() == 0:
        db.session.add(Dpto(nombre_dpto='Administración'))
        db.session.add(Dpto(nombre_dpto='Primaria'))
        db.session.add(Dpto(nombre_dpto='Secundaria'))
    if TipoPersona.query.count() == 0:
        db.session.add(TipoPersona(nombre_tipopersona='Estudiante'))
        db.session.add(TipoPersona(nombre_tipopersona='Docente'))
        db.session.add(TipoPersona(nombre_tipopersona='Personal Adm.'))
    if TipoControl.query.count() == 0:
        db.session.add(TipoControl(nombre_control='Almuerzo Regular'))
        db.session.add(TipoControl(nombre_control='Dieta Especial'))
    db.session.commit()
    # Crear la configuración inicial si no existe
    # Lista de configuraciones por defecto
    default_settings = {
        'IMPRIME_TICKETS': 'True',
        'NOMBRE_COLEGIO': "Colegio Privado 'El Inge'",
        'LOGO_FILENAME': 'default_logo.png' # Un logo por defecto
    }

    for key, value in default_settings.items():
        if Setting.query.filter_by(key=key).first() is None:
            print(f"Creando configuración: {key}...")
            setting = Setting(key=key, value=value)
            db.session.add(setting)
    
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)