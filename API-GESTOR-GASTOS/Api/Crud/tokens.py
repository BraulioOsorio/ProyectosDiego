import sys
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from Api.Models.User import Token_Model
from Api.Schemas.tokens import TokenCreate, TokenUpdate
#from Api.Models.transacciones import Transaction

async def create_new_token(token_data: TokenCreate, db: Session):
    token_db = Token_Model(
        token = token_data.token,
        user_id = token_data.user_id
    )

    try:
        db.add(token_db)
        db.commit()
        db.refresh(token_db)
        return token_db
    except Exception as e:
        db.rollback()
        print(f"Error al crear un token: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al crear token: {str(e)}")
    

async def get_token_by_token(token: str, db: Session):
    token_db = db.query(Token_Model).filter(Token_Model.token == token).first()
    if token_db is None:
        return None
    return token_db

async def update_token_status(token_data: TokenUpdate, db: Session):
    token_db = await get_token_by_token(token_data.token, db)
    if token_db:
        try:
            token_db.token_status = token_data.token_status
            db.add(token_db)
            db.commit()
            db.refresh(token_db)
            return token_db
        except Exception as e:
            db.rollback()
            print(f"Error al actualizar el estado del token: {str(e)}", file=sys.stderr)
            raise HTTPException(status_code=500, detail=f"Error al actualizar estado del token: {str(e)}")
    else:
        return None
