import tensorflow as tf
import numpy as np

# Cargar el modelo
modelo = tf.keras.models.load_model("C:/Users/DELL/Desktop/Tec/Semestres/7. Septimo/Emprendimiento/Emprendimiento/proyecto/fastapi-server/app/resources/mejor_modelo.keras")

# Imprimir un resumen del modelo para verificar que se ha cargado correctamente
modelo.summary()

# Ejemplo de datos de entrada (asegúrate de que los datos estén en el formato correcto)
# Supongamos que el modelo espera una entrada de forma (1, 60, 6)
datos_entrada = np.random.rand(1, 60, 6)  # Generar datos aleatorios con la forma correcta

# Hacer una predicción
prediccion = modelo.predict(datos_entrada)

# Imprimir la predicción
print("Predicción:", prediccion)