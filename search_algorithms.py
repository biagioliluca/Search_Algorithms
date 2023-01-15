from tkinter import *
import copy
import threading



def start(grid):
    global algo
    if algo == 'Dijkstra':
        dijkstra(grid)
    elif algo == 'A*':
        a_star(grid)
    elif algo == 'BFS':
        bfs(grid)
    elif algo == 'DFS':
        dfs(grid)

def reset(root, grid):
    global start_point_set
    global start_setted
    global end_point_set
    global end_setted
    start_point_set = False
    start_setted = False
    end_point_set = False
    end_setted = False
    grid.destroy()
    Grid(root,60,55,10)

def set_start():
    global start_setted
    if start_setted == False:
        print("start settato True")
        global start_point_set
        start_point_set = True
        start_setted = True

def set_end():
    global end_setted
    if end_setted == False:
        global end_point_set
        end_point_set = True
        end_setted = True

def algorithm_callback(*args):
    global algo
    if args[0] == 'BFS':
        algo = 'BFS'
        print(algo)
    elif args[0] == 'Dijkstra':
        algo = 'Dijkstra'
        print(algo)
    elif args[0] == 'A*':
        algo = 'A*'
        print(algo)
    elif args[0] == 'DFS':
        algo = 'DFS'
        print(algo)





class Node():
    def __init__(self, row, column, father = None, path_cost = 0, *args, **kwargs):
        self.row = row
        self.col = column
        self.father = father
        self.path_cost = path_cost
        self.wall = False

class Grid(Canvas):
    def __init__(self, root, num_columns, num_rows, cell_size, *args, **kwargs):
        Canvas.__init__(self, root, width = num_columns * cell_size, height = num_rows * cell_size, *args, **kwargs)

        self.num_columns = num_columns
        self.num_rows = num_rows
        self.cell_size = cell_size
        self.start_node = None
        self.end_node = None

        self.grid_, self.graphic_grid= self.initialize_grid(num_rows, num_columns, cell_size)

        self.bind("<Button-1>", self.handleMouse)
        self.bind("<B1-Motion>", self.handleMouse)

        self.grid(row=0,column=0)

    def handleMouse(self, event):
        row = int(event.y / self.cell_size)
        column = int(event.x / self.cell_size)

        cell = self.grid_[row][column]
        global start_point_set
        global end_point_set
        if start_point_set:
            self.start_node = self.grid_[row][column]
            self.start_node.wall = True

            self.itemconfigure(self.graphic_grid[row][column], fill='yellow')
            start_point_set = False
        elif end_point_set:
            self.end_node = self.grid_[row][column]
            self.itemconfigure(self.graphic_grid[row][column], fill='red')
            end_point_set = False
        elif not cell.wall:
            cell.wall = True
            self.itemconfigure(self.graphic_grid[row][column], fill='black')


    def initialize_grid(self, num_rows, num_columns, cell_size):
        grid = []
        color_grid = []
        for row in range(num_rows):
            new_row = []
            new_color_row = []
            for col in range(num_columns):
                rectangle = self.create_rectangle(col*cell_size,row*cell_size,(col+1)*cell_size,(row+1)*cell_size,fill='white',outline='black')
                new_row.append(Node(row, col))
                new_color_row.append(rectangle)
            grid.append(new_row)
            color_grid.append(new_color_row)
        return grid, color_grid

def dijkstra(grid):
    if grid.start_node == None:
        print("Insert a start point")
        return
    elif grid.end_node == None:
        print("Insert an end point")
        return

    start = grid.start_node
    end = grid.end_node

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
            track_solution(node,grid)
            return

        explored.append((node.path_cost, node))

        for action in ["up","right","left","down"]:
            if action == "up" and node.row-1 >= 0 and not grid.grid_[node.row-1][node.col].wall:
                child = grid.grid_[node.row-1][node.col]
                grid.itemconfigure(grid.graphic_grid[node.row-1][node.col], fill='blue')
                analyze_child(frontier, explored, node, child)

            if action == "right" and node.col+1 <= grid.num_columns-1 and not grid.grid_[node.row][node.col+1].wall:
                child = grid.grid_[node.row][node.col+1]
                grid.itemconfigure(grid.graphic_grid[node.row][node.col+1], fill='blue')
                analyze_child(frontier, explored, node, child)

            if action == "left" and node.col-1 >= 0 and not grid.grid_[node.row][node.col-1].wall:
                child = grid.grid_[node.row][node.col-1]
                grid.itemconfigure(grid.graphic_grid[node.row][node.col-1], fill='blue')
                analyze_child(frontier, explored, node, child)

            if action == 'down' and node.row+1 <= grid.num_rows-1 and not grid.grid_[node.row+1][node.col].wall:
                child = grid.grid_[node.row+1][node.col]
                grid.itemconfigure(grid.graphic_grid[node.row+1][node.col], fill='blue')
                analyze_child(frontier, explored, node, child)


