from vertex import Vertex
from point import Point
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from prettytable import PrettyTable
import argparse

def generate_graph(vertexs_number: int, percentage: int):
    random.seed(98491)
        
    points = [(Point(random.randint(1,20), random.randint(1,20))) for i in range(vertexs_number)]
    vertexs = [(Vertex(i, points[i])) for i in range(vertexs_number)]
    vertex_label = [vertex.id for vertex in vertexs]

    edges_number = int(max((vertexs_number*(vertexs_number-1)/2)*(percentage/100), vertexs_number-1))    
    edges = set()
    visited = list()
    unvisited = vertex_label
    
    for i in range(edges_number):
        if len(edges) == 0: #initial case: pick 2 random unvisited vertexes to form the first edge
            two_random_vertexs = random.sample(unvisited, 2)
            edges.add(tuple(sorted(two_random_vertexs)))
            unvisited = list(set(unvisited) - set(two_random_vertexs))
            visited = list(set(visited).union(two_random_vertexs))
        elif len(unvisited) != 0: #general case:
            vertex_1 = random.choice(unvisited)
            vertex_2 = random.choice(visited)
            edges.add(tuple(sorted([vertex_1,vertex_2])))
            unvisited.remove(vertex_1)
        else:
            edges.add(tuple(sorted(random.sample(vertex_label[:vertexs_number], 2))))
            
    return vertexs, edges

def k_cliques(graph):
    cliques = [{i, j} for i, j in graph.edges() if i != j]
    k = 2  #initial k
    delta = 0
    number_of_solutions = 0
    number_of_basic_operations = 0

    while cliques:
        # result
        yield k, cliques, delta, number_of_solutions, number_of_basic_operations
        
        number_of_solutions = 0
        number_of_basic_operations = 0
        
        initial = time.time()
        # merge k-cliques into (k+1)-cliques
        cliques_1 = set()
        for u, v in combinations(cliques, 2):
            number_of_basic_operations += 1
            w = u ^ v
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))
                number_of_solutions += 1
        # remove duplicates
        cliques = list(map(set, cliques_1))
        delta = time.time() - initial
        k += 1
        
def print_results_BF(graph) -> None:
    table = PrettyTable()
    table.field_names = ["k", "Number of Cliques", "Number os basic Operations", "Time", "Number of Solutions"]
    
    with open('results.txt', 'w') as f:
        i = 0
        for k, cliques, delta, number_of_solutions, number_of_basic_operations in k_cliques(graph):
            table.add_row([k, len(cliques), number_of_basic_operations, delta, number_of_solutions])
            print(table)
        i+=1
        f.write(str(table))

def plot_graph(e):
    G = nx.Graph()
    for edge in e:
        G.add_edge(edge[0],edge[1])
    nx.draw(G, node_size=700 , with_labels=True)
    plt.show()
    
def get_keys_array(dict):
    result = []
    for key in dict.keys():
        result.append(key)
    return result

def p_clique (graph, k, v):
    if k == 1:
        return True
    clique = []
    vertices = v
    max_ln=0
    max_dict=[]
    for i in range (0,len(graph)):
        clique= []
        clique.append (vertices [i])
        for v in vertices:
            if v in clique:
                continue
            isNext = True
            for u in clique:
                if graph.has_edge(u,v):
                    continue 
                else:
                    isNext = False
                    break
            if isNext:
                clique.append (v)
                if k <= len (clique):
                    return True
        if len (clique) > max_ln:
            max_ln=len (clique)
            max_dict=clique
    if k <= len (clique):
        print(clique)
        return True
    else:
        print(clique)
        return False

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("K-Cliques Problem")
    parser.add_argument("-r", type=str, help="Resolution type: BF-Search or Heuristic")
    parser.add_argument("-n", type=int, default=15, help="Number of vertexs, default=15")
    parser.add_argument("-p", type=int, default=50, help="Percentage of edges, default=50, can be: 12.5, 25, 50, 75")
    parser.add_argument("-d", type=int, default=0, help="Draw the graph: 0 - No, 1 - Yes")
    parser.add_argument("-t", type=int)
    args = parser.parse_args()
    
    #create graph
    A = time.time()
    v,e = generate_graph(args.n, args.p)
    graph = nx.Graph()
    for edge in e:
        graph.add_edge(edge[0],edge[1])
        
    if args.t == 1:
        print(p_clique(graph, 2, v))
    
    if args.r == "BF-Search":
        print_results_BF(graph)
        print("Time: ", time.time() - A)
        if args.d == 1:
            plot_graph(e)
    
    if args.r == "Heuristic":
        print("Heuristic")
        print("Time: ", time.time() - A)
        if args.d == 1:
            plot_graph(e)