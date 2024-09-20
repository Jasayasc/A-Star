import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

class NodoArbol:
    def _init_(self, valor):
        self.valor = valor
        self.hijos = []

def convertir_grafo_a_arbol(grafo, nodo_raiz):
    def construir_arbol(nodo, ancestros):
        arbol_nodo = NodoArbol(nodo)
        nuevos_ancestros = ancestros + [nodo]
        for vecino in grafo[nodo]:
            if vecino[0] != nodo and vecino[0] not in ancestros:
                arbol_nodo.hijos.append(construir_arbol(vecino[0], nuevos_ancestros))
            else:
                arbol_nodo.hijos.append(NodoArbol(vecino[0]))
        return arbol_nodo

    return construir_arbol(nodo_raiz, [])

def agregar_nodos_y_conexiones(grafo_nx, nodo, parent=None, unique_id=0, nodo_map=None):
    nodo_id = f"{nodo.valor}_{unique_id}"
    grafo_nx.add_node(nodo_id, label=nodo.valor)
    if parent:
        parent_id = f"{parent.valor}_{nodo_map[parent]}"
        grafo_nx.add_edge(parent_id, nodo_id)
    nodo_map[nodo] = unique_id
    for idx, hijo in enumerate(nodo.hijos):
        agregar_nodos_y_conexiones(grafo_nx, hijo, nodo, unique_id + idx + 1, nodo_map)

def ingresar_grafo():
    grafo = {}
    num_nodos = int(input("Ingrese la cantidad de nodos: "))
    for _ in range(num_nodos):
        nodo = input(f"Ingrese el nombre del nodo ({_ + 1}): ")
        grafo[nodo] = []  # Inicializa la lista de conexiones para cada nodo

    while True:
        conexion = input("Ingrese la conexión entre nodos (formato: nodo1 nodo2 costo) o 'fin' para terminar: ")
        if conexion.lower() == 'fin':
            break
        try:
            nodo1, nodo2, costo = conexion.split()
            costo = float(costo)

            if nodo1 not in grafo or nodo2 not in grafo:
                print("Uno o ambos nodos no existen. Asegúrese de haberlos ingresado correctamente.")
                continue

            grafo[nodo1].append((nodo2, costo))
            grafo[nodo2].append((nodo1, costo))
        except ValueError:
            print("Error en el formato de la conexión. Asegúrese de usar el formato: nodo1 nodo2 costo")

    return grafo

# Función principal
if _name_ == "_main_":
    # Ingresar el grafo
    grafo = ingresar_grafo()

    # Convertir el grafo en un árbol a partir del nodo raíz (puedes elegir el nodo que quieras como raíz)
    nodo_raiz = input("Ingrese el nodo raíz para el árbol: ")
    arbol = convertir_grafo_a_arbol(grafo, nodo_raiz)

    # Crear un grafo vacío usando NetworkX
    grafo_nx = nx.DiGraph()
    nodo_map = {}
    agregar_nodos_y_conexiones(grafo_nx, arbol, nodo_map=nodo_map)

    # Usar graphviz para el layout
    pos = graphviz_layout(grafo_nx, prog='dot')

    plt.figure(figsize=(10, 8))
    labels = {node: data['label'] for node, data in grafo_nx.nodes(data=True)}
    nx.draw(grafo_nx, pos, labels=labels, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
    plt.title("Visualización Jerárquica del Árbol")
    plt.show()
