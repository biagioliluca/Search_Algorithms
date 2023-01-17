from tkinter import *
from algorithms import *


class Node():
    def __init__(self, row, column, father = None, path_cost = 0, *args, **kwargs):
        self.row = row
        self.col = column
        self.father = father
        self.path_cost = path_cost
        self.wall = False

class Grid(Canvas):
    def __init__(self, root, num_columns, num_rows, cell_size, start_point_button, goal_point_button, *args, **kwargs):
        Canvas.__init__(self, root, width = num_columns * cell_size, height = num_rows * cell_size, *args, **kwargs)

        self.num_columns = num_columns
        self.num_rows = num_rows
        self.cell_size = cell_size
        self.start_node = None
        self.end_node = None

        self.start_point_button = start_point_button
        self.goal_point_button = goal_point_button

        self.grid_, self.graphic_grid= self.initialize_grid(num_rows, num_columns, cell_size)

        self.bind("<Button-1>", self.handleMouse)
        self.bind("<B1-Motion>", self.handleMouse)

        self.grid(row=0,column=0)

    def handleMouse(self, event):
        row = int(event.y / self.cell_size)
        column = int(event.x / self.cell_size)

        cell = self.grid_[row][column]
        if self.start_point_button.start_point_set:
            self.start_node = self.grid_[row][column]
            self.start_node.wall = True

            self.itemconfigure(self.graphic_grid[row][column], fill='yellow')
            self.start_point_button.start_point_set = False
        elif self.goal_point_button.end_point_set:
            self.end_node = self.grid_[row][column]
            self.itemconfigure(self.graphic_grid[row][column], fill='red')
            self.goal_point_button.end_point_set = False
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

class GoalButton(Button):
    def __init__(self, root, text):
        Button.__init__(self, root, text = text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda: self.set_end())
        self.end_setted = False
        self.end_point_sett = False

    def set_end(self):
        if not self.end_setted:
            self.end_point_set = True
            self.end_setted = True

class BeginButton(Button):
    def __init__(self, root, text):
        Button.__init__(self, root, text = text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda: self.set_start())
        self.start_point_set = False
        self.start_setted = False

    def set_start(self):
        if not self.start_setted:
            self.start_point_set = True
            self.start_setted = True

class ResetButton(Button):
    def __init__(self, root, canvas, begin_button, end_button, text):
        Button.__init__(self, root, text = text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda master = root, old_grid = canvas: self.reset(master, old_grid, begin_button, end_button))

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
    def __init__(self, root, canvas, text):
        Button.__init__(self, root, text = text, bg = 'white', fg = 'black', border = 3, font = ('Arial', 12), command = lambda actual_grid = canvas: self.start(canvas))

        self.canvas = canvas

        self.algorithm = 'Dijkstra'
        
    def start(self, canvas):
        if self.algorithm == 'Dijkstra':
            Dijkstra(canvas).dijkstra()
        elif self.algorithm == 'A*':
            pass
        elif self.algorithm == 'BFS':
            pass
        elif self.algorithm == 'DFS':
            pass

class DropDown(OptionMenu):
    def __init__(self, root, variable, start_button):
        OptionMenu.__init__(self, root, variable, *['Dijkstra', 'A*', 'BFS', 'DFS'], command = self.algorithm_callback)

        self.start_button = start_button

    def algorithm_callback(self, *args):
        if args[0] == 'BFS':
            self.start_button.algorithm = 'BFS'
        elif args[0] == 'Dijkstra':
            self.start_button.algorithm = 'Dijkstra'
        elif args[0] == 'A*':
            self.start_button.algorithm = 'A*'
        elif args[0] == 'DFS':
            self.start_button.algorithm = 'DFS'

root = Tk()
root.title("Search Algorithms")
root.geometry("850x650")
root.config(background = "Light Blue")


begin_point = BeginButton(root, text = 'Choose start')
goal_point = GoalButton(root, text = 'Choose end')
begin_point.grid(row=2,column=1)
goal_point.grid(row=2,column=2)

canvas = Grid(root,60,55,10, begin_point, goal_point)

start_button = StartButton(root, canvas, text = "Start").grid(row=1,column=1)
reset_button = ResetButton(root, canvas, begin_point, goal_point, text = 'Reset').grid(row=1,column=2)

variable = StringVar(root)
variable.set("Dijkstra")
opm = DropDown(root, variable, start_button).grid(row=1,column=0)




root.mainloop()

