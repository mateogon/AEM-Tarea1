
def leer_datos(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    # Extraer información básica
    num_proyectos = int(lineas[0].strip())
    num_tareas = int(lineas[1].strip())
    presupuesto_max = int(lineas[2].strip())
    
    # Extraer las ganancias de cada proyecto
    ganancias = list(map(int, lineas[3].strip().split()))
    
    # Extraer los costos de cada tarea
    costos = list(map(int, lineas[4].strip().split()))
    
    # Extraer las tareas asociadas a cada proyecto
    tareas_por_proyecto = []
    for i in range(5, 5 + num_proyectos):
        tareas = list(map(int, lineas[i].strip().split()))
        tareas_por_proyecto.append(tareas)
    
    return num_proyectos, num_tareas, presupuesto_max, ganancias, costos, tareas_por_proyecto

def obtener_tareas_proyecto(proyecto, tareas_por_proyecto):
    # Retorna las tareas asociadas a un proyecto específico
    tareas = tareas_por_proyecto[proyecto]
    return tareas

def calcular_costo_tareas(tareas_totales, costos):
    # Calcula el costo total basado en las tareas seleccionadas
    costo = 0
    for tarea in range(len(tareas_totales)):
        if tareas_totales[tarea]:
            costo += costos[tarea]
    return costo

def cumple_presupuesto(proyectos_seleccionados, presupuesto_max, tareas_por_proyecto, costos):
    tareas_seleccionadas = [0 for _ in range(len(costos))]
    
    for proyecto in proyectos_seleccionados:
        tareas_del_proyecto = obtener_tareas_proyecto(proyecto, tareas_por_proyecto)
        for i, tarea_seleccionada in enumerate(tareas_del_proyecto):
            if tarea_seleccionada:
                tareas_seleccionadas[i] = 1
    
    costo_total = calcular_costo_tareas(tareas_seleccionadas, costos)
    
    return costo_total <= presupuesto_max, costo_total

def calcular_ganancia(proyectos_seleccionados, ganancias):
    ganancias_totales = 0
    for proyecto in proyectos_seleccionados:
        ganancias_totales += ganancias[proyecto]
    return ganancias_totales


if __name__ == '__main__':
    archivo = '1-2024.txt'  # Asegúrate de usar la ruta correcta al archivo
    num_proyectos, num_tareas, presupuesto_max, ganancias, costos, tareas_por_proyecto = leer_datos(archivo)

    print(f'Número de proyectos: {num_proyectos}')
    print(f'Número de tareas: {num_tareas}')
    print(f'Presupuesto máximo: {presupuesto_max}')
    print(f'Ganancias: {ganancias}')
    print(f'Costos: {costos}')
    print(f'Tareas por proyecto: {tareas_por_proyecto[:2]}')  # Imprime solo las tareas de los primeros dos proyectos para revisar
