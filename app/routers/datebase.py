from fastapi import APIRouter, HTTPException
from ..Utils import Utils
from pydantic import BaseModel
from datetime import datetime

# Crear el router con un prefijo "/db"
router = APIRouter(
    prefix="/db",  # Prefijo para todas las rutas dentro de este router
    tags=["Database"]  # Etiqueta para la documentación en Swagger
)

# Modelo de datos para la inserción
class Medicion(BaseModel):
    temperatura: float
    humedad: float
    id_producto: int

class Usuario(BaseModel):
    correo: str
    contrasena: str

def get_db_connection():
    if not Utils.conexion.is_connected():
        Utils.conexion.reconnect()
    return Utils.conexion

# Ruta para obtener todas las mediciones
@router.get("/mediciones")  # Esto ahora será accesible en /db/mediciones
def obtener_mediciones():
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Medicion;")
    mediciones = cursor.fetchall()

    cursor.close()
    return {"mediciones": mediciones}

@router.post("/mediciones")
def insertar_medicion(medicion: Medicion):
    conexion = get_db_connection()
    cursor = conexion.cursor()

    fecha_actual = datetime.now()

    cursor.execute(
        "INSERT INTO Medicion (Fecha, IdSensor, IdProducto, valor) VALUES (%s, %s, %s, %s);",
        (fecha_actual, 1, medicion.id_producto, medicion.temperatura)
    )

    cursor.execute(
        "INSERT INTO Medicion (Fecha, IdSensor, IdProducto, valor) VALUES (%s, %s, %s, %s);",
        (fecha_actual, 2, medicion.id_producto, medicion.humedad)
    )

    conexion.commit()

    cursor.close()
    return {"message": "Medición insertada exitosamente"}

@router.post("/sign_up")
def sign_up(usuario: Usuario):
    conexion = get_db_connection()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT IdUsuario FROM Usuario WHERE Correo = %s AND Contrasena = %s;",
        (usuario.correo, usuario.contrasena)
    )
    usuario = cursor.fetchone()
    cursor.close()

    if usuario is None:
        raise HTTPException(status_code=403, detail="Usuario no encontrado")

    return {"IdUsuario": usuario[0]}

@router.get("/productos/{id_usuario}")
def obtener_productos(id_usuario: int):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Producto WHERE IdUsuario = %s;", (id_usuario,))
    productos = cursor.fetchall()

    cursor.close()

    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos para este usuario")

    return {"productos": productos}

# Ruta para obtener la última temperatura de un producto
@router.get("/productos/{id_producto}/ultima_temperatura")
def obtener_ultima_temperatura(id_producto: int):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT valor FROM Medicion WHERE IdProducto = %s AND IdSensor = 1 ORDER BY Fecha DESC LIMIT 1;",
        (id_producto,)
    )
    ultima_temperatura = cursor.fetchone()

    cursor.close()

    if ultima_temperatura is None:
        raise HTTPException(status_code=404, detail="No se encontró la última temperatura para este producto")

    return {"ultima_temperatura": ultima_temperatura}

# Ruta para obtener la última humedad de un producto
@router.get("/productos/{id_producto}/ultima_humedad")
def obtener_ultima_humedad(id_producto: int):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT valor FROM Medicion WHERE IdProducto = %s AND IdSensor = 2 ORDER BY Fecha DESC LIMIT 1;",
        (id_producto,)
    )
    ultima_humedad = cursor.fetchone()

    cursor.close()

    if ultima_humedad is None:
        raise HTTPException(status_code=404, detail="No se encontró la última humedad para este producto")

    return {"ultima_humedad": ultima_humedad}

# Nueva ruta para obtener el historial de temperatura de un producto
@router.get("/productos/{id_producto}/historico_temperatura")
def obtener_historico_temperatura(id_producto: int):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT valor, Fecha FROM Medicion WHERE IdProducto = %s AND IdSensor = 1 ORDER BY Fecha DESC;",
        (id_producto,)
    )
    historico_temperatura = cursor.fetchall()

    cursor.close()

    if not historico_temperatura:
        raise HTTPException(status_code=404, detail="No se encontró el historial de temperatura para este producto")

    return {"historico_temperatura": historico_temperatura}

# Nueva ruta para obtener el historial de humedad de un producto
@router.get("/productos/{id_producto}/historico_humedad")
def obtener_historico_humedad(id_producto: int):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT valor, Fecha FROM Medicion WHERE IdProducto = %s AND IdSensor = 2 ORDER BY Fecha DESC;",
        (id_producto,)
    )
    historico_humedad = cursor.fetchall()

    cursor.close()

    if not historico_humedad:
        raise HTTPException(status_code=404, detail="No se encontró el historial de humedad para este producto")

    return {"historico_humedad": historico_humedad}