def analyze_child(frontier, explored, father, child):
    new_path_cost = father.path_cost + 1

    if is_in(frontier, child) == None and is_in(explored, child) == None:
        add_to_frontier(frontier, father, child, new_path_cost)
    elif is_in(frontier, child) != None and is_in(frontier, child).path_cost > new_path_cost:
        delete_node(frontier, is_in(frontier, child))
        add_to_frontier(frontier, father, child, new_path_cost)

def add_to_frontier(frontier, father, node, new_cost):
    node.path_cost = new_cost
    node.father = father
    frontier.append((node.path_cost, node))
    frontier.sort(key=lambda a: a[0])
    print(node)

def delete_node(frontier, node):
    for tuple in frontier:
        if tuple[1] == node:
            frontier.remove(tuple)
            return
    raise Exception("NODE NOT FOUND")

def is_in(_list, node):
    for tuple in _list:
        if tuple[1] == node:
            return tuple[1]
    return None

def a_star(grid):
    pass

def bfs(grid):
    pass

def dfs(grid):
    pass

def track_solution(node, grid):
    variable = copy.copy(node.father)
    while variable.father != None:
        row = variable.row
        col = variable.col
        grid.itemconfigure(grid.graphic_grid[row][col], fill='green')
        variable = variable.father

root = Tk()
root.title("Search Algorithms")
root.geometry("850x650")
root.config(background = "Light Blue")

grid = Grid(root,60,55,10)

algo = 'Dijkstra'

variable = StringVar(root)
variable.set("Dijkstra")
algorithms = ['Dijkstra', 'A*', 'BFS', 'DFS']
opm = OptionMenu(root, variable, *algorithms, command = algorithm_callback).grid(row=1,column=0)
#opm.config(width=30)
#opm.pack()

start_button = Button(root, text = "Start", bg = "white", fg = "black", border = 3, font = ("Arial", 12), command = lambda actual_grid = grid: start(actual_grid)).grid(row=1,column=1)

#start_button.pack()

reset_button = Button(root, text = 'Reset', bg = "white", fg = "black", border = 3, font = ("Arial", 12), command = lambda master = root, old_grid = grid: reset(master, old_grid)).grid(row=1,column=2)

start_point_set = False
start_setted = False
begin_point = Button(root, text = 'Choose start', bg = "white", fg = "black", border = 3, font = ("Arial", 12), command=lambda: set_start()).grid(row=2,column=1)

# end_point_set = False
# end_setted = False
goal_point = Button(root, text = 'Choose end', bg = "white", fg = "black", border = 3, font = ("Arial", 12), command=lambda: set_end()).grid(row=2,column=2)

class GoalButton(Button):
    def __init__(self, root, text):
        super.__init__(self, root, text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda: self.set_end())
        self.end_setted = False
        self.end_point_sett = False

    def set_end(self):
        if not self.end_setted:
            self.end_point_set = True
            self.end_setted = True


class BeginButton(Button):
    def __init__(self, root, text):
        super.__init__(self, root, text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda: self.set_start())
        self.start_point_set = False
        self.start_setted = False

    def set_start(self):
        if not self.start_setted:
            self.start_point_set = True
            self.start_setted = True

class ResetButton(Button):
    def __init__(self, root, text, canvas, begin_button, end_button):
        super.__init__(self, root, text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda master = root, old_grid = canvas: reset(master, old_grid, begin_button, end_button))

    def reset(root, canvas, begin_button, end_button):
        # reset flags
        begin_button.start_point_set = False
        begin_button.start_setted = False
        end_button.end_point_set = False
        end_button.end_setted = False
       
        # create a new grid
        canvas.destroy()
        Grid(root,60,55,10)

class StartButton(Button):
    def __init__(self, root, text, canvas):
        super.__init__(self, root, text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda actual_grid = canvas: start(canvas))

        self.algorithm = 'Dijkstra'

    def start(self, canvas):
        if self.algorithm == 'Dijkstra':
            dijkstra(canvas)
        elif self.algorithm == 'A*':
            a_star(canvas)
        elif self.algorithm == 'BFS':
            bfs(canvas)
        elif self.algorithm == 'DFS':
            dfs(canvas)

class DropDown(OptionMenu):
    def __init__(self, root):
        super.__init__(self, root, variable = StringVar(root), *['Dijkstra', 'A*', 'BFS', 'DFS'], command = self.algorithm_callback)
        super.variable.set("Dijkstra")

#reset_button.pack(side = LEFT)



root.mainloop()

