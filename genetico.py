import random

def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Generamos un camino para el individuo de un largo 'longitud' con movimientos al azar
def generar_individuo(longitud):
    movimientos = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    return [random.choice(movimientos) for _ in range(longitud)]

# Evaluamos los individuos y obtenemos su valor fitnnes
def evaluar_individuo(individuo, simulacion, inicio):
    pos_actual = inicio
    camino = [inicio]

    # Recorremos la lista entera de movimientos que tiene el camino del individuo
    for mov in individuo:
        candidato = (pos_actual[0] + mov[0], pos_actual[1] + mov[1])
        # Si el individuo en su trayecto no choca con una pared o el fuego 
        if candidato in simulacion.obtener_vecinos(pos_actual[0], pos_actual[1]):
            pos_actual = candidato
            camino.append(pos_actual)
            if pos_actual == simulacion.salida:
                break
        # Si el individuo choco con algo entonces se tomara el camino hasta antes de chocar para obtener el valor del individuo
        else:
            break
                
    distancia = heuristica_manhattan(pos_actual, simulacion.salida)
    costo_movimiento= simulacion.costo_movimiento(pos_actual[0], pos_actual[1])
    # En caso de que el individuo no lograra llegar a la salida su puntaje se vera reducido
    fitness = 1000.0 / (distancia + costo_movimiento + 1)

    # En caso de que el individuo llegara a la salida se le dara un puntaje de 5000 y asi sea mas probable que sea elegido
    if pos_actual == simulacion.salida:
        fitness += 5000
        
    return fitness, camino

def algoritmo_genetico(simulacion, inicio, tam_poblacion=30, prob_mutacion=0.1):
    movimientos = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    generaciones = 30
    individuos = []
    actual_generacion = []
    largo = 30

    
    for i in range(tam_poblacion):
        ind = generar_individuo(largo)
        fitness, camino = evaluar_individuo(ind,simulacion,inicio)
        individuos.append([fitness, ind])


    for i in range(generaciones):

        if actual_generacion:
            individuos = []
            for ind in actual_generacion:
                fitness, camino = evaluar_individuo(ind,simulacion,inicio)
                individuos.append([fitness, ind])

        #Seleccion
        individuos.sort(reverse=True)
        mitad = tam_poblacion//2
        individuos = individuos[:mitad]

        corte = largo //2
        #Cruce
        actual_generacion = []
        for i in range(tam_poblacion):

            padre1 = random.choice(individuos)
            padre2 = random.choice(individuos)
            hijo = padre1[1][:corte] + padre2[1][corte:]
            

            #Mutacion
            if(random.random() < prob_mutacion):
                    hijo[random.randint(0,largo-1)] = random.choice(movimientos)

            actual_generacion.append(hijo)

    individuos = []
    for ind in actual_generacion:
        fitness, camino = evaluar_individuo(ind,simulacion,inicio)
        individuos.append([fitness, camino])

    individuos.sort(reverse=True)

    return individuos[0][1]