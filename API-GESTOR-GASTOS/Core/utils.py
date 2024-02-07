import secrets
import string

# Funcion para generar un ID de usuario aleatorio
def generate_user_id(length = 30):
    # Caracteres posibles para le ID aleatorio
    characteres = string.ascii_letters + string.digits

    # Genera un ID aleatorio de la longitud deseada
    random_id = ''.join(secrets.choice(characteres) for _ in range(length))

    return random_id