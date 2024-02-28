# from fastapi import FastAPI,Request,Depends
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# from db.session import get_session

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/home")
# def inicio():
#     return { "msg" : "Hola mundo" }

# @app.get("/")
# def prueba(db:Session = Depends(get_session)):
#     return { "msg" : "Hello World" }

from fastapi import FastAPI,APIRouter
from Api.Routes import users,categories,transacciones
from Core.config import settings

api_router = APIRouter()
api_router.include_router(users.router,prefix="/users",tags=["users"])
api_router.include_router(categories.router,prefix="/categories",tags=["categories"])
api_router.include_router(transacciones.router,prefix="/transation",tags=["transacciones"])

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION,description=settings.PROJECT_DESCRIPTION)
app.include_router(api_router)

