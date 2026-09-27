from collections import deque

def bfs(simulacion, inicio):
    """Búsqueda en Anchura (BFS)."""
    # Caso en que el nodo inicial ya es la salida
    if inicio == simulacion.salida:
        return [inicio]

    # Cola FIFO con la estructura: (coordenada_actual, camino_recorrido)
    caminos = deque([(inicio, [inicio])])
    # Conjunto para evitar procesar casillas repetidas o ciclos
    visitados = set([inicio])

    while caminos:
        # Extraer el nodo más antiguo en la cola (exploración nivel por nivel)
        actual, camino = caminos.popleft()
        
        # Explorar casillas vecinas ortogonales transitables
        for nodos in simulacion.obtener_vecinos(actual[0], actual[1]):

            if nodos in visitados:
                continue

            # Marcar la casilla como visitada y agregarla a la cola
            visitados.add(nodos)
            nuevo_camino = camino + [nodos]
            caminos.append((nodos, nuevo_camino))

            # Test de objetivo al momento de generar el nodo sucesor
            if nodos == simulacion.salida:
                return nuevo_camino
                
    # Si la cola se vacía sin alcanzar la salida
    return None


def dfs(simulacion, inicio):
    """Búsqueda en profundidad (DFS)."""
    # Pila de camino que almacena la rama actual en exploración
    camino = [inicio]
    # Registro de casillas visitadas para no repetir nodos en la ruta
    visitados = set([inicio])

    while camino:
        # Observar el nodo en el tope de la pila sin desapilarlo
        actual = camino[-1]
        
        # Test de objetivo al expandir el nodo actual
        if actual == simulacion.salida:
            return camino
            
        flag = False
        # Buscar el primer vecino disponible para seguir profundizando
        for nodo in simulacion.obtener_vecinos(actual[0], actual[1]):

            if nodo not in visitados:
                visitados.add(nodo)
                camino.append(nodo)
                flag = True
                
                # Comprobación de meta al descubrir el nodo sucesor
                if nodo == simulacion.salida:
                    return camino
                # Interrumpir el bucle para continuar en profundidad por esta rama
                break

        # Si no quedan vecinos disponibles desde la casilla actual, retroceder (backtracking)
        if flag == False:
            camino.pop()

    # Si se desapilan todas las opciones sin hallar la meta
    return None