# app/__init__.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import datetime

# 1. Inicializa las extensiones SIN importar nada de nuestra app todavía
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 2. Vincula las extensiones a la instancia de la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # 3. Importa los modelos y las rutas DESPUÉS de que 'db' y 'app' estén listos
    from . import routes, models
    
    @app.context_processor
    def inject_global_vars():
        """ Inyecta variables globales en todas las plantillas. """
        # Ahora podemos usar 'models.Setting' de forma segura
        try:
            settings = models.Setting.query.all()
            app_settings = {setting.key: setting.value for setting in settings}
        except Exception:
            app_settings = {'LOGO_FILENAME': 'default_logo.png', 'NOMBRE_COLEGIO': 'Control de Almuerzos'}

        return {
            'now': datetime.utcnow,
            'app_settings': app_settings
        }

    # 4. Registra el Blueprint
    app.register_blueprint(routes.bp)
    
    return app