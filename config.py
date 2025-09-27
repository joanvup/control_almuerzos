import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # === INICIO DE LA LÓGICA DE BD FLEXIBLE ===
    # 1. Por defecto, usa la URL de la base de datos del entorno (para producción en Render)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # 2. Si no se encuentra, construye la ruta para SQLite (para desarrollo local)
    if not SQLALCHEMY_DATABASE_URI:
        INSTANCE_FOLDER_PATH = os.path.join(basedir, 'instance')
        if not os.path.exists(INSTANCE_FOLDER_PATH):
            os.makedirs(INSTANCE_FOLDER_PATH)
        db_name = 'almuerzos.db'
        DB_PATH = os.path.join(INSTANCE_FOLDER_PATH, db_name)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_PATH
    # 3. Lógica para la ruta de backup de SQLite (solo se define si usamos SQLite)
    DB_PATH = None
    if 'sqlite' in SQLALCHEMY_DATABASE_URI:
        DB_PATH = SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    # === FIN DE LA LÓGICA DE BD FLEXIBLE ===
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Opción para imprimir tickets
    IMPRIME_TICKETS = os.environ.get('IMPRIME_TICKETS', 'True').lower() in ['true', '1', 't']

    # Carpeta para subir archivos
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    
    # Nombre del colegio para los tickets
    NOMBRE_COLEGIO = "Fundación Colegio Bilingüe de Valledupar"
    # Ruta a la carpeta de backups
    BACKUP_FOLDER = os.path.join(basedir, 'backups')
    # Extraer la ruta del archivo de la URI de la base de datos
    # DB_PATH = SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')

    # === INICIO DE LA SOLUCIÓN ===
    # Construir la ruta absoluta y robusta al archivo de la base de datos
    # 1. Obtener solo el nombre del archivo de la URI
    db_filename = SQLALCHEMY_DATABASE_URI.split('/')[-1]
    # 2. Unirlo con la ruta base del proyecto para obtener la ruta absoluta
    DB_PATH = os.path.join(basedir, db_filename)
    # === FIN DE LA SOLUCIÓN ====