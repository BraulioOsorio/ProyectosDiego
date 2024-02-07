from passlib.context import CryptContext

# Configurar hashing de contraselas
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# Funcion para generar un hash_passw

def get_hashed_password(password :str):
    return pwd_context.hash(password)

# Funcion para verificar una contraseña hashada
def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)