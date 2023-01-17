import copy

class Dijkstra():
    def __init__(self, canvas):
        self.canvas = canvas
    
    def dijkstra(self):
        if self.canvas.start_node == None:
            print("Insert a start point")
            return
        elif self.canvas.end_node == None:
            print("Insert an end point")
            return

        start = self.canvas.start_node
        end = self.canvas.end_node

        # priority queue where there are nodes that need to be analyzed
        frontier = []
        frontier.append((start.path_cost,start))

        # list of completely analyzed nodes
        explored = []

        while True:
            if len(frontier) == 0:
                raise Exception("End not detected")

            node = frontier.pop(0)[1]
            if node == end:
                self.track_solution(node,self.canvas)
                return

            explored.append((node.path_cost, node))

            for action in ["up","right","left","down"]:
                if action == "up" and node.row-1 >= 0 and not self.canvas.grid_[node.row-1][node.col].wall:
                    child = self.canvas.grid_[node.row-1][node.col]
                    # self.canvas.itemconfigure(self.canvas.graphic_grid[node.row-1][node.col], fill='blue')
                    self.analyze_child(frontier, explored, node, child)

                if action == "right" and node.col+1 <= self.canvas.num_columns-1 and not self.canvas.grid_[node.row][node.col+1].wall:
                    child = self.canvas.grid_[node.row][node.col+1]
                    # self.canvas.itemconfigure(self.canvas.graphic_grid[node.row][node.col+1], fill='blue')
                    self.analyze_child(frontier, explored, node, child)

                if action == "left" and node.col-1 >= 0 and not self.canvas.grid_[node.row][node.col-1].wall:
                    child = self.canvas.grid_[node.row][node.col-1]
                    # self.canvas.itemconfigure(self.canvas.graphic_grid[node.row][node.col-1], fill='blue')
                    self.analyze_child(frontier, explored, node, child)

                if action == 'down' and node.row+1 <= self.canvas.num_rows-1 and not self.canvas.grid_[node.row+1][node.col].wall:
                    child = self.canvas.grid_[node.row+1][node.col]
                    # self.canvas.itemconfigure(self.canvas.graphic_grid[node.row+1][node.col], fill='blue')
                    self.analyze_child(frontier, explored, node, child)

    def analyze_child(self, frontier, explored, father, child):
        new_path_cost = father.path_cost + 1

        if self.is_in(frontier, child) == None and self.is_in(explored, child) == None:
            self.add_to_frontier(frontier, father, child, new_path_cost)
        elif self.is_in(frontier, child) != None and self.is_in(frontier, child).path_cost > new_path_cost:
            self.delete_node(frontier, self.is_in(frontier, child))
            self.add_to_frontier(frontier, father, child, new_path_cost)

    def add_to_frontier(self, frontier, father, node, new_cost):
        node.path_cost = new_cost
        node.father = father
        frontier.append((node.path_cost, node))
        frontier.sort(key=lambda a: a[0])
        print(node)

    def delete_node(self, frontier, node):
        for tuple in frontier:
            if tuple[1] == node:
                frontier.remove(tuple)
                return
        raise Exception("NODE NOT FOUND")

    
    def is_in(self, list_, node):
        for tuple in list_:
            if tuple[1] == node:
                return tuple[1]
        return None

    def track_solution(self, node, canvas):
        variable = copy.copy(node.father)
        while variable.father != None:
            row = variable.row
            col = variable.col
            canvas.itemconfigure(canvas.graphic_grid[row][col], fill='green')
            variable = variable.father

class AStar():
    pass

class BFS ():
    pass

class DFS():
    pass
