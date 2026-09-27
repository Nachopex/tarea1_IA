import random
import Busqueda_Noinformada
import Busqueda_informada
import genetico
class Agente:
    def __init__(self, id_agente, pos_inicial):
        self.id = id_agente
        self.posicion = pos_inicial
        self.ruta = []
        self.evacuado = False
        self.muerto = False

class SimulacionEscape:
    def __init__(self, mapa_grid, k_fuego, posiciones_agentes):
        """
        mapa_grid: Matriz del entorno (' ' libre, '#' muro, 'S' salida, 'F' fuego).
        k_fuego: Turnos para propagación del fuego
        """
        self.mapa = [list(fila) for fila in mapa_grid]
        self.filas = len(self.mapa)
        self.cols = len(self.mapa[0])
        self.k_fuego = k_fuego
        self.turno_actual = 0
        self.congestion = [[0 for _ in range(self.cols)] for _ in range(self.filas)]
        self.salida = self.encontrar_salida()
        self.agentes = [Agente(i, pos) for i, pos in enumerate(posiciones_agentes)]
        self.actualizar_congestion()   

    def encontrar_salida(self):
        # Cada piso cuenta con una única salida de evacuación
        for i in range(self.filas):
            for j in range(self.cols):

                if self.mapa[i][j] == 'S':
                    return (i, j)
        return None

    def actualizar_congestion(self):
        """Calcula la cantidad de agentes en cada celda para generar cuellos de botella"""
        self.congestion = [[0 for _ in range(self.cols)] for _ in range(self.filas)]
        for agente in self.agentes:

            if not agente.evacuado and not agente.muerto:
                i, j = agente.posicion
                self.congestion[i][j] += 1

    def propagar_fuego(self):
        """El fuego se propaga de manera irreversible y consume agentes a su paso"""
        nuevos_fuegos = []
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for i in range(self.filas):

            for j in range(self.cols):

                if self.mapa[i][j] == 'F':
                    for desplazamiento_i, desplazamiento_j in movimientos:
                        ni, nj = i + desplazamiento_i, j + desplazamiento_j
                        if 0 <= ni < self.filas and 0 <= nj < self.cols:
                            if self.mapa[ni][nj] not in ['#', 'S', 'F']:
                                nuevos_fuegos.append((ni, nj))
        
        for ni, nj in nuevos_fuegos:
            self.mapa[ni][nj] = 'F'
            
        # Comprobar si el fuego alcanzó a algún agente
        for agente in self.agentes:

            if not agente.evacuado and not agente.muerto:
                if self.mapa[agente.posicion[0]][agente.posicion[1]] == 'F':
                    agente.muerto = True

    def costo_movimiento(self, i, j):
        """Función de penalización cuadrática: a mayor concentración, costo exponencial."""
        return 1 + (self.congestion[i][j] ** 2) * 2

    def obtener_vecinos(self, i, j):
        vecinos = []
        for desplazamiento_i, desplazamiento_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:

            ni, nj = i + desplazamiento_i, j + desplazamiento_j
            if 0 <= ni < self.filas and 0 <= nj < self.cols:
                if self.mapa[ni][nj] not in ['#', 'F']:
                    vecinos.append((ni, nj))
        return vecinos

    def planificar_ruta(self, agente, algoritmo):
        """Calcula o recalcula el camino del agente hacia la salida según el algoritmo elegido."""
        if agente.muerto or agente.evacuado:
            agente.ruta = []
            return

        camino = None
        if algoritmo == "BFS":
            camino = Busqueda_Noinformada.bfs(self, agente.posicion)
        elif algoritmo == "DFS":
            camino = Busqueda_Noinformada.dfs(self, agente.posicion)
        elif algoritmo == "Greedy":
            camino = Busqueda_informada.greedy_best_first(self, agente.posicion)
        elif algoritmo == "A*":
            camino = Busqueda_informada.a_star(self, agente.posicion)
        elif algoritmo == "Genético":
            camino = genetico.algoritmo_genetico(self, agente.posicion)

        # Si encontró un camino válido, omitimos la casilla actual (camino[0])
        if camino and len(camino) > 1:
            agente.ruta = list(camino[1:])
        else:
            agente.ruta = []

    def turno(self,algoritmo):

        # Expandir el fuego si estamos en un multiplo de k
        
        if self.turno_actual > 0:
            if self.turno_actual % self.k_fuego == 0:
                self.propagar_fuego()

        CAPACIDAD_MAXIMA = 3
        for agente in self.agentes:
            # Revisar si el agente esta muerto o si ya escapo
            if agente.muerto or agente.evacuado:
                continue

            # Buscar si en la ruta del agente fue bloqueado por el fuego a unas 3 casillas de distancia
            ruta_bloqueada = False
            for i,j in agente.ruta[:4]:
                if self.mapa[i][j] == 'F':
                    ruta_bloqueada = True
                    break

            # Verificar si existe un camino
            # 1. Planificar si no tiene ruta o si se topó con fuego próximo
            if not agente.ruta or ruta_bloqueada:
                self.planificar_ruta(agente, algoritmo)

            # Si no encontró ruta posible, no puede avanzar este turno
            if not agente.ruta:
                continue

            # 2. Mirar la siguiente casilla sin sacarla de la lista
            siguiente_paso = agente.ruta[0]

            ci, cj = siguiente_paso

            # Si la casilla está saturada y no es la salida de escape
            if self.congestion[ci][cj] >= CAPACIDAD_MAXIMA and siguiente_paso != self.salida:
                # Replanifica para ver si encuentra un camino secundario despejado
                self.planificar_ruta(agente, algoritmo)
                if agente.ruta:
                    siguiente_paso = agente.ruta[0]
                    ci, cj = siguiente_paso

                # Si sigue llena (o no hay otra ruta), el agente ESPERA este turno
                if self.congestion[ci][cj] >= CAPACIDAD_MAXIMA and siguiente_paso != self.salida:
                    continue
                

            # Movimiento físico
            pos_anterior = agente.posicion
            agente.posicion = agente.ruta.pop(0)

            # Actualización inmediata del tráfico
            self.congestion[pos_anterior[0]][pos_anterior[1]] -= 1
            self.congestion[agente.posicion[0]][agente.posicion[1]] += 1

            # Comprobación de meta
            if agente.posicion == self.salida:
                agente.evacuado = True
                self.congestion[agente.posicion[0]][agente.posicion[1]] -= 1

        self.turno_actual +=1

        self.actualizar_congestion()

    def terminar(self):
            """Retorna True si todos los agentes han sido evacuados o han muerto."""
            return all(agente.evacuado or agente.muerto for agente in self.agentes)