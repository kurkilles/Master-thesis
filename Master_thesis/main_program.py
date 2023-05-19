import numpy as np
#import sympy

test = np.array([[0,1,1,0,0],[0,0,1,1,0],[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
test2 = np.array([[1,1,0,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,1,0,1,0],[0,0,1,1,0],[0,0,0,1,1]])

class Possibility:

    def __init__(self, edge_list, adjacency_list, connected_components, size, term):
        # Graph in an edge list format
        self.edge_list = edge_list
        # Graph in an adjacency list format
        self.adjacency_list = adjacency_list
        self.size = size
        self.edges = [x for x,y in self.edge_list]
        self.connected_components = connected_components
        self.term = term
        self.added = False

    def reduce(self, edge):
        # Here we find the edge to reduce
        for e in self.edge_list:
            if e[0] == edge:
                e_to_reduce = e
                break
        new = min(e_to_reduce[1])
        old = max(e_to_reduce[1])

        # We need to change connected components
        new_cc = self.connected_components.copy()
        if old in self.connected_components:
            if new in self.connected_components:
                new_cc.remove(old)
            else:
                new_cc.remove(old)
                new_cc.append(new)
        self.connected_components = new_cc

        # Here is our main loop that changes all other edges
        new_edge_list = []
        for e in self.edge_list:
            if e == e_to_reduce:
                continue
            elif old in e[1]:
                a, b = e[1]
                if a == old:
                    new_edge_list.append([e[0], (new, b)])
                else:
                    new_edge_list.append([e[0], (new, a)])
            else:
                new_edge_list.append(e)
        self.edge_list = new_edge_list

    # This unction unifies edge lists in order to be able to find duplicates
    def unify(self):
        c_edge = []
        for edge in self.edge_list:
            if edge[1][0] > edge[1][1]:
                c_edge.append([edge[0], (edge[1][1],edge[1][0])])
            else:
                c_edge.append(edge)
        self.edge_list = c_edge

    def add_r(self, edge):
        self.term += "R{}*".format(edge)

    def add_f(self, edge):
        self.term += "F{}*".format(edge)

    # This function deletes an edge from edge list in this instance
    def delete(self, edge):
        for e in self.edge_list:
            if e[0] == edge:
                e_to_remove = e
                break
        self.edge_list.remove(e_to_remove)

    # Adding two instances = adding their terms
    def __iadd__(self, other):
        if self.term[-1] != "*":
            self.term += "*"
        self.term = self.term[:-1] + "+" + other.term[:-1]
        self.added = True

    def par(self):
        if self.added:
            self.term = "(" + self.term + ")*"
            self.added = False


class Solution:
    # We have to check if the connection is possible at the start

    def __init__(self, edge_list, nodes):
        # The original edge list and its size
        self.edge_list = edge_list
        # Here be improvements
        self.nodes = nodes
        # Variables needed to clear bridges
        self.certain_bridges = []
        self.id = 0
        self.visited_dfs = [False for i in range(len(self.get_al(self.edge_list, self.nodes)))]
        self.ids = [1 for i in range(len(self.get_al(self.edge_list, self.nodes)))]
        self.low = [1 for i in range(len(self.get_al(self.edge_list, self.nodes)))]
        self.bridges = []
        self.bridge_candidates = []

    @staticmethod
    def input_matrix():
        matrix=np.array([])
        size = int(input("How many vertices does this graph has? "))
        while True:
            if input("\nDo you want to add an edge?\nClick enter if yes and write anything if not.\n"):
                return matrix
            try:
                # Create an empty vector, to later add to a matrix
                vector = np.zeros((1,size))
                # Which nodes are connected
                first = int(input("What is the first vertex? "))
                second = int(input("What is the second vertex? "))
                if first==second:
                    print("Vertex can not be connected to itself")
                    continue
                # Adding values to our vector
                vector[0,first-1]=1
                vector[0,second-1]=1
                # Connecting the vector to our matrix
                if matrix.size>0:
                    matrix=np.vstack([matrix, vector])
                else:
                    matrix=vector
                print(matrix)
            except:
                print("There was an error\nPlease type correct values")


    # Converts input matrix into an edge list
    @staticmethod
    def convert(matrix):
        # This is an edge number
        i=1
        edge_list = []
        for vector in matrix:
            # Creating tuple containing two connected nodes
            my_tuple = tuple(i+1 for i, x in enumerate(vector) if x==1)
            # creating list [edge number, (two connected nodes)]
            edge_list.append([i,my_tuple])
            # Next edge
            i += 1
        return edge_list


    # Turning edge list into an adjacency list
    @staticmethod
    def get_al(edge_list, nodes_number):
        graph = {}
        for i in range(nodes_number):
            graph[i+1] = []
        # Every edge is converted into two parts of a dictionary eg. [1, (3,4)] - {3 : [4], 4 : [3]}
        for edge in edge_list:
            graph[edge[1][0]].append(edge[1][1])
            graph[edge[1][1]].append(edge[1][0])
        return graph


    # This function removes chosen edge from a list
    def __remove_edge(self, edge_list, t_edge):
        n_edge_list = edge_list.copy()
        for edge in n_edge_list.copy():
            if edge == t_edge:
                n_edge_list.remove(edge)
                break
        return n_edge_list

    # Our main algorithm
    def __bfs(self, al, start, ends):
        # Initializing the queue
        queue = [start]
        # Initializing list that shows which nodes were visited and turning the starting one visited
        visited_bfs = [False for i in range(len(al))]
        visited_bfs[start-1]=True
        v_set = {start}

        # Loop working as long as there are items in a queue
        while queue:
            # Setting variable node as the first item in the queue and deleting it from the queue
            node=queue[0]
            del queue[0]
            # Getting the neighbours of that node
            neighbours=al[node]

            # Going threw all the unvisited neighbours
            for n in neighbours:
                if ends.issubset(v_set):
                    return True
                if not visited_bfs[n-1]:
                    v_set.add(n)
                    # Adding the neighbours to the queue and changing their status to visited
                    queue.append(n)
                    visited_bfs[n-1] = True
        return False

    # Our main algorithm
    def __bfs_b(self, al, start, ends):
        # Initializing the queue
        queue = [start]
        # Initializing list that shows which nodes were visited and turning the starting one visited
        visited_bfs = [False for i in range(len(al))]
        visited_bfs[start-1]=True
        v_set = {start}

        # Loop working as long as there are items in a queue
        while queue:
            # Setting variable node as the first item in the queue and deleting it from the queue
            node=queue[0]
            del queue[0]
            # Getting the neighbours of that node
            neighbours=al[node]

            # Going threw all the unvisited neighbours
            for n in neighbours:
                if not visited_bfs[n-1]:
                    v_set.add(n)
                    # Adding the neighbours to the queue and changing their status to visited
                    queue.append(n)
                    visited_bfs[n-1] = True
        if ends.issubset(v_set):
            return visited_bfs
        else:
            return False

    # This function finds bridges in the graph
    def __find_bridges(self, at=1, parent=0):
        # Defining the id's and low-link values lists
        self.visited_dfs[at-1] = True
        self.id += 1
        self.low[at-1] = self.id
        self.ids[at-1] = self.id
        # Going through all the neighbours of a current node
        for neighbour in self.get_al(self.edge_list, self.nodes)[at]:
            # Ignoring the neighbour if we've come to the current node from it
            if neighbour == parent:
                continue
            # Using this function again if the neighbour was not visited
            elif not self.visited_dfs[neighbour-1]:
                self.__find_bridges(neighbour, at)
                self.low[at-1] = min(self.low[at-1], self.low[neighbour-1])
                # Adding found bridges to the list
                if self.ids[at-1] < self.low[neighbour-1]:
                    self.bridges.append((at, neighbour))
            # Changing the low-link value of the current node
            else:
                self.low[at-1] = min(self.low[at-1], self.ids[neighbour-1])

    # This function search if there are two nodes connected with each other by two or more edges
    def __find_duplicates(self):
        for a, b in self.bridges.copy():
            if self.get_al(self.edge_list, self.nodes)[a].count(b)>1:
                # Removing those edges from the bridge list
                self.bridges.remove((a,b))

    # Searching for the bridges in the edge list
    def __find_bridge_edges(self):
        for edge in self.edge_list:
            if edge[1] in self.bridges:
                self.bridge_candidates.append(edge)

    # This function clears bridges and unwanted components of the graph
    def clear_bridges(self, first, rest):
        # Here are activated three functions, that all together find all the edges that are considered bridges
        self.__find_bridges()
        self.__find_duplicates()
        self.__find_bridge_edges()
        # Here we go trough all those edges
        for bridge in self.bridge_candidates:
            # We check if the bridge was not already deleted
            if bridge in self.edge_list:
                edges = self.edge_list.copy()
                edges.remove(bridge)
                # We find all the nodes who are possible to be visited after the removal of the bridge
                visited = self.__bfs_b(self.get_al(edges, self.nodes), first, rest)
                # We remove edges that are not needed
                if visited:
                    not_visited = []
                    for i, x in enumerate(visited):
                        if not x:
                            not_visited.append(i+1)
                    edges_copy = edges.copy()
                    for edge in edges:
                        if set(edge[1]).issubset(set(not_visited)):
                            edges_copy.remove(edge)
                    self.edge_list = edges_copy
                else:
                    self.certain_bridges.append(bridge[0])

    def convert_cc(self, connected_components):
        # If all nodes need to be connected:
        if connected_components == "all":
            connected_components = [i+1 for i in range(self.nodes)]
        first = connected_components[0]
        if first > self.nodes:
            return "No connection between all nodes from the start"
        rest = set(connected_components[1:])
        return first, rest

    # Our main function
    def solve(self, connected_components):

        first, rest = self.convert_cc(connected_components)

        # Activating bridge clearing
        self.clear_bridges(first,rest)

        # This is used for getting the equation
        size = [x for x,y in self.edge_list]

        # Here we initialize our first certain edge
        certain = [Possibility(edge_list=self.edge_list, size=size,
                               adjacency_list=Solution.get_al(self.edge_list, self.nodes),
                               connected_components=connected_components, term = "")]
        if not self.__bfs(certain[0].adjacency_list, self.convert_cc(certain[0].connected_components)[0],
                          self.convert_cc(certain[0].connected_components)[1]):
            return "No connection between all nodes from the start"


        for edge in self.edge_list:
            if edge[0] in self.certain_bridges:
                certain[0].reduce(edge[0])

        if len(certain[0].connected_components)==1:
            equation=""
            for e in self.certain_bridges:
                equation+="R{}*".format(e)
            return equation[:-1]

        # This list stores possible working candidates
        uncertain = []
        # We go threw every single edge
        for edge in certain[0].edge_list.copy():

            # Here we put into our uncertain list possible candidates
            uncertain_parent = []
            for c in certain.copy():
                # If the edge is self-loop delete it
                this_edge = ""
                for e in c.edge_list:
                    if edge[0] == e[0]:
                        this_edge = e
                        break
                if this_edge and this_edge[1][0] == this_edge[1][1]:
                    c.delete(edge[0])
                else:
                    uncertain.append(Possibility(adjacency_list=Solution.get_al(self.__remove_edge(c.edge_list, this_edge), self.nodes),
                                             edge_list=self.__remove_edge(c.edge_list, this_edge), size=size,
                                            connected_components=c.connected_components, term=c.term))
                    uncertain_parent.append(c.connected_components)
                    c.reduce(edge[0])
                    c.add_r(edge[0])

            # We check those candidates if there are valid
            for uc in uncertain:
                # We check if there is a connection between every pair and add True, False value
                if len(uc.connected_components) == 1 or self.__bfs(uc.adjacency_list, self.convert_cc(uc.connected_components)[0],
                              self.convert_cc(uc.connected_components)[1]):
                    uc.add_f(edge[0])
                    certain.append(uc)
            # We clear our uncertain list
            uncertain = []
            # Here we unify edges
            for c in certain:
                c.unify()
            if len(certain) > 1:
                # Here we remove duplicates
                to_remove = []
                to_add = []
                for c in certain[:-1]:
                    for d in certain[certain.index(c)+1:]:
                        if c.edge_list == d.edge_list:
                            to_add.append([c,d])

                to_remove = []
                for a in to_add:
                    if a[0] not in to_remove:
                        to_remove.append(a[1])
                        a[0] += a[1]

                for r in to_remove:
                    certain.remove(r)

            for c in certain:
                c.par()

        # Having all the certain possibilities we create an equation
        equation = certain[0].term
        equation = equation[:-1]
        pre_equation = ""
        for c in self.certain_bridges:
            pre_equation += "R{}*".format(c)
        if pre_equation and equation[-1] == ")":
            equation = pre_equation + equation
        elif pre_equation:
            equation = pre_equation + "(" + equation + ")"
        if equation[0]=="(":
            equation = equation[1:-1]
        # And we return it
        return equation