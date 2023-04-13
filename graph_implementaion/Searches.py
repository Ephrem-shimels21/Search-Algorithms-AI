from collections import deque
from Graph import Graph
import heapq
import math
import random
import matplotlib.pyplot as plt
import time
import random
import networkx as nx


def dfs(adj_list, start, end, path = []):
    path = path + [start]
    if start == end:
        return path
    for node in adj_list[start]:
        if node[0] not in path:
            new_path = dfs(adj_list, node[0], end, path)
            if new_path:
                return new_path
    return None
def iterative_deepening_search(graph, start_node, goal_node, max_depth):
    for depth in range(max_depth + 1):
        visited = set()
        result = depth_limited_search(
            graph, start_node, goal_node, visited, depth)
        if result is not None:
            return result
    return None
def depth_limited_search(graph, current_node, goal_node, visited, depth):
    if depth == 0:
        if current_node == goal_node:
            return [current_node]
        else:
            return None
    elif depth > 0:
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                result = depth_limited_search(
                    graph, neighbor, goal_node, visited, depth - 1)
                if result is not None:
                    return [current_node] + result
    return None
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



Data = {}
with open("./citys.txt","r") as file:
    for line in file:
        line = line.split()
        if len(line) > 3:
            Data[f"{line[0]} {line[1]}"] = (line[2], line[3])
        else:
            Data[line[0]] = (line[1],line[2])
del Data['City']

def Heuristic(node_A, node_B, cityData):
    """"
    calculates the distance between the two cities in km using Haversine formula
    """
    long1, lat1, long2, lat2 = map(math.radians, [float(cityData[node_A][1]), float(cityData[node_A][0]),float(cityData[node_B][0]) * (math.pi / 180), float(cityData[node_B][0])])

    dlon = long2 - long1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    r = 6371      # Radius of earth in kilometers.
    distance = c * r

    return distance

def find_taken_distance(path, graph):
    final_cost = 0
    visited = set()
    for i in range(len(path)):
        if i + 1 < len(path):
            for node in path:
                for neigbor in graph[node]:
                    if path[i + 1] == neigbor[0] and path[i + 1] not in visited:
                        visited.add(neigbor[0])
                        final_cost += neigbor[1]
    return final_cost

def astar(start_node, end_node, graph, lat_long_dict):
    fringe = []
    visited = set()
    parent = {}
    actual_cost = {start_node: 0}
    total_estimated_cost = {start_node: Heuristic(start_node, end_node, lat_long_dict)}

    heapq.heappush(fringe, (total_estimated_cost[start_node], start_node))

    while fringe:
        current_node = heapq.heappop(fringe)[1]

        if current_node == end_node:
            path = []
            while current_node in parent:
                path.append(current_node)
                current_node = parent[current_node]
            path.append(start_node)
            return path[::-1], find_taken_distance(path[::-1], graph)

        visited.add(current_node)

        for neighbor, cost in graph[current_node]:
            if neighbor in visited:
                continue

            tentative_actual_cost = actual_cost[current_node] + cost
            if neighbor not in actual_cost or tentative_actual_cost < actual_cost[neighbor]:
                parent[neighbor] = current_node
                actual_cost[neighbor] = tentative_actual_cost
                total_estimated_cost[neighbor] = tentative_actual_cost + \
                    Heuristic(neighbor, end_node, lat_long_dict)
                heapq.heappush(fringe, (total_estimated_cost[neighbor], neighbor))

    return None

cities = list(Data.keys())
randomCities = []
while len(randomCities) < 11:
    randomCities.append(cities[random.randint(0, 19)])

if __name__=="__main__":
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
    a.locations = Data
    path, cost = astar("Arad", "Bucharest", a.graph , a.locations)
