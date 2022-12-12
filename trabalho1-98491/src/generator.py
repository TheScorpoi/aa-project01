from src.vertex import Vertex
from src.point import Point
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import argparse
import collections
import psutil

random.seed(98491)

def generate_graph(vertexs_number: int, percentage: int):
    
    points = [(Point(random.randint(1, 20), random.randint(1, 20))) for i in range(vertexs_number)]
    vertexs = [(Vertex(i, points[i])) for i in range(vertexs_number)]
    vertex_label = [vertex.id for vertex in vertexs]

    edges_number = round(((vertexs_number*(vertexs_number-1))/2)*(percentage/100))
    edges = list()
    visited = list()
    adj_list = dict()
    unvisited = vertex_label
    
    for i in range(edges_number):
        if len(edges) == 0:  # initial case: pick 2 random unvisited vertexes to form the first edge
            two_random_vertexs = random.sample(unvisited, 2)
            edges.append(tuple(sorted(two_random_vertexs)))
            unvisited = list(set(unvisited) - set(two_random_vertexs))
            visited = list(set(visited).union(two_random_vertexs))
        elif len(unvisited) != 0:  # general case:
            vertex_1 = random.choice(unvisited)
            vertex_2 = random.choice(visited)
            edges.append(tuple(sorted([vertex_1, vertex_2])))
            unvisited.remove(vertex_1)
        else:
            edges.append(tuple(sorted(random.sample(vertex_label[:vertexs_number], 2))))
            
    # generate adjacency list
    for node1, node2 in sorted(edges):
        if node1 in adj_list:
            adj_list[node1].append(node2)
        else:
            adj_list[node1] = [node2]
        if node2 in adj_list:
            adj_list[node2].append(node1)
        else:
            adj_list[node2] = [node1]

    return vertexs, edges, adj_list

def plot_graph(e):
    G = nx.Graph()
    for edge in e:
        G.add_edge(edge[0], edge[1])
    nx.draw(G, node_size=700, with_labels=True)
    plt.show()

def p_clique(graph, k):
    basic_op = 1
    if k==0:
        return False, basic_op
    if k==1 or k == 2:
        return True, basic_op
    vertices = list(graph.keys())
    for i in range(1, len(graph)):
        clique = []
        clique.append(vertices[i])
        basic_op += 1
        for v in vertices:
            initial = v
            if v in clique:
                basic_op += 1
                continue
            for u in clique:
                basic_op += 1
                if u in graph[v]:
                    isNext = True
                    continue
                else:
                    if u == initial:
                        continue
                    isNext = False
                    break
            if isNext:
                clique.append(v)
                if k <= len(clique):
                    return True, basic_op
    if k <= len(clique):
        return True, basic_op
    else:
        return False, basic_op

def get_adj_list_in_a_set(graph):
    neighbors = collections.defaultdict(set)
    for vertice, adajacent_vertices in graph.items():
        for a_d in adajacent_vertices:
            if a_d != vertice:
                neighbors[a_d].add(vertice)
                neighbors[vertice].add(a_d)
    return neighbors

def pick_random(s):
    if s:
        elem = s.pop()
        s.add(elem)
        return elem

