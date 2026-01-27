import random
from utils.errors import InvalidDistinationFor42Path

class Cell:
    def __init__(self):
        self.north: bool = True
        self.west: bool = True
        self.south: bool = True
        self.east: bool = True
        self.visited = False
        self._42_path = False
        self.parent = []
        self.BFSvisited = False

class MazeGenerator:
    def __init__(self, cols, rows):
        self.x = cols
        self.y = rows
        self.maze = self.creat_grid()
        self.stack: list = []
    
    
    def creat_grid(self) -> list:
        return [[Cell() for _ in range(self.x)] for _ in range(self.y)]

    def find_nighbors(self, cell) -> list:
        x, y = cell
        maze = self.maze
        unvisited_cells = []
        if x - 1 >= 0 and not maze[y][x-1].visited \
            and self.maze[y][x - 1]._42_path == False:
            unvisited_cells.append((x-1, y, "left"))
        if x + 1 < self.x and not maze[y][x+1].visited \
            and self.maze[y][x + 1]._42_path == False:
            unvisited_cells.append((x+1, y, "right"))
        if y - 1 >= 0 and not maze[y-1][x].visited \
            and self.maze[y - 1][x]._42_path == False:
            unvisited_cells.append((x, y-1, "top"))
        if y + 1 < self.y and not maze[y+1][x].visited \
            and self.maze[y + 1][x]._42_path == False:
            unvisited_cells.append((x, y+1, "bottom"))
        return unvisited_cells        


    def creat_maze_bakctracker_algo(self, i = 0, j = 0):
        
        if (self.x < 9 or self.y < 9):
            # to handel this error call the instnace remove_walls methode 
            # on exception block
            raise InvalidDistinationFor42Path("error: invalid path "
                "for 42 pathern.\n'we will generat maze without 42 pathern'")
        self.creat_42_pathren()
        self.remove_walls(i, j)

    def remove_walls(self, i = 0, j = 0) -> None:
        self.maze[j][i].visited = True
        neighbors = self.find_nighbors((i, j))
        while neighbors:
            next_cell = random.choice(neighbors)
            new_x, new_y, direction = next_cell
            self.maze[new_y][new_x].visited = True
            if direction == "left":
                self.maze[j][i].west = False
                self.maze[new_y][new_x].east = False
            elif direction == "right":
                self.maze[j][i].east = False
                self.maze[new_y][new_x].west = False
            elif direction == "top":
                self.maze[j][i].north = False
                self.maze[new_y][new_x].south = False
            elif direction == "bottom":
                self.maze[j][i].south = False
                self.maze[new_y][new_x].north = False
            self.remove_walls(new_x, new_y)
            neighbors = self.find_nighbors((i, j))

    # this method I do it to creat 42 patter it's not finished has error i will correct it when i came back
    def creat_42_pathren(self):
        # if self.x % 2 == 0:
        x = self.x // 2 - 3
        # else:
        #     x = self.x // 2 - 4
        # if self.y % 2 == 0:
        #     y = self.y // 2 - 4
        # else:
        y = self.y // 2 - 3
        # drowing of 4
        first_y = y
        for move in range(0, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        #drowing of 2

        y = first_y
        x += 2
        for move in range(0, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x - move]._42_path = True
            last_x = move
        x -= last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x
        
    def debug_print(self):
        for y in range(self.y):
            # top walls
            for x in range(self.x):
                print("+---" if self.maze[y][x].north else "+   ", end="")
            print("+")

            # side walls
            for x in range(self.x):
                print("|   " if self.maze[y][x].west else "    ", end="")
            print("|")

        # bottom border
        print("+---" * self.x + "+")
