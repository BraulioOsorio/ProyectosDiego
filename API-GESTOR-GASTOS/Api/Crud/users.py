import sys

from fastapi.responses import JSONResponse # Mandar mensajes de error al log

from Api.Models.User import User
from fastapi import HTTPException
from Api.Schemas.users import UserCreate,UserRead,UserUpdateAdmin
from sqlalchemy.orm import Session
from Core.security import get_hashed_password,verify_password
from Core.utils import generate_user_id


def create_new_user(user:UserCreate,db:Session,rol:str):
    db_user = User(
        user_id = generate_user_id(),
        full_name = user.full_name,
        mail = user.mail,
        passhash = get_hashed_password(user.passhash),
        user_role = rol,
        user_status = user.user_status
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return db_user
    except Exception as e :
        db.rollback()
        # Imprimir el error en la consola
        print(f"Error al crear un usuario: {str(e)}",file=sys.stderr)
        raise HTTPException(status_code=500,detail=f"Error al crear usuario: {str(e)} ")

def get_user_by_email(email:str,db:Session):
    user = db.query(User).filter(User.mail == email).first()
    return user

def get_user_by_email_update(user_id : str,email : str,db :Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user.mail != email:
        verify_user = get_user_by_email(email,db)
        if verify_user is None:
            return True
        return False
    return True

def get_users_rol(rolUserToken : str,user_id : str ,db : Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user.user_role == rolUserToken:
        return False
    return True

    
def get_user_by_id(id:str,db:Session):
    user = db.query(User).filter(User.user_id == id).first()
    return user

def authenticate_user(username:str, password : str,db : Session):
    user = get_user_by_email(username,db)
    if not user:
        return False
    if not verify_password(password,user.passhash):
        return False
    return user

def update_user_exist(user:UserUpdateAdmin,db:Session,rol:str):
    user_db = db.query(User).filter(User.user_id == user.user_id).first()
    if not user_db:
        raise HTTPException(status_code=401,detail="The user not Exist")

    user_db.full_name = user.full_name
    user_db.mail = user.mail
    user_db.passhash = get_hashed_password(user.passhash)
    user_db.user_status = user.user_status
    user_db.user_role = rol
    try:
        db.commit()
        db.close()
        return JSONResponse(content={"message": "Item updated successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="Error a actualiar usuario")
