from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import get_session
from Api.Schemas.users import UserCreate,UserRead,Token,UserCreateAdmin
from Api.Crud.users import *
from Core.security import create_access_token,verify_token

router = APIRouter()

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(token:str = Depends(oauth2_sheme),db : Session = Depends(get_session)):
    user_id = await verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401,detail="invalid token")
    user_db = get_user_by_id(user_id,db)
    if user_db is None:
        raise HTTPException(status_code=404,detail="User not fount")
    return user_db


@router.post("/create-user/",response_model=UserRead,)
async def create_user(user:UserCreate,db:Session = Depends(get_session)):
    verify_user = get_user_by_email(user.mail,db)
    if verify_user is None:
        return create_new_user(user,db,'user')
    
    raise HTTPException(status_code=404,detail="Email already exists")


@router.post("/create-user-admin/",response_model=UserRead,)
async def create_user(user:UserCreateAdmin,db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        verify_user = get_user_by_email(user.mail,db)
        if verify_user is None:
            return create_new_user(user,db,user.user_role)
        
        raise HTTPException(status_code=404,detail="Email already exists")
    raise HTTPException(status_code=404,detail="Not authorized")



@router.get("/get/{user_id}",response_model=UserRead)
def read_user(user_id:str, db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" or current_user.user_id == user_id:
        user = get_user_by_id(user_id,db)
        if user is None:
            raise HTTPException(status_code=404,detail="User not fount")
        
        return user
    else:
        raise HTTPException(status_code=404,detail="No funca")
        



#rut apa el inicio de sesion
@router.post("/login",response_model=Token)
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_session)):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401,
            detail="invalid username or password",
            headers={"WWW-Authenticate":"Bearer"},
            )
    access_token = create_access_token(data={"sub":user.user_id})
    return{"access_token":access_token,"token_type":"bearer"}





