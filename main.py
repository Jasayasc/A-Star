import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

# Variables globales para almacenar el grafo y los nombres de los nodos
G = nx.Graph()
node_names = []


def set_node_count():
    try:
        count = int(entry_node_count.get())
        if count <= 0:
            raise ValueError
        create_node_names(count)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido de nodos mayor a 0.")


def create_node_names(count):
    global node_names
    node_names = []

    # Pedir al usuario que ingrese los nombres de los nodos
    for i in range(count):
        name = simpledialog.askstring("Nombre del Nodo", f"Ingrese el nombre para el nodo {i + 1}:")
        if name:
            node_names.append(name)
        else:
            messagebox.showerror("Error", "Debe ingresar un nombre válido para cada nodo.")
            return

    # Crear nodos con los nombres ingresados
    G.clear()
    G.add_nodes_from(node_names)
    # Mostrar el panel para añadir aristas
    show_edge_input_panel()


def show_edge_input_panel():
    # Limpiar ventana actual y preparar para la entrada de aristas
    for widget in window.winfo_children():
        widget.destroy()

    tk.Label(window, text="Agregar Aristas y Pesos").pack(pady=10)

    # Comboboxes para seleccionar nodos por nombre y campo para peso
    global node1_combobox, node2_combobox, entry_weight
    node1_combobox = ttk.Combobox(window, values=node_names, state="readonly")
    node1_combobox.pack(pady=5)
    node1_combobox.set("Nodo 1")

    node2_combobox = ttk.Combobox(window, values=node_names, state="readonly")
    node2_combobox.pack(pady=5)
    node2_combobox.set("Nodo 2")

    entry_weight = tk.Entry(window)
    entry_weight.pack(pady=5)
    entry_weight.insert(0, "Peso")

    tk.Button(window, text="Agregar Arista", command=add_edge).pack(pady=5)
    tk.Button(window, text="Ejecutar A* en Árbol de Decisión", command=run_astar_on_tree).pack(pady=5)


def add_edge():
    # Agregar arista al grafo con los nodos y peso especificados
    try:
        node1 = node1_combobox.get()
        node2 = node2_combobox.get()
        weight = float(entry_weight.get())

        if node1 == node2:
            messagebox.showwarning("Aviso", "No se pueden conectar nodos iguales.")
            return

        G.add_edge(node1, node2, weight=weight)
        messagebox.showinfo("Éxito", f"Arista añadida: {node1} - {node2} con peso {weight}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos para los nodos y el peso.")


def graph_to_decision_tree(graph):
    decision_tree = nx.DiGraph()
    visited = set()
    queue = deque()
    parent = {}  # Diccionario para almacenar el padre de cada nodo

    root = list(graph.nodes())[0]
    queue.append(root)
    visited.add(root)

    while queue:
        current = queue.popleft()
        children = list(graph.neighbors(current))
        children = [child for child in children if child not in visited and child != parent.get(current)]

        for child in children[:2]:  # Tomar los primeros dos hijos válidos
            decision_tree.add_edge(current, child)
            visited.add(child)
            parent[child] = current
            queue.append(child)

    return decision_tree


def run_astar_on_tree():
    # Construir el árbol de decisión a partir del grafo
    decision_tree = graph_to_decision_tree(G)

    start = simpledialog.askstring("Nodo de inicio", "Ingrese el nombre del nodo de inicio:")
    end = simpledialog.askstring("Nodo de fin", "Ingrese el nombre del nodo de fin:")

    if start not in decision_tree.nodes() or end not in decision_tree.nodes():
        messagebox.showerror("Error", "Los nodos de inicio o fin no son válidos.")
        return

    try:
        # Ejecutar A* en el árbol de decisión con heurística nula
        path = nx.astar_path(decision_tree, start, end, heuristic=lambda u, v: 0, weight='weight')
        messagebox.showinfo("Resultado", f"Camino encontrado en el Árbol de Decisión: {path}")
        draw_graph(decision_tree, path)
    except nx.NetworkXNoPath:
        messagebox.showwarning("Sin camino", "No hay un camino disponible entre los nodos seleccionados.")


def draw_graph(G, path=None):
    # Dibujar el grafo utilizando Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, ax=ax, node_color='lightblue', node_size=500, font_size=10)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax, edge_color='red', width=2)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Configuración inicial de la ventana Tkinter
window = tk.Tk()
window.title("Aplicación A* en Árbol de Decisión")

# Panel para definir la cantidad de nodos
tk.Label(window, text="Ingrese la cantidad de nodos:").pack(pady=10)
entry_node_count = tk.Entry(window)
entry_node_count.pack(pady=5)
tk.Button(window, text="Definir Nodos", command=set_node_count).pack(pady=5)

window.mainloop()
