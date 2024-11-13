import requests
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Configuración del servidor Flask
FLASK_SERVER_URL = "http://54.236.89.141:8081/sensor/chart-data"  

def obtener_datos():
    """
    Función para obtener los datos del servidor Flask.
    """
    try:
        response = requests.get(FLASK_SERVER_URL)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error al obtener datos: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

def actualizar_grafico():
    """
    Función para actualizar el gráfico con datos en tiempo real.
    """
    # Obtener datos del servidor Flask
    data = obtener_datos()

    if data:
        # Limpiar el gráfico
        ax.cla()

        # Extraer datos
        temperaturas = data['temperaturas']
        humedades = data['humedades']
        luces = data['luces']
        tiempo = np.arange(len(temperaturas))  
        # Configurar los ejes
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Variables')
        ax.set_zlabel('Valores')
        ax.set_title('Gráfico de Barras 3D en Tiempo Real')

        # Ancho de las barras
        bar_width = 0.3

        # Graficar barras para Temperatura
        ax.bar(tiempo - bar_width, temperaturas, zs=0, zdir='y', color='red', alpha=0.8, label='Temperatura')

        # Graficar barras para Humedad
        ax.bar(tiempo, humedades, zs=1, zdir='y', color='green', alpha=0.8, label='Humedad')

        # Graficar barras para Lux
        ax.bar(tiempo + bar_width, luces, zs=2, zdir='y', color='blue', alpha=0.8, label='Lux')

        # Agregar leyenda
        ax.legend()

        # Redibujar el gráfico en la ventana
        canvas.draw()

    # Programar la próxima actualización en 1 segundo
    root.after(1000, actualizar_grafico)

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Gráfico de Barras 3D - Sensores")

# Crear la figura de Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Crear el widget de Matplotlib embebido en Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Iniciar la actualización del gráfico
actualizar_grafico()

# Iniciar el bucle principal de Tkinter
root.mainloop()
