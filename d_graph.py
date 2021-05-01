# Course: CS261 - Data Structures
# Author: Alyssa Comstock
# Assignment: 6
# Description: Contains the class and functions for a directional graph

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Function that adds a vertex to the directed graph.

        Returns the new number of vertices.
        """


        if self.v_count == 0:
            self.adj_matrix = [[0]]
            self.v_count+=1
            return self.v_count
        else:
            self.v_count+= 1
            self.adj_matrix.append([0]*(self.v_count-1))
            for i in range(0,self.v_count):
                self.adj_matrix[i].append(0)
        return self.v_count



    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Function that add edges to the graph based on the src and dst params passed in.

        Updates the weights.
        """
        if(src == dst):
            return

        if(weight < 0):
            return
        elif(src >= self.v_count or dst>=self.v_count):
            return
        self.adj_matrix[src][dst] = weight
        return



    def remove_edge(self, src: int, dst: int) -> None:
        """
        Function that removes a edge from the adj matrix
        """

        if(src < 0):
            return
        if(dst <0):
            return
        if(src >= self.v_count or dst >= self.v_count):
            # not in graph
            return
        self.adj_matrix[src][dst] = 0
        return



    def get_vertices(self) -> []:
        """
        Function that gets the list of vertices in the graph.
        """


        temp = []
        for i in range(0, self.v_count):
            temp.append(i)
        return temp



    def get_edges(self) -> []:
        """
        Function that gets the edges in a graph
        """


        temp = []
        if(self.v_count == 0):
            return temp
        for src in range(0, self.v_count):
            for dst in range(0, self.v_count):
                val = self.adj_matrix[src][dst]
                if(val != 0):
                    temp.append((src, dst, val))
        return temp



    def is_valid_path(self, path: []) -> bool:
        """
        Function that determines if the path parameter passed in is a valid path
        in the directed graph
        """


        for i in range(len(path)-1):
            src = path[i]
            dst = path[i+1]
            if(self.adj_matrix[src][dst] == 0):
                return False
        return True



    def dfs(self, v_start, v_end=None) -> []:
        """
        Function that does a depth first search and returns the order of vertices.
        """


        # STEP 1: Init empty set of visited vertices
        visited = []

        # STEP 2: init empty stack
        result_stack = deque()  # will be used as a stack

        # STEP 2 pt 2: add v_start
        result_stack.append(v_start)


        # STEP 3: if the stack is not empty, pop vertex v
        while (len(result_stack) > 0):
            v = result_stack.pop()

            # sort in reverse order so that the items are popped off in order
            successors = []
            for i in range(self.v_count):
                # get all the successors
                if (self.adj_matrix[v][i] != 0):
                       successors.append(i)
            successors = sorted(successors, reverse=True)
            if (v not in visited):
                # if the current vertex is not in visited we add it, and then append it
                visited.append(v)
                # add all the successors
                for i in successors:
                    result_stack.append(i)
                if (v == v_end):
                    # if we have reached the end we return after adding the final vertex so that its not missed
                    return visited
        return visited



    def bfs(self, v_start, v_end=None) -> []:
        """
        Function that does a bf search and returns the order of vertices.
        """

        # STEP 1: Init empty set of visited vertices
        visited = []

        # STEP 2: init empty stack
        result_queue = deque()  # will be used as a stack

        # STEP 2 pt 2: add v_start
        result_queue.append(v_start)

        # STEP 3: if the queue is not empty, dequeue
        while (len(result_queue) > 0):
            v = result_queue.pop()  # remove from the front
            # sort in reverse order so that the items are popped off in order
            successors = []
            for i in range(self.v_count):
                # get all the successors
                if (self.adj_matrix[v][i] != 0):
                    successors.append(i)
            successors = sorted(successors, reverse=False)

            if (v not in visited):
                # if the current vertex is not in visited we add it, and then append it ( to the left)
                visited.append(v)
                # add all the successors
                for i in successors:
                    result_queue.appendleft(i)
                if (v == v_end):
                    # if we have reached the end we return after adding the final vertex so that its not missed
                    return visited
        return visited



    def has_cycle(self):
        """
        Function that determines if there is a cycle in the graph.  Returns True if so, false otherwise
        """

        # STEP 2: init empty stack
        result_stack = deque()  # will be used as a stack

        for key in range(0,self.v_count):
            # STEP 1: Init empty set of visited vertices
            visited = []

            # STEP 3: if the stack is not empty, pop vertex v

            result_stack.append(key)

            while (len(result_stack) > 0):
                v = result_stack.pop()
                # sort in reverse order so that the items are popped off in order

                successors = []
                for i in range(0,self.v_count):
                    # get all the successors
                    if (self.adj_matrix[v][i] != 0):
                        successors.append(i)
                successors = sorted(successors, reverse=True)

                if (v not in visited):
                    # if the current vertex is not in visited we add it, and then append it
                    visited.append(v)
                    # add all the successors
                    for i in successors:
                        result_stack.append(i)
                else:
                    # v in visited
                    for i in successors:
                        if (i in visited):
                            # checking if we already went here
                            return True


        return False



    def dijkstra(self, src: int) -> []:
        """
        Function that uses dijkstra formula to determine the shortest distances between src parameter and vertex v
        returns a list of distances
        """

        # based on the psuedocode in the module

        # STEP 1 initialize empty map / hash table representing visited vertices
        visited = {} # using a dictionary

        # STEP 2: set up the priority queue. add only the distance 0 with the src which will be the start
        priority_queue = []

        heapq.heappush(priority_queue, [0, src])
        # set the src in visited to 0
        visited[src] = 0


        while(len(priority_queue)>0):
            # STEP 3: remove the first element from the priority queue
            temp = priority_queue.pop()
            v = temp[1] # gets the current vertex
            d = temp[0] # current vertex distance

            if v not in visited.keys():
                # if the key doesn't exist then initialize it to infinity
                visited[v] = float('inf')

            # for each successor of v we need to check the distances to see if 1 is better
            for i in range(0,self.v_count):
                # get each successor that exists so if a weight is not 0
                if(self.adj_matrix[v][i] != 0):
                    di = self.adj_matrix[v][i] # this is the distance between v and i, so the weight between them
                    # for example: the distance between 0 -> 1 is 10

                    if(i not in visited.keys()):
                        # if the key doesn't exist then initialize it to infinity
                        visited[i] = float('inf')

                    # di + d is the weight between v and i + the distance
                    if((di+d) < visited[i]):
                        # inserting vi into the priority queue with d+di
                        # if the new distance is better, we replace the distance in the visited list
                        # set the new visited distance to the new distance
                        visited[i] = di+d
                        # then add that to the priority queue with the distance first
                        heapq.heappush(priority_queue, (di+d, i))

        # make the visited dictionary to a distance list
        distance = []
        for i in range(0, self.v_count):
            if(i in visited.keys()):
                distance.append(visited[i])
            else:
                distance.append(float('inf'))
        return distance



if __name__ == '__main__':
    """
    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)
 
    print("\nPDF - method remove_edges() example")
    print("----------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)
    g.remove_edge(0,1)
    g.remove_edge(5, 5)
    print(g)
    
    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

   
    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method dfs() test 2")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    print(g.dfs(0,3))
   
    """
    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - method has_cycle() example 2")
    print("----------------------------------")
    edges2 = [(0,1,8), (1,4,1), (1,9,10), (1,12,9), (2,5,1), (4,8,17), (6,10,5), (9,2,11), (9,6,13), (11,0,9), (11,4,7),(11,5,20), (11,9,1)]
    g2 = DirectedGraph(edges2)
    print(g.get_edges(), g.has_cycle(), sep='\n')

    print('\n', g2)

    """
    
    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    """