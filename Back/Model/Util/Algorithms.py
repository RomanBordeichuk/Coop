from numpy.lib.function_base import delete
import osmnx
import networkx as nx
from queue import LifoQueue, PriorityQueue
from itertools import compress
from numpy import invert
from operator import itemgetter
from .NodeInstance import Node
from .RoadInstance import Road
from .dijkstra import find_shortest_path
from .Consts import *
import math
import time

# class SegmentedTree:
#     class Node:
#         pass


class GraphAlgorithms:
    """ Graph threory algorithms
    """

    @staticmethod
    def dfs(adjusting_matrix, nodes, visited, first_node = 0):
        """Deepth-first search


        Args:
            adjusting_matrix (list[list[[int, Road]]]): distances_matrix
            nodes (list[Node]): nodes
            edges (list[Road]): edges (unnecessary)
            first_node (int): the first node from which we will make the dfs

        Returns:
            [int, list[Node], int]: number of visited nodes, list of visited nodes, the first unsearched node (in the worst case = 1) 
        """
        # visited = [False] * len(nodes)
        visited_number = 0
        visited_list = []
        q = LifoQueue(maxsize = len(nodes))

        q.put(first_node)

        while not q.empty():
            vertex = q.get()
            if not visited[vertex]:
                visited[vertex] = True
                visited_number += 1
                visited_list.append(vertex)
                for vertex_index in adjusting_matrix[vertex]:
                    q.put(vertex_index)
        

        for index, visit in enumerate(visited):
            if visit == False:
                first_node = index
                break
        
        return [visited_number, list(compress(nodes, visited)), first_node, visited] # number, visited list, unvisited list
    
    @staticmethod
    def dijkstra(distance_matrix, v, u):
        """ dijkstra by Cristian Bastidas
            Nothing special
            Why'd I use application of dijkstra by someone, who's not in our group?
            Answer is so simple: I'm lazy

        Args:
            distance_matrix (list[list[[int, Road]]]): matrix w/ distances
            v (int): start node
            u (int): end node
        """

        return find_shortest_path(distance_matrix, v, u)
        

    @staticmethod
    def getBiggestComponent(adjusting_matrix, nodes):
        """getting the Biggest linked component

        Args:
            adjusting_matrix (list[list[[int, Road]]]): matrix w/ distances
            nodes (list[Node]): nodes
            edges (list[Road]): roads

        Returns:
            list[Node]: the nodes from the biggest component
        """
        visited_number = 0
        first_node = 0
        components = []
        visited_list = [False] * len(nodes)

        while visited_number < len(nodes) - 1:
            number, visited_nodes, first_node, visited_list = GraphAlgorithms.dfs(adjusting_matrix, nodes, visited_list, first_node)
            visited_number += number
            components.append([number, visited_nodes])
            if number >= len(nodes) // 2:
                break

        biggest_component = max(components, key=itemgetter(0))
        return biggest_component[1]

    @staticmethod
    # heuristic function 
    # in plans: just h(n1, n2) = |n1.x - n2.x| + |n1.y - n2.y| 
    def heuristic(node1: Node, node2: Node, mode = 0):
        if mode == 0:
            #return 1 * (abs(node1.apos[0] - node2.apos[0]) + abs(node1.apos[1] - node2.apos[1]))
            #return max(abs(node1.apos[0] - node2.apos[0]), abs(node1.apos[1] - node2.apos[1]))
            return math.hypot(abs(node1.apos[0] - node2.apos[0]), abs(node1.apos[1] - node2.apos[1]))
        else:
            return "L0L"

    @staticmethod
    # cost func
    # g1(road) = road.lenght;
    # g2(road) = road.lenght + Q(road)
    # Q(road) is flow of road
    def cost(road: Road, mode = 0):
        if mode == 0:
            return road.length
        elif mode == 1:
            return road.length + road.Flow()
        else:
            return "L0L"

    @staticmethod
    # nodes, current_node, destination, current_cost, path, threshold
    def IDDFS(nodes, destination, current_cost, path, color_nodes, threshold):
        current_node = color_nodes[-1]

        if current_node == destination:
            return [-current_cost, path]

        f = GraphAlgorithms.heuristic(nodes[current_node], nodes[destination]) + current_cost
        if f > threshold:
            return [f, path]
        
        min = math.inf
        

        for adj_road in nodes[current_node].adj_nodes:
            if adj_road[0] not in color_nodes and adj_road[1].is_open:

                # color_nodes[adj_road[0]] = 1
                color_nodes.append(adj_road[0])
                path.append([adj_road[1], current_node, adj_road[0]])
                ret = GraphAlgorithms.IDDFS(nodes, destination, 
                current_cost + GraphAlgorithms.cost(adj_road[1]), path, color_nodes, threshold)

                if ret[0] < 0:
                    return ret

                if ret[0] < min:  
                    min = ret[0]
                
                
                
                # color_nodes[adj_road[0]] = 0
                color_nodes.pop()
                path.pop()

        return [min, path]


    def IDA(nodes, start_node, destination):
        # start = time.time()
        threshold = GraphAlgorithms.heuristic(nodes[start_node], nodes[destination]) 
        
        color_nodes = [start_node] # [0] * len(nodes)
        while True:
            
            # color_nodes[start_node] = 1
            ret = GraphAlgorithms.IDDFS(nodes, destination, 0, [], color_nodes, threshold)
            if ret[0] == math.inf:
                return []
            elif ret[0] < 0:
                # print("The time for one cycle: ", abs(time.time() - start))
                return ret[1]
            else:
                threshold = ret[0]
        
    def A_Star(nodes : list[Node], start_node: int, destination: int):
        open_list = PriorityQueue()
        open_list.put((0, start_node))
        cost_list = {}
        parent_list = {}
        cost_list[start_node] = 0
        parent_list[start_node] = None

        while not open_list.empty():
            current_node = open_list.get()[1]

            if current_node == destination:
                break

            for adj_road in nodes[current_node].adj_nodes:
                if not adj_road[1].is_open:
                    continue

                new_cost = cost_list[current_node] + GraphAlgorithms.cost(adj_road[1])

                if adj_road[0] not in cost_list or new_cost < cost_list[adj_road[0]]:
                    cost_list[adj_road[0]] = new_cost
                    priority = GraphAlgorithms.heuristic(nodes[adj_road[0]], nodes[destination]) + new_cost
                    open_list.put((priority, adj_road[0]))
                    parent_list[adj_road[0]] = [adj_road[1], current_node, adj_road[0]]
        

        if destination not in parent_list:
            return []

        way = []
        parent = parent_list[destination]
        while parent != None:
            way.append(parent)
            parent = parent_list[parent[1]]
        
        return way[::-1]

    @staticmethod
    def getAdjustingMatrix(nodes):

        matrix = {index : set() for index in range(len(nodes))}

        for node in nodes:
            for road in node.adj_nodes:
                matrix[node.index].add(road[1])
                matrix[road[1]].add(node.index)
        
        return matrix

    @staticmethod
    # Old method of getting matrix for Dijkstra, which is unused now
    def getMatrix(vertixes, edges):
        """getting the distances matrix

        Args:
            vertixes (list[Node]): nodes
            edges (list[Road]): roads, unnecessary

        Returns:
            list[list[[int, Road]]]: [length, Road] - n*n matrix with Road w/ length for dijkstra
        """
        distance_matrix = []
        # k = 0
        for i in range(len(vertixes)):
            temp = []
            for j in range(len(vertixes)):
                temp.append([0, None])
            distance_matrix.append(temp)

        for index, node in enumerate(vertixes):
            for road in node.start_roads:
                distance_matrix[road.start_node][road.end_node] = [road.length, road]

        return distance_matrix




