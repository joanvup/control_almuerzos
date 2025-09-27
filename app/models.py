from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)

# --- Tablas de la aplicación ---

class Dpto(db.Model):
    __tablename__ = 'dptos'
    id_dpto = db.Column(db.Integer, primary_key=True)
    nombre_dpto = db.Column(db.String(100), unique=True, nullable=False)
    personas = db.relationship('Persona', backref='dpto_ref', lazy=True)

class TipoControl(db.Model):
    __tablename__ = 'tipo_control'
    id_control = db.Column(db.Integer, primary_key=True)
    nombre_control = db.Column(db.String(100), unique=True, nullable=False)
    personas = db.relationship('Persona', backref='control_ref', lazy=True)
    registros = db.relationship('Registro', backref='tipo_control_ref', lazy=True)

class TipoPersona(db.Model):
    __tablename__ = 'tipos_persona'
    id_tipopersona = db.Column(db.Integer, primary_key=True)
    nombre_tipopersona = db.Column(db.String(100), unique=True, nullable=False)
    personas = db.relationship('Persona', backref='tipo_persona_ref', lazy=True)

class Persona(db.Model):
    __tablename__ = 'personas'
    # Usamos un String para id_persona ya que puede ser un código alfanumérico
    id_persona = db.Column(db.String(20), primary_key=True, unique=True)
    nombre_persona = db.Column(db.String(150), nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    foto = db.Column(db.String(120), nullable=True, default='default.jpg')

    # Llaves foráneas
    tipo_persona_id = db.Column(db.Integer, db.ForeignKey('tipos_persona.id_tipopersona'), nullable=False)
    dpto_id = db.Column(db.Integer, db.ForeignKey('dptos.id_dpto'), nullable=False)
    control_id = db.Column(db.Integer, db.ForeignKey('tipo_control.id_control'), nullable=False)
    
    registros = db.relationship('Registro', backref='persona_ref', lazy=True)

class Registro(db.Model):
    __tablename__ = 'registros'
    id_registro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_hora_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Llaves foráneas
    persona_id = db.Column(db.String(20), db.ForeignKey('personas.id_persona'), nullable=False)
    tipo_control_id = db.Column(db.Integer, db.ForeignKey('tipo_control.id_control'), nullable=False)

# app/models.py

# ... (tus otros modelos) ...

class Setting(db.Model):
    __tablename__ = 'settings'
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(255), nullable=False)