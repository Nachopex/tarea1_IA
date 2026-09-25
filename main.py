import random
import Busqueda_Noinformada
import Busqueda_informada

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
        """Función de penalización: a mayor densidad de personas, mayor costo"""
        return 1 + (self.congestion[i][j] * 2)

    def obtener_vecinos(self, i, j):
        vecinos = [(i, j)]
        for desplazamiento_i, desplazamiento_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + desplazamiento_i, j + desplazamiento_j
            if 0 <= ni < self.filas and 0 <= nj < self.cols:
                if self.mapa[ni][nj] not in ['#', 'F']:
                    vecinos.append((ni, nj))
        return vecinos



