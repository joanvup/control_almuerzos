import qrcode
from io import BytesIO
import base64
import pytz # <-- Añadir esta importación

def generate_qr_code(data_string):
    """
    Genera un código QR a partir de una cadena de texto y lo devuelve como una imagen base64.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=1,
    )
    qr.add_data(data_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return f"data:image/png;base64,{img_str}"

# === INICIO DE NUEVA FUNCIÓN DE AYUDA ===
def convert_utc_to_local(utc_dt, timezone_str="America/Bogota"):
    """Convierte un objeto datetime de UTC a una zona horaria local."""
    if not utc_dt:
        return None
    try:
        local_tz = pytz.timezone(timezone_str)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_dt
    except Exception:
        # Si algo falla, devuelve la hora original para no romper la app
        return utc_dt
# === FIN DE NUEVA FUNCIÓN ===