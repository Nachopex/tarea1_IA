import statistics
import random
import time
from simulacion import SimulacionEscape

# Mapa 1 (Alta densidad / Cuello de botella)
# Pasillos muy angostos que convergen hacia una única salida.
# Tamaño: 20x11 | Agentes: 80
MAPA_1 = [
    "####################",
    "#F                S#",
    "############### ####",  
    "#                  #",
    "####### #### #######",  
    "#                 F#",
    "### #### #### #### #",  
    "#          F       #",
    "#F                 #",
    "#                  #",
    "####################"
]

# Mapa 2 (Densidad media / Laberinto corporativo)
# Múltiples salas conectadas por intersecciones y cruces ciegos.
# Tamaño: 30x15 | Agentes: 80
MAPA_2 = [
    "##############################",
    "#     #      #     F#       S#",
    "# ### # #### # #### # ###### #",
    "# #        #        #        #",
    "# # ###### ######## ######## #",
    "#   #    #   #    # #   #    #",
    "##### ## ### # ## # # # # ####",
    "#     #      #  #     #      #",
    "####### ######## ###### ######",
    "#       #      #      #      #",
    "# ##### # #### ###### ###### #",
    "# #   # #    #      # #      #",
    "# # # # #### ###### # # ######",
    "#F  #        #F              #",
    "##############################"
]

# Mapa 3 (Baja densidad / Dispersión abierta)
# Entorno semiabierto con baja concentración de muros y múltiples rutas.
# Tamaño: 40x18 | Agentes: 200
MAPA_3 = [
    "########################################",
    "#                                     S#",
    "#  ##          ##       F  ##          #",
    "#  ##          ##          ##          #",
    "#                                      #",
    "#       ####        ####        ####   #",
    "#       ####        ####        ####   #",
    "#F                                     #",
    "#                                      #",
    "#  ##          ##          ##          #",
    "#  ##          ##          ##          #",
    "#                                      #",
    "#F                                     #",
    "#       ####        ####        ####   #",
    "#       ####        ####        ####   #",
    "#                             F        #",
    "#                                      #",
    "########################################"
]
# Codigo extraido directamente del main para poder generar posiciones aleatorias para los agentes dentro de los mapas en cada iteracion de las pruebas
def generar_posiciones(mapa_grid, cantidad):
    """Genera posiciones aleatorias válidas"""
    filas = len(mapa_grid)
    cols = len(mapa_grid[0])
    libres = [(r, c) for r in range(filas) for c in range(cols) if mapa_grid[r][c] == ' ']
    
    if len(libres) >= cantidad:
        return random.sample(libres, cantidad)
    return [random.choice(libres) for _ in range(cantidad)]

# Configuracion para las pruebas, en donde se haran 100 iteraciones por algoritmo
ITERACIONES = 100 
ALGORITMOS = ["BFS", "DFS", "Greedy", "A*","Genético"]
CONFIGURACIONES_MAPAS = {
    "Mapa 1": (MAPA_1, 80, 3), # (Matriz, N° Agentes, k_fuego)
    "Mapa 2": (MAPA_2, 80, 3),
    "Mapa 3": (MAPA_3, 200, 3)
}

def ejecutar_benchmark():
    """Ejecuta las pruebas de rendimiento comparando los algoritmos en cada mapa."""
    print(f"=== INICIANDO BENCHMARK ({ITERACIONES} iteraciones por prueba) ===\n")
    
    for nombre_mapa, (mapa, cantidad_agentes, k_fuego) in CONFIGURACIONES_MAPAS.items():
        print(f"--- Evaluando {nombre_mapa} ({cantidad_agentes} agentes) ---")

        for algoritmo in ALGORITMOS:
            tiempos_turnos = []
            tasas_supervivencia = []

            # Ejecutar las iteraciones configuradas para el algoritmo actual
            for i in range(ITERACIONES):
                posiciones = generar_posiciones(mapa, cantidad_agentes)
                sim = SimulacionEscape(mapa, k_fuego, posiciones)

                salvados = 0
                while not sim.terminar():
                    sim.turno(algoritmo)

                # Contar agentes que lograron evacuar en la simulación
                for agente in sim.agentes:
                    if agente.evacuado:
                        salvados +=1
                supervivencia = (salvados/cantidad_agentes) * 100
                tasas_supervivencia.append(supervivencia)
                tiempos_turnos.append(sim.turno_actual)

            # Cálculo de estadísticas descriptivas de supervivencia y turnos
            promedio_supervivencia = statistics.mean(tasas_supervivencia)
            media_turnos = statistics.mean(tiempos_turnos)
            std_turnos = statistics.stdev(tiempos_turnos) if ITERACIONES > 1 else 0
            min_turnos = min(tiempos_turnos)
            max_turnos = max(tiempos_turnos)

            print(f"Algoritmo: {algoritmo: <8} | Supervivencia: {promedio_supervivencia:5.1f}% | "
                    f"Turnos -> Media: {media_turnos:5.1f} | DesvEst: {std_turnos:5.1f} | "
                    f"Min: {min_turnos} | Max: {max_turnos}")
        print("")
if __name__ == "__main__":
    tiempo_inicio = time.time()
    ejecutar_benchmark()
    print(f"Tiempo total de ejecución: {(time.time() - tiempo_inicio):.2f} segundos.")