import pandas as pd
import matplotlib.pyplot as plt 

def clique_size_edges(data, algorithm):
    nodes = data['Nodes']
    percentage_max_num_edges = data['Percentagem']
    basic_operations = data['Different_k']

    plt.scatter(nodes[percentage_max_num_edges == 12],basic_operations[percentage_max_num_edges == 12],c="r",marker="+", label="Edge % = 0.125")
    plt.scatter(nodes[percentage_max_num_edges == 25],basic_operations[percentage_max_num_edges == 25],c="b",marker="o", label="Edge % = 0.25")
    plt.scatter(nodes[percentage_max_num_edges == 50],basic_operations[percentage_max_num_edges == 50],c="g",marker="x", label="Edge % = 0.5")
    plt.scatter(nodes[percentage_max_num_edges == 75],basic_operations[percentage_max_num_edges == 75],c="y",marker="v", label="Edge % = 0.75")

    plt.legend()
    plt.title('Clique size - ' + algorithm)
    plt.xlabel('Edges Number')
    plt.ylabel('Cliques Size')
    plt.show()

def clique_size_vertices(data, algorithm):
    nodes = data['Nodes']
    percentage_max_num_edges = data['Percentagem']
    basic_operations = data['Different_k']

    plt.scatter(nodes[percentage_max_num_edges == 12],basic_operations[percentage_max_num_edges == 12],c="r",marker="+", label="Edge % = 0.125")
    plt.scatter(nodes[percentage_max_num_edges == 25],basic_operations[percentage_max_num_edges == 25],c="b",marker="o", label="Edge % = 0.25")
    plt.scatter(nodes[percentage_max_num_edges == 50],basic_operations[percentage_max_num_edges == 50],c="g",marker="x", label="Edge % = 0.5")
    plt.scatter(nodes[percentage_max_num_edges == 75],basic_operations[percentage_max_num_edges == 75],c="y",marker="v", label="Edge % = 0.75")

    plt.legend()
    plt.title('Clique size - ' + algorithm)
    plt.xlabel('Vertices Number')
    plt.ylabel('Cliques Size')
    plt.show()
    
def basic_operations_num(data, algorithm):
    nodes = data['Nodes']
    percentage_max_num_edges = data['Percentagem']
    basic_operations = data['Basic_Operations']

    plt.scatter(nodes[percentage_max_num_edges == 12],basic_operations[percentage_max_num_edges == 12],c="r",marker="+", label="Edge % = 0.125")
    plt.scatter(nodes[percentage_max_num_edges == 25],basic_operations[percentage_max_num_edges == 25],c="b",marker="o", label="Edge % = 0.25")
    plt.scatter(nodes[percentage_max_num_edges == 50],basic_operations[percentage_max_num_edges == 50],c="g",marker="x", label="Edge % = 0.5")
    plt.scatter(nodes[percentage_max_num_edges == 75],basic_operations[percentage_max_num_edges == 75],c="y",marker="v", label="Edge % = 0.75")

    plt.legend()
    plt.title('Number of Basic Operations - ' + algorithm)
    plt.xlabel('Vertices Number')
    plt.ylabel('Number of Basic Operations')
    plt.show()
    
def execution_times(data, algorithm):
    nodes = data['Nodes']
    percentage_max_num_edges = data['Percentagem']
    basic_operations = data['Time']

    plt.scatter(nodes[percentage_max_num_edges == 12],basic_operations[percentage_max_num_edges == 12],c="r",marker="+", label="Edge % = 0.125")
    plt.scatter(nodes[percentage_max_num_edges == 25],basic_operations[percentage_max_num_edges == 25],c="b",marker="o", label="Edge % = 0.25")
    plt.scatter(nodes[percentage_max_num_edges == 50],basic_operations[percentage_max_num_edges == 50],c="g",marker="x", label="Edge % = 0.5")
    plt.scatter(nodes[percentage_max_num_edges == 75],basic_operations[percentage_max_num_edges == 75],c="y",marker="v", label="Edge % = 0.75")

    plt.legend()
    plt.title('Execution Time - ' + algorithm)
    plt.xlabel('Vertices Number')
    plt.ylabel('Time (s)')
    plt.show()
    
def memory_used(data, algorithm):
    nodes = data['Nodes']
    percentage_max_num_edges = data['Percentagem']
    basic_operations = data['Memory']

    plt.scatter(nodes[percentage_max_num_edges == 12],basic_operations[percentage_max_num_edges == 12],c="r",marker="+", label="Edge % = 0.125")
    plt.scatter(nodes[percentage_max_num_edges == 25],basic_operations[percentage_max_num_edges == 25],c="b",marker="o", label="Edge % = 0.25")
    plt.scatter(nodes[percentage_max_num_edges == 50],basic_operations[percentage_max_num_edges == 50],c="g",marker="x", label="Edge % = 0.5")
    plt.scatter(nodes[percentage_max_num_edges == 75],basic_operations[percentage_max_num_edges == 75],c="y",marker="v", label="Edge % = 0.75")

    plt.legend()
    plt.title('Memory Used - ' + algorithm)
    plt.xlabel('Vertices Number')
    plt.ylabel('Memory (MB)')
    plt.show()
    
if __name__ == "__main__":
    
    df_BF = pd.read_csv('results/results_analise_BF.txt', sep=',')

    basic_operations_num(df_BF, 'Brute Force')
    execution_times(df_BF, 'Brute Force')
    clique_size_vertices(df_BF, 'Brute Force')
    clique_size_edges(df_BF, 'Brute Force')
    memory_used(df_BF, 'Brute Force')

    #df_greedy = pd.read_csv('results_analise_greedy.txt', sep=',')

    #basic_operations_num(df_greedy, 'Heuristic')
    #execution_times(df_greedy, 'Heuristic')
    #clique_size_vertices(df_greedy, 'Heuristic')
    #clique_size_edges(df_greedy, 'Heuristic')
    #memory_used(df_BF, 'Heuristic')
    