def excludeOSMGraph(graph, use_custom_algorithm = False):
    """Excluding the nodes and edges which doesn't seem to be usefull for our purposes

    Args:
        graph (nx.graph): graph was got by osm tools

    Returns:
        list[Node], list[Node], list[Road]: nodes, spawn_nodes, roads
    """
    nodes = []
    roads = []
    spawn_nodes = []

    start = time.time()
    
    if use_custom_algorithm:

        nodes_indexes = {}
        roads_to_delete = []

        # offset_x = graph.nodes[next(iter(graph.nodes))]['x']
        # offset_y = graph.nodes[next(iter(graph.nodes))]['y']

        # first part of excluding useless nodes & roads include:
        # creating the nodes from .osm graph (networkx model)    
        for node_index, node in enumerate(graph.nodes):
            # attributes = graph.nodes[node]
            # nodes.append(Node(0, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))
            # nodes[-1].attributes = attributes
            # if nodes[-1].type == "spawn":
            #     spawn_nodes.append(node)

            nodes_indexes[node] = node_index
            pass

        # nodes_n_roads = [0] * len(nodes)

        # exclude from graph the forbidden attributes such as 'pedestrian', and so on.
        for edge in graph.edges:
            attributes = graph.edges[edge]
            if 'highway' in attributes:
                if attributes['highway'] in ForbiddenHighways:
                    roads_to_delete.append(edge)
                    # print(nodes[nodes_indexes[edge[0]]])
                    # print(nodes[nodes_indexes[edge[1]]])
                    continue
            else:
                roads_to_delete.append(edge)
                continue

        
        # removing edges from .osm graph
        for edge in roads_to_delete:
            graph.remove_edge(edge[0], edge[1], edge[2])

        list_subgraphs = list(graph.subgraph(c) for c in nx.weakly_connected_components(graph))
        graph = max(list_subgraphs, key=len)


        offset_x = graph.nodes[next(iter(graph.nodes))]['x']
        offset_y = graph.nodes[next(iter(graph.nodes))]['y']
        nodes_indexes = {}

        for node_index, node in enumerate(graph.nodes):
            attributes = graph.nodes[node]
            if len(graph.edges(node)) <= 1:
                spawn_nodes.append(node_index)
                nodes.append(Node(0, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))
            else:
                nodes.append(Node(1, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))

            nodes[-1].attributes = attributes
            nodes_indexes[node] = node_index
            pass

        # removing the unnecessary nodes from .osm graph
        # nodes = [nodes[i] for i in range(len(nodes)) if nodes_n_roads[i] != 0]
        nodes_indexes = { i : nodes_indexes[i] for i in nodes_indexes}
        
        # for node_index, node in enumerate(nodes):
        #     node.index = node_index

        # creating nodes indexes for getting them on the next step
        for index, node_index in enumerate(nodes_indexes.keys()):
            nodes_indexes[node_index] = index


    else:
        list_subgraphs = list(graph.subgraph(c) for c in nx.weakly_connected_components(graph))
        graph = max(list_subgraphs, key=len)

        nodes_indexes = {}
        roads_to_delete = []

        offset_x = graph.nodes[next(iter(graph.nodes))]['x']
        offset_y = graph.nodes[next(iter(graph.nodes))]['y']

        # first part of excluding useless nodes & roads include:
        # creating the nodes from .osm graph (networkx model)    
        for node_index, node in enumerate(graph.nodes):
            attributes = graph.nodes[node]
            # nodes.append(Node(0, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))
            if len(graph.edges(node)) <= 1:
                spawn_nodes.append(node_index)
                nodes.append(Node(0, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))
            else:
                nodes.append(Node(1, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))

            nodes[-1].attributes = attributes

            nodes_indexes[node] = node_index
            pass



    # creating roads for our formed graph
    for index, edge in enumerate(graph.edges):
        attributes = graph.edges[edge]
        s_n = nodes_indexes[edge[0]]
        e_n = nodes_indexes[edge[1]]
        lanes = (int(attributes['lanes']) if not isinstance(attributes['lanes'], list) else int(attributes['lanes'][0])) if 'lanes' in attributes.keys() else 1
        # print(lanes)
        roads.append(Road(nodes, s_n, e_n, 1, index))# (lanes + 1) // 2 ))
        nodes[s_n].addRoad(roads[-1])
        nodes[e_n].addRoad(roads[-1], 'end')
        nodes[s_n].addRoadAdj(e_n, roads[-1])



    graph = None

    print("The time for graph exluding: ", abs(time.time() - start))
    return [nodes, spawn_nodes, roads, offset_x, offset_y]


