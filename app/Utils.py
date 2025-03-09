import mysql.connector
import tensorflow as tf

class Utils:
    # Conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",       # Si usas un servidor remoto, cambia esto por la IP
        user="root",            # Usuario de MySQL
        password="Passw0rd",    # La contraseña de MySQL
        database="SensorDB"     # Nombre de la base de datos
    )

    # Cargar el modelo de TensorFlow
    modelo = tf.keras.models.load_model("C:/Users/DELL/Desktop/Tec/Semestres/7. Septimo/Emprendimiento/Emprendimiento/proyecto/fastapi-server/app/resources/mejor_modelo.keras")