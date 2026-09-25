from collections import deque

# asumimos que caminos seguira una estructura de (coordenadas, [nodo1,nodo2,nodo3...,nodoFin])
def bfs(simulacion,inicio):
  """Búsqueda en Anchura (BFS)."""

  caminos = deque([(inicio, [inicio])])
  visitados = set([inicio])

  while caminos:

    actual, camino = caminos.popleft()
    for nodos in simulacion.obtener_vecinos(actual[0], actual[1]):

      if nodos in visitados:
        continue

      visitados.add(nodos)
      nuevo_camino = camino + [nodos]
      caminos.append((nodos, nuevo_camino))

      if nodos == simulacion.salida:
        return caminos.pop()
  return None

def dfs(simulacion, inicio):

  camino = [inicio]
  visitados = set([inicio])

  while camino:

    actual = camino[-1]
    # Caso en que el nodo inicial sea el final
    if actual == simulacion.salida:
      return camino
    flag = False
    for nodo in simulacion.obtener_vecinos(actual[0], actual[1]):

      if nodo not in visitados:
        visitados.add(nodo)
        camino.append(nodo)
        flag = True
        if nodo == simulacion.salida:
          return camino
        break

    if flag == False:
      camino.pop()

  return None