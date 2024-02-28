import sys

from fastapi.responses import JSONResponse # Mandar mensajes de error al log

from Api.Models.transacciones import Transaction
from fastapi import HTTPException
from Api.Schemas.transacciones import *
from sqlalchemy.orm import Session


def create_new_t(tran:TCreate,db:Session,id_user : str):
    t_db = Transaction(
        user_id = id_user,
        category_id = tran.category_id,
        amount = tran.amount,
        t_description = tran.t_description,
        t_type = tran.t_type
    )

    try:
        db.add(t_db)
        db.commit()
        db.refresh(t_db)
        db.close()
        return t_db
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=f"Error al crear la transaccion: {str(e)} ")


def update_t_exist(tran:TUpdate,db:Session):
    t_db = db.query(Transaction).filter(Transaction.transactions_id == tran.transactions_id).first()
    if not t_db:
        raise HTTPException(status_code=404,detail="No existe")
    
    t_db.amount = tran.amount
    t_db.t_description = tran.t_description
    t_db.t_type =tran.t_type
    t_db.category_id = tran.category_id

    try:
        db.commit()
        db.close()
        return JSONResponse(content={"message": "Item updated successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="Se peto") 
    

def get_t_id(id : int,db : Session):
    t_db = db.query(Transaction).filter(Transaction.transactions_id == id).first()
    return t_db


def get_t_all(id_user : str,db:Session):
    t_db_all = db.query(Transaction).filter(Transaction.user_id == id_user).all()
    return t_db_all
