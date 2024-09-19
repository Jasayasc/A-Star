import heapq
import math


def ingresar_grafo():
    grafo = {}
    #coordenadas = {}

    # Solicitar el número de nodos
    num_nodos = int(input("Ingrese la cantidad de nodos: "))

    # Ingresar coordenadas para cada nodo
    for _ in range(num_nodos):
        nodo = input(f"Ingrese el nombre del nodo ({_}): ")
    #    x = float(input(f"Ingrese la coordenada X del nodo {nodo}: "))
    #    y = float(input(f"Ingrese la coordenada Y del nodo {nodo}: "))
    #    coordenada [nodo] = (x, y)
    #    grafo[nodo] = []  # Inicializa la lista de conexiones para cada nodo

    # Ingresar las conexiones entre nodos
    while True:
        conexion = input("Ingrese la conexión entre nodos (formato: nodo1 nodo2 costo) o 'fin' para terminar: ")
        if conexion.lower() == 'fin':
            break
        nodo1, nodo2, costo = conexion.split()
        costo = float(costo)
        # Añadir la conexión a ambos nodos ya que es un grafo no dirigido
        grafo[nodo1].append((nodo2, costo))
        grafo[nodo2].append((nodo1, costo))

    return grafo, coordenadas



def a_star(grafo, coordenadas, inicio, objetivo):
    open_set = []
    heapq.heappush(open_set, (0, inicio))

    costos = {inicio: 0}
    padres = {inicio: None}

    while open_set:
        _, nodo_actual = heapq.heappop(open_set)

        if nodo_actual == objetivo:
            return reconstruir_camino(padres, objetivo)

        for vecino, costo in grafo.get(nodo_actual, []):
            nuevo_costo = costos[nodo_actual] + costo

            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                # En lugar de heurística, solo usamos el costo acumulado
                prioridad = nuevo_costo  # Sin heurística
                heapq.heappush(open_set, (prioridad, vecino))
                padres[vecino] = nodo_actual

    return None


def reconstruir_camino(padres, objetivo):
    camino = []
    nodo_actual = objetivo
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = padres[nodo_actual]
    camino.reverse()
    return camino


# Solicitar datos del grafo al usuario
grafo, coordenadas = ingresar_grafo()

# Solicitar nodo inicial y objetivo
inicio = input("Ingrese el nodo de inicio: ")
objetivo = input("Ingrese el nodo objetivo: ")

# Ejecutar el algoritmo A*
camino = a_star(grafo, coordenadas, inicio, objetivo)

# Mostrar el resultado
if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino entre los nodos especificados.")
