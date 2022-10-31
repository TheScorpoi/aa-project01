from pydoc import cli
from vertex import Vertex
from point import Point
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from prettytable import PrettyTable
import argparse
import collections

def generate_graph(vertexs_number: int, percentage: int):
    random.seed(98491)

    points = [(Point(random.randint(1, 20), random.randint(1, 20))) for i in range(vertexs_number)]
    vertexs = [(Vertex(i, points[i])) for i in range(vertexs_number)]
    vertex_label = [vertex.id for vertex in vertexs]

    edges_number = int(max((vertexs_number*(vertexs_number-1)/2)*(percentage/100), vertexs_number-1))
    edges = set()
    visited = list()
    adj_list = dict()
    unvisited = vertex_label

    for i in range(edges_number):
        if len(edges) == 0:  # initial case: pick 2 random unvisited vertexes to form the first edge
            two_random_vertexs = random.sample(unvisited, 2)
            edges.add(tuple(sorted(two_random_vertexs)))
            unvisited = list(set(unvisited) - set(two_random_vertexs))
            visited = list(set(visited).union(two_random_vertexs))
        elif len(unvisited) != 0:  # general case:
            vertex_1 = random.choice(unvisited)
            vertex_2 = random.choice(visited)
            edges.add(tuple(sorted([vertex_1, vertex_2])))
            unvisited.remove(vertex_1)
        else:
            edges.add(
                tuple(sorted(random.sample(vertex_label[:vertexs_number], 2))))
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

def k_cliques(graph, k):
    cliques = [{i, j} for i, j in graph.edges() if i != j]
    k = k
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
            number_of_solutions += 1
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))
                # print("cliques_1: ", k ,"   ", cliques_1)
        # remove duplicates
        cliques = list(map(set, cliques_1))
        delta = time.time() - initial
        k += 1

def print_results_BF(graph, k) -> None:
    table = PrettyTable()
    table.field_names = ["k", "Number of Cliques",
        "Number os basic Operations", "Time", "Number of Solutions"]

    with open('results.txt', 'w') as f:
        i = 0
        for k, cliques, delta, number_of_solutions, number_of_basic_operations in k_cliques(graph, k):
            table.add_row(
                [k, len(cliques), number_of_basic_operations, delta, number_of_solutions])
        i += 1
        f.write(str(table))

def plot_graph(e):
    G = nx.Graph()
    for edge in e:
        G.add_edge(edge[0], edge[1])
    nx.draw(G, node_size=700, with_labels=True)
    plt.show()

def get_keys_array(dict):
    result = []
    for key in dict.keys():
        result.append(key)
    return result

def find_clique_greedy(graph):
    clique = []
    vertices = list(graph.keys())
    rand = random.randrange(0, len(vertices), 1)
    clique.append(vertices[rand])
    # print("clique inicial: ", clique)
    for v in vertices:
        # print("v: ", v)
        if v in clique:
            continue
        isNext = True
        for u in clique:
            if u in graph[v]:
                continue
            else:
                isNext = False
                break
        if isNext:
           clique.append(v)
    return sorted(clique)

def p_clique(graph, k):
    if k == 1:
        return True
    clique = []
    vertices = get_keys_array(graph)
    max_ln = 0
    max_dict = []
    for i in range(0, len(graph)):
        clique = []
        clique.append(vertices[i])
        for v in vertices:
            if v in clique:
                continue
            isNext = True
            for u in clique:
                if u in graph[v]:
                    continue
                else:
                    isNext = False
                    break
            if isNext:
                clique.append(v)
                if k <= len(clique):
                    return True
        if len(clique) > max_ln:
            max_ln = len(clique)
            max_dict = clique
    if k <= len(clique):
        return True
    else:
        return False

def cliques_recursive(neighbors, r, p, x):
    if not p and not x:
        yield r
    else:
        for v in min((p - neighbors[u] for u in p | x), key=len):
            yield from cliques_recursive(
                neighbors, r | {v}, p & neighbors[v], x & neighbors[v]
            )
            p.remove(v)
            x.add(v)

def cliques(graph):
    neighbors = collections.defaultdict(set)
    for vertice, adacent_vertices in graph.items():
        for a_d in adacent_vertices:
            if a_d != vertice:
                neighbors[a_d].add(vertice)
                neighbors[vertice].add(a_d)
    yield from cliques_recursive(neighbors, set(), set(neighbors), set())

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("K-Cliques Problem")
    parser.add_argument("-r", type=str, help="Resolution type: BF-Search or Heuristic")
    parser.add_argument("-n", type=int, default=20, help="Number of vertexs, default=15")
    parser.add_argument("-p", type=int, default=25, help="Percentage of edges, default=50, can be: 12.5, 25, 50, 75")
    parser.add_argument("-k", type=int, default=25, help="Percentage of edges, default=3, can be: 12.5, 25, 50, 75")
    parser.add_argument("-d", type=int, default=0, help="Draw the graph: 0 - No, 1 - Yes")
    parser.add_argument("-t", type=int)
    args = parser.parse_args()
    
    #create graph
    A = time.time()
    v,e, adj_list = generate_graph(args.n, args.p)
    graph = nx.Graph()
    for edge in e:
        graph.add_edge(edge[0],edge[1])
        
    if args.t == 1:
        #print(find_clique_greedy(adj_list))
        #print(p_clique(adj_list, 2))
        #plot_graph(e)
        #print(list(nx.find_cliques_recursive(graph)))
        #plot_graph(e)
        for c in cliques(adj_list):
            print(c)
        result = list(set(len(c) for c in cliques(adj_list)))
        print(result)
        #plot_graph(e)
        
    k = int(args.n * (args.k / 100))
    #print(k)
    
    if args.r == "BF-Search":
        #print("Graph with ", args.n, " nodes and ", len(e), " edges has these cliques of size", result, "and it takes", time.time() - A , "seconds to find them")
        table = PrettyTable()
        table.field_names = ["Number of Nodes", "%","Number of Edges", "Cliques", "Different k","Time"]
        with open('results.txt', 'w') as f:
            for i in range(5, 200):
                for p in [12, 25, 50, 75]:
                    v,e, adj_list = generate_graph(i, p)
                    graph = nx.Graph()
                    for edge in e:
                        graph.add_edge(edge[0],edge[1])
                    A = time.time()
                    result = list(set(len(c) for c in cliques(adj_list)))
                    table.add_row([i, p,len(e), result, len(result), time.time() - A])
            print(table)
            f.write(str(table))
            
        with open('results_analise.txt', 'a') as f_analise:
            for i in range(5, 200):
                for p in [12, 25, 50, 75]:
                    v,e, adj_list = generate_graph(i, p)
                    graph = nx.Graph()
                    for edge in e:
                        graph.add_edge(edge[0],edge[1])
                    A = time.time()
                    result = list(set(len(c) for c in cliques(adj_list)))
                    f_analise.write([i, p,len(e), result, len(result), time.time() - A])
            print(table)
            f.write(str(table))        
    
        
        if args.d == 1:
            plot_graph(e)
    
    if args.r == "Heuristic":
        print("Heuristic")
        print("Time: ", time.time() - A)
        if args.d == 1:
            plot_graph(e)