from Graph import Graph
import numpy as np
import networkx as nx


def adj_list_to_matrix(adj_list):
    nodes = list(adj_list.keys())
    n = len(nodes)
    adj_matrix = [[0 for i in range(n)] for j in range(n)]
    
    for node in adj_list:
        row_index = nodes.index(node)
        for neighbor in adj_list[node]:
            col_index = nodes.index(neighbor[0])
            adj_matrix[row_index][col_index] = 1
            
    return adj_matrix, nodes


graph = {
    'Arad': ['Zerind', 'Sibiu', 'Timisoara'],
    'Zerind': ['Oradea', 'Arad'],
    'Oradea': ['Zerind', 'Sibiu'],
    'Timisoara': ['Arad', 'Lugoj'],
    'Lugoj': ['Timisoara', 'Mehadia'],
    'Mehadia': ['Lugoj', 'Drobeta'],
    'Drobeta': ['Mehadia', 'Craiova'],
    'Craiova': ['Drobeta', 'Rimnicu Vilcea', 'Pitesti'],
    'Rimnicu Vilcea': ['Craiova', 'Sibiu', 'Pitesti'],
    'Sibiu': ['Oradea', 'Arad', 'Fagaras', 'Rimnicu Vilcea'],
    'Fagaras': ['Sibiu', 'Bucharest'],
    'Pitesti': ['Craiova', 'Rimnicu Vilcea', 'Bucharest'],
    'Bucharest': ['Fagaras', 'Pitesti', 'Urziceni', 'Giurgiu'],
    'Urziceni': ['Bucharest', 'Hirsova', 'Vaslui'],
    'Eforie': ['Hirsova'],
    'Hirsova': ['Urziceni', 'Eforie'],
    'Vaslui': ['Urziceni', 'Iasi'],
    'Iasi': ['Vaslui', 'Neamt'],
    'Neamt': ['Iasi'],
    'Giurgiu': ['Bucharest']
}

degree_centrality = {}
for node in graph:
    degree_centrality[node] = len(graph[node])

print("Degree Centrality:")
for node, degree in degree_centrality.items():
    print(f"{node}: {degree}")



def eigenvector_centrality(adj_matrix, tol=1e-6):
    n = len(adj_matrix)
    x = np.ones(n)
    x /= np.linalg.norm(x)

    while True:
        x_new = np.dot(adj_matrix, x)
        x_new /= np.linalg.norm(x_new)
        if np.abs(np.dot(x_new, x) - 1) < tol:
            break
        x = x_new

    return x_new


def katz_centrality(adj_matrix, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-6):
    n = len(adj_matrix)
    x = np.zeros(n)
    b = np.full(n, beta)
    I = np.identity(n)

    for _ in range(max_iter):
        x_new = alpha * np.dot(adj_matrix, x) + b
        err = np.linalg.norm(x_new - x)
        if err < tol:
            break

        x = x_new

    x /= np.linalg.norm(x)
    centrality = {i: x[i] for i in range(n)}

    return centrality


def pagerank(M, num_iterations: int = 100, d: float = 0.85):
    """PageRank algorithm with explicit number of iterations. Returns ranking of nodes (pages) in the adjacency matrix.

    Parameters
    ----------
    M : numpy array
        adjacency matrix where M_i,j represents the link from 'j' to 'i', such that for all 'j'
        sum(i, M_i,j) = 1
    num_iterations : int, optional
        number of iterations, by default 100
    d : float, optional
        damping factor, by default 0.85

    Returns
    -------
    numpy array
        a vector of ranks such that v_i is the i-th rank from [0, 1],
        v sums to 1

    """
    M = np.array(M)
    N = M.shape[1]
    v = np.ones(N) / N
    M_hat = (d * M + (1 - d) / N)
    for i in range(num_iterations):
        v = M_hat @ v
    return v

graph = nx.Graph()
a = Graph()
a.insertEdge('Oradea','Sibiu', 151 )
a.insertEdge('Oradea','Zerind', 71)
a.insertEdge('Zerind','Arad', 75)
a.insertEdge('Arad','Sibiu', 140)
a.insertEdge('Arad','Timisoara', 118)
a.insertEdge('Sibiu','Fagaras', 99)
a.insertEdge('Sibiu','Rimnicu Vilcea', 80)
a.insertEdge('Timisoara','Lugoj', 111)
a.insertEdge('Lugoj','Mehadia', 70)
a.insertEdge('Mehadia','Drobeta', 75)
a.insertEdge('Drobeta','Craiova', 120)
a.insertEdge('Craiova','Pitesti', 138)
a.insertEdge('Rimnicu Vilcea','Pitesti', 97)
a.insertEdge('Rimnicu Vilcea', 'Craiova', 146)
a.insertEdge('Fagaras', 'Bucharest', 211)
a.insertEdge('Pitesti', 'Bucharest', 101)
a.insertEdge('Bucharest', 'Urziceni', 85)
a.insertEdge('Bucharest', 'Giurgiu', 90)
a.insertEdge('Urziceni', 'Hirsova', 98)
a.insertEdge('Urziceni', 'Vaslui', 142)
a.insertEdge('Hirsova', 'Eforie', 86)
a.insertEdge('Vaslui', 'Iasi', 92)
a.insertEdge('Iasi', 'Neamt', 87)

adj_matrix, nodes = adj_list_to_matrix(a.graph)
g2 = nx.Graph()
for i in range(len(adj_matrix)):
    for j in range(i+1, len(adj_matrix[i])):
        if adj_matrix[i][j] != 0:
            g2.add_edge(i, j)
# print(adj_list_to_matrix(a.graph))
print(nx.eigenvector_centrality(g2),"using nx")
print(eigenvector_centrality(adj_matrix))

print(nx.katz_centrality(g2), "using nx for katz")
print(katz_centrality(adj_matrix))

print(pagerank(adj_matrix),"page rank")
# centrality_scores = nx.katz_centrality(adj_matrix)
# print(centrality_scores, "katz fist")

# print(eigenvector_centrality(adj_list_to_matrix(a.graph)))
# print(katz_centrality(adj_list_to_matrix(a.graph)), "katz")
# print(nx.eigenvector_centrality(graph))
