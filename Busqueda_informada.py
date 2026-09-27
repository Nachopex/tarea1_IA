# Distancia Manhattan entre dos puntos (fila, columna)
def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def greedy_best_first(simulacion, inicio):
    """Búsqueda voraz."""
    camino = [inicio]
    visitados = set([inicio])
    # Lista de nodos por explorar
    nodos_candidatos = []

    # Caso en que el nodo inicial ya sea la salida
    if camino[-1] == simulacion.salida:
        return camino
    
    while camino:
        actual = camino[-1]
        
        # Explorar casillas adyacentes no visitadas
        for nodo in simulacion.obtener_vecinos(actual[0], actual[1]):
            if nodo not in visitados:
                visitados.add(nodo)
                # Formato del candidato: [distancia_a_la_salida, coordenadas, ruta_completa]
                nodos_candidatos.append([heuristica_manhattan(nodo, simulacion.salida), nodo, camino + [nodo]])
        
        # Si no quedan caminos posibles por explorar
        if not nodos_candidatos:
            return None

        # Seleccionar y remover el nodo con menor distancia estimada a la meta
        mejor_paquete = min(nodos_candidatos)
        nodos_candidatos.remove(mejor_paquete)

        menor_h, mejor_nodo, mejor_camino = mejor_paquete

        camino = mejor_camino
        
        # Comprobar si se alcanzó la salida
        if mejor_nodo == simulacion.salida:
            return camino

    return None


def a_star(simulacion, inicio):
    """Búsqueda A* con penalización por congestión."""
    camino = [inicio]
    
    # Registro del costo real acumulado g(n) hasta cada casilla
    costo_acumulado = {inicio: 0}
    
    # Formato de la lista: [f, h, g, nodo_actual, camino_recorrido]
    nodos_candidatos = [[0, 0, 0, inicio, [inicio]]]
    
    # Caso en que el nodo inicial ya sea la salida
    if camino[-1] == simulacion.salida:
        return camino
    
    while nodos_candidatos:
        # Extraer el nodo con menor f(n) = g(n) + h(n)
        mejor_paquete = min(nodos_candidatos)
        nodos_candidatos.remove(mejor_paquete)
        f_actual, h_actual, costo_g, actual, mejor_camino = mejor_paquete

        camino = mejor_camino
        
        # Comprobar si el nodo extraído es la salida
        if actual == simulacion.salida:
            return mejor_camino
        
        # Revisar los vecinos válidos
        for nodo in simulacion.obtener_vecinos(actual[0], actual[1]):
            # Sumar el costo acumulado anterior más el costo de la casilla (incluye congestión)
            nuevo_g = costo_g + simulacion.costo_movimiento(nodo[0], nodo[1])
            
            # Si es la primera vez que se visita el nodo o encontramos una ruta de menor costo hacia él
            if nodo not in costo_acumulado or nuevo_g < costo_acumulado[nodo]:
                costo_acumulado[nodo] = nuevo_g
                nuevo_h = heuristica_manhattan(nodo, simulacion.salida)
                funcion_f = nuevo_g + nuevo_h
                
                # Guardar el candidato actualizado para la siguiente iteración
                nodos_candidatos.append([funcion_f, nuevo_h, nuevo_g, nodo, mejor_camino + [nodo]])

    return None