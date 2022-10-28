from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx
import time
import random
from prettytable import PrettyTable

def k_cliques(graph):
    # 2-cliques
    cliques = [{i, j} for i, j in graph.edges() if i != j]
    k = 5

    while cliques:
        # result
        yield k, cliques

        # merge k-cliques into (k+1)-cliques
        cliques_1 = set()
        for u, v in combinations(cliques, 2):
            w = u ^ v
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))

        # remove duplicates
        cliques = list(map(set, cliques_1))
        k += 1

def print_cliques(graph, size_k):
    for k, cliques in k_cliques(graph):
        info = k, len(cliques), cliques[:3]
        #print('%d-cliques = %d, %s.' % (k, len(cliques), cliques))
        
        
    
def print_results(graph) -> None:
    table = PrettyTable()
    table.field_names = ["Vertices", "Edges", "Number os basic Operations", "Time", "Number of Solutions"]
    
    with open('results.txt', 'w') as f:
        for k, cliques in k_cliques(graph):
            info = k, len(cliques), cliques[:3]
            table.add_row([graph.number_of_nodes(), graph.number_of_edges(), graph.number_of_nodes() * graph.number_of_edges(), time.time(), len(cliques)])
            #f.write('%d-cliques = %d, %s.' % (k, len(cliques), cliques))
        f.write(str(table))

if __name__ == '__main__':
    
    #start_1 = time.time()
    nodes, edges = 6, 4
    size_k = 3
    graph = nx.Graph(seed=98491)
    graph.add_nodes_from(range(nodes))
    graph.add_edges_from(combinations(range(nodes), 2))
    
    #ad_matrix = nx.to_numpy_matrix(graph)
    #print(ad_matrix)
    
    print(graph.nodes())
    print(graph.edges())
    
    #maximal_cliques_nodes = list(nx.find_cliques(graph))
    #maximal_cliques_nodes = np.array(maximal_cliques_nodes, dtype=list)
    #print(maximal_cliques_nodes)
    
    
    #random.seed(98491)
    #print(random.random())
    
    print_results(graph)
    
    #pos = nx.spring_layout(graph)
    #nx.draw_networkx_nodes(graph, pos)
    #nx.draw_networkx_labels(graph, pos)
    #nx.draw_networkx_edges(graph, pos, edge_color='r', arrows = True)

    #plt.show()
    #finnish_1 = time.time()
    #3delta_1 = finnish_1 - start_1
    #print("Time: desenhar ", delta_1)

    start_2 = time.time()
    #print_cliques(graph, size_k)
    finnish_2 = time.time()
    delta_2 = finnish_2 - start_2

    #print("Time: algoritmo ", delta_2)