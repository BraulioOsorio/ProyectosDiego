from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError,jwt
from Core.config import settings

# Configurar hashing de contraselas
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# Funcion para generar un hash_passw

def get_hashed_password(password :str):
    return pwd_context.hash(password)

# Funcion para verificar una contraseña hashada
def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

# funcion par crear un token JWT
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MIN)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encode_jwt

async def verify_token(token:str):
    try:
        paylaod = jwt.decode(token,settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user : str = paylaod.get("sub") #obtener el identificador de usuario
        return user
    except jwt.ExpiredSignatureError: #Token ha expirado
        return None
    except JWTError:
        return None

