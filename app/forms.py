from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField 
from app.models import Usuario, Dpto, TipoControl, TipoPersona, Rol, Persona

# --- Funciones para llenar los combos (SelectField) ---
def get_dptos():
    return Dpto.query.all()

def get_tipos_persona():
    return TipoPersona.query.all()

def get_tipos_control():
    return TipoControl.query.all()

def get_roles():
    return Rol.query.all()


# --- Formularios de la App ---
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')


class DptoForm(FlaskForm):
    id_dpto = HiddenField()
    nombre_dpto = StringField('Nombre del Departamento', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Guardar')
    # === AÑADE ESTA FUNCIÓN DE VALIDACIÓN ===
    def validate_nombre_dpto(self, nombre_dpto):
        # Si estamos editando (el campo id_dpto tiene un valor)
        if self.id_dpto.data:
            dpto = Dpto.query.filter_by(nombre_dpto=nombre_dpto.data).first()
            # Si se encuentra un dpto con ese nombre Y su ID es diferente al que estamos editando, es un duplicado.
            if dpto and dpto.id_dpto != int(self.id_dpto.data):
                raise ValidationError('Ese nombre de departamento ya existe. Por favor, elige otro.')
        else: # Si estamos creando (el campo id_dpto está vacío)
            if Dpto.query.filter_by(nombre_dpto=nombre_dpto.data).first():
                raise ValidationError('Ese nombre de departamento ya existe. Por favor, elige otro.')

class TipoControlForm(FlaskForm):
    id_control = HiddenField()
    nombre_control = StringField('Nombre del Tipo de Control', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Guardar')
    # === AÑADE ESTA FUNCIÓN DE VALIDACIÓN ===
    def validate_nombre_control(self, nombre_control):
        if self.id_control.data:
            item = TipoControl.query.filter_by(nombre_control=nombre_control.data).first()
            if item and item.id_control != int(self.id_control.data):
                raise ValidationError('Ese tipo de control ya existe.')
        else:
            if TipoControl.query.filter_by(nombre_control=nombre_control.data).first():
                raise ValidationError('Ese tipo de control ya existe.')

class TipoPersonaForm(FlaskForm):
    id_tipopersona = HiddenField()
    nombre_tipopersona = StringField('Nombre del Tipo de Persona', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Guardar')
    # === AÑADE ESTA FUNCIÓN DE VALIDACIÓN ===
    def validate_nombre_tipopersona(self, nombre_tipopersona):
        if self.id_tipopersona.data:
            item = TipoPersona.query.filter_by(nombre_tipopersona=nombre_tipopersona.data).first()
            if item and item.id_tipopersona != int(self.id_tipopersona.data):
                raise ValidationError('Ese tipo de persona ya existe.')
        else:
            if TipoPersona.query.filter_by(nombre_tipopersona=nombre_tipopersona.data).first():
                raise ValidationError('Ese tipo de persona ya existe.')
    
class PersonaForm(FlaskForm):
    id_persona = StringField('Código / ID', validators=[DataRequired(), Length(min=1, max=20)])
    nombre_persona = StringField('Nombre Completo', validators=[DataRequired(), Length(min=3, max=150)])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')], validators=[DataRequired()])
    dpto = QuerySelectField('Departamento', query_factory=get_dptos, get_label='nombre_dpto', allow_blank=False, validators=[DataRequired()])
    tipo_persona = QuerySelectField('Tipo de Persona', query_factory=get_tipos_persona, get_label='nombre_tipopersona', allow_blank=False, validators=[DataRequired()])
    control = QuerySelectField('Tipo de Control Asignado', query_factory=get_tipos_control, get_label='nombre_control', allow_blank=False, validators=[DataRequired()])
    foto = FileField('Foto (Opcional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    foto_webcam = HiddenField('Foto de Webcam')
    submit = SubmitField('Guardar Persona')
    
    # Validar que el id_persona sea único al crear
    def validate_id_persona(self, id_persona):
        # Esta validación solo aplica para nuevos registros. Para editar, necesitamos un truco.
        # Por ahora, lo dejamos así, y la lógica de la ruta manejará la edición.
        if Persona.query.get(id_persona.data):
            raise ValidationError('Ese código ya está registrado. Por favor, elige otro.')


class UsuarioForm(FlaskForm):
    id = HiddenField()
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contraseña', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[EqualTo('password')])
    rol = QuerySelectField('Rol', query_factory=get_roles, get_label='nombre', allow_blank=False, validators=[DataRequired()])
    submit = SubmitField('Guardar Usuario')

    # === REEMPLAZA ESTA FUNCIÓN COMPLETA ===
    def validate_username(self, username):
        # Primero, buscamos si ya existe un usuario con ese nombre
        user = Usuario.query.filter_by(username=username.data).first()
        
        # Si se encontró un usuario, debemos determinar si es un conflicto
        if user:
            # Si estamos CREANDO un nuevo usuario (el campo ID está vacío),
            # entonces cualquier usuario encontrado es un duplicado.
            print("1-us1: ",self.id.data)
            print("1-us2: ",user.id)
            if not user.id:
                raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige otro.')
            
            # Si estamos EDITANDO (el campo ID tiene un valor),
            # solo es un error si el ID del usuario encontrado es DIFERENTE
            # al ID del usuario que estamos editando.
            print("2-us1: ",self.id.data)
            print("2-us2: ",user.id)
            
            if self.id.data and user.id != int(self.id.data):
                raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige otro.')