from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..Utils import Utils
import numpy as np

# Crear el router con un prefijo "/modelo"
router = APIRouter(
    prefix="/modelo",  # Prefijo para todas las rutas dentro de este router
    tags=["Modelo"]    # Etiqueta para la documentación en Swagger
)

# Definir el modelo de datos para la entrada
class DatosEntrada(BaseModel):
    datos: list

# Ruta para hacer una predicción con el modelo
@router.post("/predecir")
def predecir(datos_entrada: DatosEntrada):
    datos = np.array(datos_entrada.datos)

    # Verificar si el tamaño es correcto
    if datos.size != 60 * 6:
        raise HTTPException(
            status_code=400, 
            detail=f"El tamaño de los datos es incorrecto. Se esperaba {60*6} elementos, pero se recibieron {datos.size}."
        )

    try:
        datos = datos.reshape(1, 60, 6)  # Ajusta la forma según sea necesario
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo cambiar la forma de los datos. Asegúrate de que la estructura sea correcta."
        )

    # Hacer una predicción
    try:
        prediccion = Utils.modelo.predict(datos)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al hacer la predicción: {str(e)}"
        )

    # Devolver la predicción
    return {"prediccion": prediccion.tolist()}