def bron_kerbosch(clique, candidates, excluded, NEIGHBORS):
    '''Bron–Kerbosch algorithm with pivot'''
    global counter, cliques_list
    counter += 1
    if not candidates and not excluded:
        if len(clique) >= 1:
            cliques_list.append(clique)
        return
 
    pivot = pick_random(candidates) or pick_random(excluded)
    for v in list(candidates.difference(NEIGHBORS[pivot])):
        new_candidates = candidates.intersection(NEIGHBORS[v])
        new_excluded = excluded.intersection(NEIGHBORS[v])
        bron_kerbosch(clique + [v], new_candidates, new_excluded, NEIGHBORS)
        candidates.remove(v)
        excluded.add(v)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("K-Cliques Problem")
    parser.add_argument("-r", type=str, help="Resolution type: BF-Search or Heuristic")
    parser.add_argument("-n", type=int, default=20, help="Number of vertexs, default=15")
    parser.add_argument("-p", type=int, default=25, help="Percentage of edges, default=50, can be: 12.5, 25, 50, 75")
    parser.add_argument("-k", type=int, default=25, help="Percentage of edges, default=3, can be: 12.5, 25, 50, 75")
    parser.add_argument("-d", type=int, default=0, help="Draw the graph: 0 - No, 1 - Yes")
    parser.add_argument("-pt", type=int, default=0, help="PrettyTable: 0 - No, 1 - Yes")
    args = parser.parse_args()
    
    if args.r == "BF-Search":
        table = PrettyTable()
        table.field_names = ["Number of Nodes", "%", "Number of Edges", "(%) k", "k", "Clique size k?", "Basic Operations", "Time", "Memory"]
        if args.pt == 1:
            with open('results/results_BF.txt', 'w') as f:
                for i in range(5, 80):
                    for p in [12.5, 25, 50, 75]:
                        v,e, adj_list = generate_graph(i, p)
                        graph = nx.Graph()
                        for edge in e:
                            graph.add_edge(edge[0],edge[1])
                        for j in [12.5, 25, 50, 75]:
                            A = time.time()
                            mem1 = psutil.virtual_memory().used # total physical memory in Bytes
                            k = int(i * j / 100)
                            counter = 0
                            cliques_list = []
                            neighbors = get_adj_list_in_a_set(adj_list)
                            bron_kerbosch([], set(graph.nodes()), set(), neighbors)
                            result = False
                            for cliq in cliques_list:
                                if len(cliq) == k or k==1:
                                    result = True
                                    break
                            mem2 = psutil.virtual_memory().used  # total physical memory in Bytes
                            table.add_row([i, p, len(e), j, k, result, counter,  time.time() - A, abs(mem2 - mem1)/2**(20)])
                f.write(str(table))
            if args.d == 1:
                plot_graph(e)
        if args.pt == 0:
            with open('results/results_analise_BF.txt', 'w') as f:
                f.write("Nodes,Percentagem,Edges,Perc_k,k,Result,Basic_Operations,Time,Memory\n")
                for i in range(5, 80):
                    for p in [12.5, 25, 50, 75]:
                        v,e, adj_list = generate_graph(i, p)
                        graph = nx.Graph()
                        for edge in e:
                            graph.add_edge(edge[0],edge[1])
                        for j in [12.5, 25, 50, 75]:
                            A = time.time()
                            mem1 = psutil.virtual_memory().used # total physical memory in Bytes
                            k = int(i * j / 100)
                            counter = 0
                            cliques_list = []
                            neighbors = get_adj_list_in_a_set(adj_list)
                            bron_kerbosch([], set(graph.nodes()), set(), neighbors)
                            result = False
                            for cliq in cliques_list:
                                if len(cliq) == k or k==1:
                                    result = True
                                    break
                            mem2 = psutil.virtual_memory().used  # total physical memory in Bytes
                            f.write(str(i) + "," + str(p) + "," + str(len(e)) + "," + str(j) + "," + str(k) + "," + str(result) + "," + str(counter) + "," + str(time.time() - A) + "," + str((abs(mem2 - mem1))/2**(20)) + "\n")
            if args.d == 1:
                plot_graph(e)
    
    if args.r == "Heuristic":
        if args.pt == 1:
            table = PrettyTable()
            table.field_names = ["Number of Nodes", "%", "Number of Edges", "(%) k", "k", "Clique size k?", "Basic Operations", "Time", "Memory"]
            with open('results/results_greedy2.txt', 'w') as f:
                for i in range(5, 80):
                    for p in [12.5, 25, 50, 75]:
                        v,e, adj_list = generate_graph(i, p)
                        graph = nx.Graph()
                        for edge in e:
                            graph.add_edge(edge[0],edge[1])
                        A = time.time()
                        for j in [12, 25, 50, 75]:
                            mem1 = psutil.virtual_memory().used # total physical memory in Bytes
                            k = int(i * j / 100)
                            result, basic_op = p_clique(adj_list, k)
                            mem2 = psutil.virtual_memory().used  # total physical memory in Bytes
                            table.add_row([i, p,len(e), j, k, result, basic_op, time.time() - A, abs(mem2 - mem1)/2**(20)])
                f.write(str(table))
        else:
            with open('results/results_analise_greedy.txt', 'w') as f_analise:
                f_analise.write("Nodes,Percentagem,Edges,Perc_k,k,Result,Basic_Operations,Time,Memory\n")
                for i in range(5, 80):
                    for p in [12.5, 25, 50, 75]:
                        v,e, adj_list = generate_graph(i, p)
                        graph = nx.Graph()
                        for edge in e:
                            graph.add_edge(edge[0],edge[1])
                        A = time.time()
                        k = 0
                        for j in [12, 25, 50, 75]:
                            k = int(i * j / 100)
                            mem1 = psutil.virtual_memory().used # total physical memory in Bytes
                            result, basic_op = p_clique(adj_list, k)
                            mem2 = psutil.virtual_memory().used  # total physical memory in Bytes
                            f_analise.write(str(i) + "," + str(p) + "," + str(len(e)) + "," + str(j)+ "," + str(k) + "," + str(result) + "," + str(basic_op) + "," + str(time.time() - A) + "," + str((abs(mem2 - mem1))/2**(20)) + "\n")
        if args.d == 1:
            plot_graph(e)