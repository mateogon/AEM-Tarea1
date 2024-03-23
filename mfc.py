import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

# Assuming gestor_tareas provides the necessary functions
from gestor_tareas import leer_datos, cumple_presupuesto, calcular_ganancia

# Variables for historic values
historic_gains = []
historic_times = []

lock = threading.Lock()

def mfc(proyectos_seleccionados, index, presupuesto_max, tareas_por_proyecto, costos, ganancias):
    if index == len(ganancias):
        cumple, _ = cumple_presupuesto(proyectos_seleccionados, presupuesto_max, tareas_por_proyecto, costos)
        if cumple:
            ganancia_total = calcular_ganancia(proyectos_seleccionados, ganancias)
            tiempo_actual = time.time() - start_time
            with lock:
                historic_times.append(tiempo_actual)
                historic_gains.append(ganancia_total)
        return

    mfc(proyectos_seleccionados, index + 1, presupuesto_max, tareas_por_proyecto, costos, ganancias)
    new_selection = proyectos_seleccionados.copy()
    new_selection.append(index)
    mfc(new_selection, index + 1, presupuesto_max, tareas_por_proyecto, costos, ganancias)

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def animate(i):
    with lock:
        plt.cla()
        if historic_times and historic_gains:
            # Compute moving average for a smoother plot
            window_size = 20  # Adjust window_size to change smoothness
            smoothed_gains = moving_average(historic_gains, window_size)
            # Adjust times to match the length of the smoothed data
            smoothed_times = historic_times[:len(smoothed_gains)]
            plt.plot(smoothed_times, smoothed_gains, marker=',', markersize=3, linestyle='-')
            plt.xlabel('Execution Time (s)')
            plt.ylabel('Gain')
            plt.title('Gain over Time')
            plt.grid(True)

# Load the task data
archivo = 'datos/1-2024.txt'
num_proyectos, num_tareas, presupuesto_max, ganancias, costos, tareas_por_proyecto = leer_datos(archivo)

start_time = time.time()

# Start MFC in a separate thread
mfc_thread = threading.Thread(target=lambda: mfc([], 0, presupuesto_max, tareas_por_proyecto, costos, ganancias))
mfc_thread.start()

# Plotting in the main thread with real-time update
fig = plt.figure(figsize=(10, 6))
ani = FuncAnimation(fig, animate, interval=1000)  # Update the plot every second
plt.show()

mfc_thread.join()
