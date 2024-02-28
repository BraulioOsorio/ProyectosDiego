from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import get_session
from Api.Schemas.users import UserCreate,UserRead,Token,UserCreateAdmin,UserUpdateAdmin,UserUpdate
from Api.Crud.users import *
from Core.security import create_access_token,verify_token
from Api.Crud.tokens import *
from Api.Schemas.tokens import *

router = APIRouter()

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(token:str = Depends(oauth2_sheme), db:Session = Depends(get_session)):
    user_id = await verify_token(token)
    if user_id is None:
        token_update = TokenUpdate(
            token=token,
            token_status=False
        )
        await update_token_status(token_update,db)
        raise HTTPException(status_code=401,detail="Invalid token")

    token_db = await get_token_by_token(token,db)
    if token_db.token_status:
        user_db = get_user_by_id(user_id,db)
        if user_db is None:
            raise HTTPException(status_code=404,detail="User not found")
        return user_db
    else:
        raise HTTPException(status_code=401,detail="Invalid token")


@router.post("/create-user/",response_model=UserRead)
async def create_user(user:UserCreate,db:Session = Depends(get_session)):
    verify_user = get_user_by_email(user.mail,db)
    if verify_user is None:
        return create_new_user(user,db,'user')
    
    raise HTTPException(status_code=404,detail="Email already exists")


@router.post("/create-user-admin/",response_model=UserRead)
async def create_user(user:UserCreateAdmin,db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" and current_user.user_status:
        verify_user = get_user_by_email(user.mail,db)
        if verify_user is None:
            return create_new_user(user,db,user.user_role)
        
        raise HTTPException(status_code=404,detail="Email already exists")
    raise HTTPException(status_code=404,detail="Not authorized")



@router.get("/get/{user_id}",response_model=UserRead)
def read_user(user_id:str, db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_status:

        if current_user.user_role == "admin" or current_user.user_id == user_id:
            user = get_user_by_id(user_id,db)
            if user is None:
                raise HTTPException(status_code=404,detail="User not fount")
            
            return user
        else:
            raise HTTPException(status_code=404,detail="No funca")
    raise HTTPException(status_code=401,detail="the user is invalid")
    
@router.post("/update-user-admin/",response_model=UserRead)
async def update_user_admin(user:UserUpdateAdmin,db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" and current_user.user_status: 
        verify_user = get_user_by_email_update(user.user_id,user.mail,db)
        if verify_user:
            rolAdmin = get_users_rol(current_user.user_role,user.user_id,db)
            if rolAdmin:
                return update_user_exist(user,db,user.user_role)
            raise HTTPException(status_code=400,detail="No tiene Permisos Para modificar otro admin")
        raise HTTPException(status_code=400,detail="Email already exists")
    
    raise HTTPException(status_code=400,detail="No tiene Permisos o se encuentra desabilitado ")



@router.post("/update-user/",response_model=UserRead)
async def update_user(user:UserUpdate,db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):

    if current_user.user_status and current_user.user_id == user.user_id:
        verify_user = get_user_by_email_update(user.user_id,user.mail,db)
        if verify_user:
            return update_user_exist(user,db,current_user.user_role)
        raise HTTPException(status_code=400,detail="Email already exists")

        
    raise HTTPException(status_code=400,detail="No tiene Permisos o se encuentra desabilitado ")
        

#rut apa el inicio de sesion
@router.post("/login",response_model=Token)
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_session)):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401,
            detail="invalid username or password",
            headers={"WWW-Authenticate":"Bearer"},
            )
    if user.user_status:
        access_token = create_access_token(data={"sub":user.user_id})
        token = TokenCreate(
            token=access_token,
            user_id = user.user_id
        )

        TOKEN = await create_new_token(token,db)
        return{"access_token":access_token,"token_type":"bearer"}
    raise HTTPException(status_code=401,detail="usuario Inactivo")


@router.post("/logout",response_model=TokenRead)
async def destroy_token(token_data:TokenUpdate,db:Session = Depends(get_session)):
    return await update_token_status(token_data,db)





