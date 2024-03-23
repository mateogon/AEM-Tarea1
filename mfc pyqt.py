import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import pyqtgraph as pg
import time
from gestor_tareas import leer_datos, cumple_presupuesto, calcular_ganancia

class WorkerThread(QThread):
    update_signal = pyqtSignal(float, float)

    def __init__(self, proyectos, presupuesto_max, tareas_por_proyecto, costos, ganancias):
        super(WorkerThread, self).__init__()
        
        self.proyectos = proyectos
        self.presupuesto_max = presupuesto_max
        self.tareas_por_proyecto = tareas_por_proyecto
        self.costos = costos
        self.ganancias = ganancias

    def run(self):
        self.mfc([], 0, time.time())

    def mfc(self, proyectos_seleccionados, index, start_time):
        if index == len(self.ganancias):
            if cumple_presupuesto(proyectos_seleccionados, self.presupuesto_max, self.tareas_por_proyecto, self.costos):
                ganancia_total = calcular_ganancia(proyectos_seleccionados, self.ganancias)
                tiempo_actual = time.time() - start_time
                self.update_signal.emit(tiempo_actual, ganancia_total)
            return

        # Explorar sin seleccionar el proyecto actual
        self.mfc(proyectos_seleccionados, index + 1, start_time)

        # Explorar seleccionando el proyecto actual
        self.mfc(proyectos_seleccionados + [index], index + 1, start_time)

class GraphWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        # Configuración inicial del gráfico
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("Ganancia Total vs. Tiempo", color="b", size="15pt")
        self.pen = pg.mkPen(color=(255, 0, 0))

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Temporizador para actualizar cada segundo
        self.timer.timeout.connect(self.update_graph)
        self.timer.start()

        # Inicializar listas x e y como atributos
        self.x = []
        self.y = []
        
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=self.pen)

        # Cargar datos de la tarea y configurar WorkerThread
        archivo = 'datos/1-2024.txt'
        num_proyectos, num_tareas, presupuesto_max, ganancias, costos, tareas_por_proyecto = leer_datos(archivo)

        self.last_update_time = time.time()  # Inicializar el contador de tiempo de actualización
        # Iniciar WorkerThread con la lógica MFC
        self.worker = WorkerThread([], presupuesto_max, tareas_por_proyecto, costos, ganancias)
        self.worker.update_signal.connect(self.update_plot_data)
        self.worker.start()
    def update_plot_data(self, tiempo, ganancia):
        # Acumula los datos en las listas x e y
        self.x.append(tiempo)
        self.y.append(ganancia)

    def update_graph(self):
        print(f"Actualizando gráfico... {time.time() - self.last_update_time:.2f} segundos")
        # Actualiza el gráfico si hay nuevos datos
        if self.x and self.y:
            self.data_line.setData(self.x, self.y)  # Actualiza los datos del gráfico
            self.graphWidget.setXRange(min(self.x), max(self.x))
            self.graphWidget.setYRange(min(self.y), max(self.y))
            self.graphWidget.enableAutoRange('xy', False)  # Deshabilita el auto-rango
            self.graphWidget.setLimits(xMin=min(self.x), xMax=max(self.x), yMin=min(self.y), yMax=max(self.y))  # Establece límites fijos

def main():
    app = QApplication(sys.argv)
    mainWin = GraphWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()