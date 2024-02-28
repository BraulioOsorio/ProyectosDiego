from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import get_session
from Api.Schemas.users import UserRead
from Api.Schemas.transacciones import *
from Api.Crud.transacciones import *
from Api.Routes.users import get_current_user
from typing import List
from Api.Crud.users import get_user_by_id
from Api.Crud.categories import cate_by_id


router = APIRouter()

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/create-transactions",response_model=TRead)
async def create_transactions(tran:TCreate,db:Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_status:
        verify_cate = cate_by_id(tran.category_id,db)
        if verify_cate is None:
            raise HTTPException(status_code=404,detail="Categoria no encontrada")
        
        if verify_cate.category_status:
            return create_new_t(tran,db,current_user.user_id)
        raise HTTPException(status_code=404,detail="La categoria esta desabilitada")
        
    raise HTTPException(status_code=404,detail="Esta desabilitado")


@router.post("/update-transactios",response_model=TRead)
async def update_transaction_exist(tran:TUpdate,db : Session = Depends(get_session),current_user : UserRead = Depends(get_current_user)):
    if current_user.user_status:
        verify_cate = cate_by_id(tran.category_id,db)
        if verify_cate is None:
            raise HTTPException(status_code=404,detail="Categoria no encontrada")
        if verify_cate.category_status:
            return update_t_exist(tran,db)

        raise HTTPException(status_code=404,detail="La categoria esta desabilitada")
    
    raise HTTPException(status_code=404,detail="Esta desabilitado")


@router.get("/get-transactions/{t_id}",response_model=TRead)
async def get_transactions(t_id:int,db:Session = Depends(get_session),current_user :UserRead =Depends(get_current_user)):
    if current_user.user_status:
        transaction = get_t_id(t_id,db)
        if transaction is None:
            raise HTTPException(status_code=404,detail="No existe la Transaccion")
        if transaction.user_id == current_user.user_id:
            return transaction
        raise HTTPException(status_code=404,detail="Esta transccion no es suya")

    raise HTTPException(status_code=404,detail="Esta desabilitado")


@router.get("/get-transactions/all/",response_model=List[TRead])
async def get_transactions_all(db:Session = Depends(get_session),current_user :UserRead =Depends(get_current_user)):
    if current_user.user_status:
        transaction = get_t_all(current_user.user_id,db)
        if transaction is None:
            raise HTTPException(status_code=404,detail="No Hay")
       
        return transaction
        

    raise HTTPException(status_code=404,detail="Esta desabilitado")

