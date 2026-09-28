# tarea1_IA
_Luis Martinez Neira_<br>
_2023427985_

# Sobre el entregable
Esta tarea escrita en python implementa 5 algoritmos de busqueda, dividido en 3 categorias: búsqueda no informada (BFS, DFS), búsqueda informada (Voraz y A*) y algoritmo genético

## Declaración de Autoría y Uso de IA
- **Algoritmos y Simulación:** Implementación propia de los algoritmos de búsqueda no informada, informada y genético, asi como de simulacion.py y benchmarking.py.
- **Interfaz Gráfica (`main.py`):** Construida con la asistencia de IA Generativa para la visualización opcional de la simulación.


## Reglas para Ejecutar el Código

### 1. Interfaz Gráfica Interactiva
Permite observar en tiempo real el comportamiento visual de los agentes, la expansión del fuego y la congestión paso a paso o de manera continua.

Para iniciar la interfaz, ejecute en la terminal:
```bash
python main.py
```
Se abrira una interfaz en la que se podran seleccionar 3 mapas distintos asi como los 5 algoritmos. Se podra avanzar los turnos manualmente o tambien hacerlo de manera automatica, asi como ajustar su velocidad. Si desea reiniciar la simulacion solo debe apretar el boton "reiniciar". Los agentes solo cambiaran de posicion al ejecutar main.py

Si desea ejecutar el benchmarking, ejecute en la terminal:
```bash
python benchmarking.py
```
> **Nota para usuarios de Linux:** Si `tkinter` no viene preinstalado con su distribución de Python, puede instalarse ejecutando:
> ```bash
> sudo apt-get install python3-tk
> ```
