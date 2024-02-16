from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import get_session
from Api.Schemas.categories import *
from Api.Crud.categories import * 
from Api.Schemas.users import UserRead
from Api.Routes.users import get_current_user
from Api.Crud.users import *

router = APIRouter()

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/create-category/",response_model=CateRead)
async def create_category(cate:CateCreate,db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" and current_user.user_status:
        return create_new_category(cate,db)
    raise HTTPException(status_code=404,detail="No tiene permisos")

@router.post("/update-category/",response_model=CateRead)
async def update_category(cate:CateUpdate,db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" and current_user.user_status:
        return update_category_exist(cate,db)
    raise HTTPException(status_code=404,detail="No tiene permisos")

@router.get("get-category/{cate_id}",response_model=CateRead)
async def read_category(cate_id:int,db:Session =Depends(get_session),current_user : UserRead =Depends(get_current_user)):
    if current_user.user_status:
        cate = cate_by_id(cate_id,db)
        return cate 
    raise HTTPException(status_code=404,detail="no tiene permisos")