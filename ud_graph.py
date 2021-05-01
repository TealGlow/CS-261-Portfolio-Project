# Course: CS 261
# Author: Alyssa Comstock
# Assignment: 6
# Description: File that contains the class and functions for an undirected graph using an adj list

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if(v in self.adj_list):
            # if key is already in list then do nothing
            return
        self.adj_list[v]=[]
        return


    # TODO: make smaller?
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if(u == v):
            return
        if(v not in self.adj_list and u not in self.adj_list):
            if(v<u):
                # inserts the keys in sorted order
                self.add_vertex(v)
                self.add_vertex(u)
                self.adj_list[u].append(v)
                self.adj_list[v].append(u)
                return
            else:
                self.add_vertex(u)
                self.add_vertex(v)
                self.adj_list[v].append(u)
                self.adj_list[u].append(v)
                return
        if(v not in self.adj_list):
            # add v
            self.add_vertex(v)
            self.adj_list[v].append(u)
            if(u in self.adj_list):
                self.adj_list[u].append(v)
            else:
                self.add_vertex(u)
                self.adj_list[u].append(v)
        if(u not in self.adj_list):
            self.add_vertex(u)
            self.adj_list[u].append(v)
            if (v in self.adj_list):
                self.adj_list[v].append(u)
            else:
                self.add_vertex(v)
                self.adj_list[v].append(u)
        else:
            #only add these items if they dont already exist in their respective adj_list
            if(u not in self.adj_list[v]):
                self.adj_list[v].append(u)
            if(v not in self.adj_list[u]):
                self.adj_list[u].append(v)
    
            return



    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """

        if(u not in self.adj_list):
            return
        if(v not in self.adj_list):
            return

        # remove the link from both sides
        if(u in self.adj_list[v]):
            self.adj_list[v].remove(u)
        if(v in  self.adj_list[u]):
            self.adj_list[u].remove(v)
        return



    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """


        if(v in self.adj_list):
            # remove each link
            for key in self.adj_list:
                self.remove_edge(key, v)
            # delete the key
            del self.adj_list[v]
        return



    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        key_list = []

        for key in self.adj_list:
            key_list.append(key)
        return key_list



    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []
        for key in self.adj_list:
            for i in range(0,len(self.adj_list[key])):
                if((key,self.adj_list[key][i]) not in edge_list and (self.adj_list[key][i],key) not in edge_list):
                    edge_list.append((key,self.adj_list[key][i]))
        return edge_list



    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """


        if(len(path) == 1):
            # single vertex in path
            if(path[0] not in self.adj_list):
                # if the single vertex is not in the keys, then its not valid
                return False
            else:
                return True


        for i in range(0, len(path)-1):
            if(path[i] not in self.adj_list):
                # if the current item is not in the list, return false anyway
                return False

            # get a list of all the edges
            edges = self.get_edges()

            # vertex in sorted order
            if(path[i] < path[i+1]):
                # if the tuple value of the sorted paths is not in the list of edges return false
                if((path[i],path[i+1])not in edges):
                    return False
            else:
                if ((path[i+1], path[i]) not in edges):
                    return False
        return True


    # TODO: CHECK
    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        vertices = self.get_vertices()
        if v_start not in vertices:
            return []


        # STEP 1: Init empty set of visited vertices
        visited = []

        # STEP 2: init empty stack
        result_stack = deque() # will be used as a stack

        # STEP 2 pt 2: add v_start
        result_stack.append(v_start)

        # STEP 3: if the stack is not empty, pop vertex v
        while(len(result_stack)>0):
            v = result_stack.pop()
            # sort in reverse order so that the items are popped off in order
            successors = sorted(self.adj_list[v], reverse=True)

            if(v not in visited):
                # if the current vertex is not in visited we add it, and then append it
                visited.append(v)
                # add all the successors
                for i in successors:
                    result_stack.append(i)
                if (v == v_end):
                    # if we have reached the end we return after adding the final vertex so that its not missed
                    return visited
        return visited



    # TODO: CHECK
    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        vertices = self.get_vertices()
        if v_start not in vertices:
            return []

        # STEP 1: Init empty set of visited vertices
        visited = []

        # STEP 2: init empty stack
        result_queue = deque()  # will be used as a stack

        # STEP 2 pt 2: add v_start
        result_queue.append(v_start)

        # STEP 3: if the queue is not empty, dequeue
        while (len(result_queue) > 0):
            v = result_queue.pop() # remove from the front
            # sort in reverse order so that the items are popped off in order
            successors = sorted(self.adj_list[v], reverse=False)

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
        


    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        count = 0
        visited = []

        # from the wikipedia page on component graph theory:
        # begin with a vertex (in this case its each key in the adj_list
        # find the entire component using either bfs or dfs, add
        # once a vertex is found that was not previously found
        # add 1 to the count and go through its vertices

        for key in self.adj_list:
            if(key not in visited):
                # if the key is not in the visited list, then it is a new component
                # find all its connected vertices with bfs, add 1 to the count
                # add it to the visited list
                temp = self.bfs(key)
                count +=1
                for i in temp:
                    # add each item to the visited list
                    visited.append(i)
        return count



    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        # STEP 1: Init empty set of visited vertices
        visited = []

        # STEP 2: init empty stack
        result_stack = deque()  # will be used as a stack

        # STEP 2 pt 2: add v_start

        # STEP 3: if the stack is not empty, pop vertex v
        for key in self.adj_list:
        # go through each key
            result_stack.append(key)
            while (len(result_stack) > 0):
                v = result_stack.pop()
                # sort in reverse order so that the items are popped off in order
                successors = sorted(self.adj_list[v], reverse=True)

                if (v not in visited):
                    # if the current vertex is not in visited we add it, and then append it
                    visited.append(v)
                    # add all the successors
                    for i in successors:
                        result_stack.append(i)
                # if v is has already been visited then we have a cycle
                if(v in result_stack):
                    return True
        return False

   


if __name__ == '__main__':
    """
    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nadd_edge example 3")
    print("----------------------------------------------")
    toAdd = ['EH', 'EB', 'HF', 'FD', 'BE', 'GI', 'DF']
    g = UndirectedGraph()
    for u, v in toAdd:
        g.add_edge(u, v)
    print(g)

    print("\nadd_edge example 2")
    print("----------------------------------------------")
    toAdd = ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE']
    g = UndirectedGraph()
    for u, v in toAdd:
        g.add_edge(u, v)
    print(g)

    print("\nadd_edge example 3")
    print("----------------------------------------------")
    toAdd = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph()
    for u, v in toAdd:
        g.add_edge(u, v)
    print(g)

    print("\nadd_edge example 4")
    print("----------------------------------------------")
    g = UndirectedGraph(['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG'])
    print(g)

 
 
    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)



  

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))
  
    """
    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')

    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')
    """

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
    """