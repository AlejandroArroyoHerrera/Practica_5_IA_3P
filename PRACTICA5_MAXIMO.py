# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:48:16 2024

@author: arroy
"""

import tkinter as tk
#from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

# Función para encontrar el conjunto al que pertenece un nodo
def encontrar(padre, nodo):
    if padre[nodo] == nodo:
        return nodo
    return encontrar(padre, padre[nodo])

# Función para unir dos conjuntos
def unir(padre, rango, nodo1, nodo2):
    raiz1 = encontrar(padre, nodo1)
    raiz2 = encontrar(padre, nodo2)
    if rango[raiz1] > rango[raiz2]:
        padre[raiz2] = raiz1
    elif rango[raiz1] < rango[raiz2]:
        padre[raiz1] = raiz2
    else:
        padre[raiz2] = raiz1
        rango[raiz1] += 1

# Función que implementa el algoritmo de Kruskal para encontrar el árbol de máximo coste
def kruskal_max(aristas, num_nodos):
    aristas = sorted(aristas, key=lambda item: item[2], reverse=True)
    padre = []
    rango = []
    for nodo in range(num_nodos):
        padre.append(nodo)
        rango.append(0)
    arbol_max = []
    for arista in aristas:
        nodo1, nodo2, peso = arista
        raiz1 = encontrar(padre, nodo1)
        raiz2 = encontrar(padre, nodo2)
        if raiz1 != raiz2:
            arbol_max.append(arista)
            unir(padre, rango, raiz1, raiz2)
    return arbol_max

# Función para visualizar el grafo y el árbol de máximo coste
def visualizar_grafo(aristas, arbol_max, num_nodos):
    grafo = nx.Graph()
    grafo.add_weighted_edges_from(aristas)
    pos = nx.spring_layout(grafo)
    plt.figure()
    
    # Dibujar todas las aristas
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    etiquetas = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=etiquetas)
    
    # Dibujar solo las aristas del árbol de máximo coste
    arbol_grafo = nx.Graph()
    arbol_grafo.add_weighted_edges_from(arbol_max)
    nx.draw_networkx_edges(arbol_grafo, pos, edge_color='blue', width=2)
    
    plt.title("Árbol de Máximo Coste usando Kruskal")
    plt.show()

# Función para manejar el evento del botón en la interfaz gráfica
def ejecutar_algoritmo():
    num_nodos = int(entrada_nodos.get())
    aristas = []
    for entrada in entradas_aristas:
        valores = entrada.get().split(',')
        nodo1, nodo2, peso = int(valores[0]), int(valores[1]), float(valores[2])
        aristas.append((nodo1, nodo2, peso))
    arbol_max = kruskal_max(aristas, num_nodos)
    visualizar_grafo(aristas, arbol_max, num_nodos)

# Añadir un campo de entrada de arista
def añadir_entrada_arista():
    entrada = tk.Entry(ventana)
    entrada.pack()
    entradas_aristas.append(entrada)

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Árbol de Máximo Coste - Kruskal")
ventana.geometry("400x300")

# Campo para ingresar el número de nodos
tk.Label(ventana, text="Número de nodos:").pack()
entrada_nodos = tk.Entry(ventana)
entrada_nodos.pack()

# Campos para ingresar las aristas
tk.Label(ventana, text="Aristas (nodo1,nodo2,peso):").pack()
entradas_aristas = []

# Añadir inicialmente 5 campos de entrada para las aristas
for i in range(5):
    añadir_entrada_arista()

# Botón para añadir más campos de entrada de aristas
boton_añadir = tk.Button(ventana, text="Añadir arista", command=añadir_entrada_arista)
boton_añadir.pack()

# Botón para ejecutar el algoritmo
boton = tk.Button(ventana, text="Ejecutar", command=ejecutar_algoritmo)
boton.pack()

ventana.mainloop()