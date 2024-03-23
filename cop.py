# main.py

from gestor_tareas import leer_datos, cumple_presupuesto, calcular_gananacia


archivo = 'datos/1-2024.txt'
num_proyectos, num_tareas, presupuesto_max, ganancias, costos, tareas_por_proyecto = leer_datos(archivo)

proyectos_seleccionados = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
cumple, costo_total = cumple_presupuesto(proyectos_seleccionados, presupuesto_max, tareas_por_proyecto, costos)
ganancia = calcular_ganancia(proyectos_seleccionados, ganancias)
print(f'Costo total de las tareas seleccionadas: {costo_total}')
print(f'Ganancia total de los proyectos seleccionados: {ganancia}')
print(f'Se cumple el presupuesto: {"Sí" if cumple else "No"}')
