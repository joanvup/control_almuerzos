import os
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # --- Claves y Configuraciones Generales ---
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-de-desarrollo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- Configuración de la Base de Datos (Dinámica) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Parsea la URL de la BD para obtener los componentes individuales si no es SQLite
    DB_CONFIG = None
    if SQLALCHEMY_DATABASE_URI and 'mysql' in SQLALCHEMY_DATABASE_URI:
        try:
            url_object = make_url(SQLALCHEMY_DATABASE_URI)
            DB_CONFIG = {
                'user': url_object.username,
                'password': url_object.password,
                'host': url_object.host,
                'port': url_object.port,
                'database': url_object.database
            }
        except Exception:
            # En caso de que la URL no se pueda parsear, DB_CONFIG será None
            pass

    # --- Configuraciones de Rutas (Paths) ---
    # Carpeta para subir archivos de fotos, logos, etc.
    UPLOAD_FOLDER = 'app/static/uploads'
    
    # Carpeta para almacenar los backups de la base de datos
    BACKUP_FOLDER = os.path.join(basedir, 'backups')

    # --- Lógica de Compatibilidad para SQLite (Si alguna vez se usa en desarrollo) ---
    # La variable DB_PATH solo es relevante para backups de SQLite.
    DB_PATH = None
    if SQLALCHEMY_DATABASE_URI and 'sqlite' in SQLALCHEMY_DATABASE_URI:
        DB_PATH = SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')