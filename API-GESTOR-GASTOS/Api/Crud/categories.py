import sys
from fastapi.responses import JSONResponse
from Api.Models.Categories import Category

from fastapi import HTTPException
from Api.Schemas.categories import *
from sqlalchemy.orm import Session


def create_new_category(cate:CateCreate,db:Session):
    cate_db = Category(
        category_name = cate.category_name,
        category_description = cate.category_description
    )
    try:
        db.add(cate_db)
        db.commit()
        db.refresh(cate_db)
        db.close()
        return cate_db
    except Exception as e:
        db.rollback()
        print(f"Error al crear una categoria: {str(e)}",file=sys.stderr)
        raise HTTPException(status_code=500,detail=f"Error al crear la categoria: {str(e)} ")
    

def update_category_exist(cate:CateUpdate,db : Session):
    cate_db = db.query(Category).filter(Category.category_id == cate.category_id).first()
    print(cate_db.category_id)
    if not cate_db:
        raise HTTPException(status_code=401,detail="The category not exist")
    
    cate_db.category_name = cate.category_name
    cate_db.category_description = cate.category_description
    cate_db.category_status = cate.category_status    
    

    try:
        db.commit()
        db.close()
        return JSONResponse(content={"message": "Item updated successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=401,detail="not update")


def cate_by_id(cate_id : int, db : Session):
    cate = db.query(Category).filter(Category.category_id == cate_id).first()
    if not cate:
        raise HTTPException(status_code=401,detail="La categoria no existe")
    return cate

def get_all_categories(db: Session):
    category = db.query(Category).filter(Category.category_status == 1).all()
    return category
        
    