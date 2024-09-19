import heapq
import math

# Grafo con distancias entre nodos
grafo = {
    'A': [('B', 3), ('C', 2)],
    'B': [('A', 3), ('C', 4), ('D', 5)],
    'C': [('A', 2), ('B', 4), ('E', 3)],
    'D': [('B', 5), ('E', 4), ('G', 4)],
    'E': [('C', 3), ('D', 4), ('F', 2)],
    'F': [('E', 2), ('G', 3)],
    'G': [('F', 3), ('D', 4)],
}

# Coordenadas de los nodos
coordenadas = {
    'A': (0, 0),
    'B': (-3, 3),
    'C': (3, 3),
    'D': (-3, 7),
    'E': (3, 7),
    'F': (2, 10),
    'G': (-1, 11),
}


#def distancia_euclidiana(nodo, objetivo):
 #   (x1, y1) = coordenadas[nodo]
  #  (x2, y2) = coordenadas[objetivo]
   # return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def a_star(grafo, inicio, objetivo):
    # Priority queue para los nodos por explorar
    open_set = []
    heapq.heappush(open_set, (0, inicio))

    # Diccionarios para guardar los costos y los padres de cada nodo
    costos = {inicio: 0}
    padres = {inicio: None}

    while open_set:
        _, nodo_actual = heapq.heappop(open_set)

        # Si llegamos al objetivo, reconstruimos el camino
        if nodo_actual == objetivo:
            return reconstruir_camino(padres, objetivo)

        # Expandir los vecinos
        for vecino, costo in grafo.get(nodo_actual, []):
            nuevo_costo = costos[nodo_actual] + costo

            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                # En lugar de heurística, solo usamos el costo acumulado
                prioridad = nuevo_costo  # Sin heurística
                heapq.heappush(open_set, (prioridad, vecino))
                padres[vecino] = nodo_actual

    # Si no se encuentra un camino al objetivo
    return None


def reconstruir_camino(padres, objetivo):
    camino = []
    nodo_actual = objetivo
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = padres[nodo_actual]
    camino.reverse()  # Invertir el camino para que vaya desde el inicio al objetivo
    return camino

if __name__ == "__main__":
    # Ejecución del algoritmo
    inicio = 'A'
    objetivo = 'G'
    camino = a_star(grafo, inicio, objetivo)
    print("Camino encontrado:", camino)