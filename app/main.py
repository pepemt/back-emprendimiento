from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.datebase import router as db_router
from app.routers.modelo import router as modelo_router

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",  # Reemplaza con la URL de tu frontend
    "http://127.0.0.1:3000",
    "http://172.20.10.5:8000"
    # Agrega aquí otros orígenes permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(db_router)
app.include_router(modelo_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}