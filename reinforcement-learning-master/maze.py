from random import shuffle, randrange
from mdpstate import MDPState
from copy import deepcopy

class Maze:
    
    """
    Creates a maze of specified size.
    Output is a list of lists, to be used as a matrix with coordinates.
    '#' = wall
    ' ' = empty space
        
    Adapted from http://rosettacode.org/wiki/Maze_generation#Python
    """
    
    def __init__(self, w=10, h=10):
        
        self.vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        self.ver = [["# "] * w + ['#'] for _ in range(h)] + [[]]
        self.hor = [["##"] * w + ['#'] for _ in range(h + 1)]
                     
        self.matrix = self.make_maze(w, h)
        
        self.grid = self.maze_to_mdp()
    
    def make_maze(self, w, h):

        self.walk(randrange(w), randrange(h))
        
        cells = ""
        
        for (a, b) in zip(self.hor, self.ver):
            cells += ''.join(a + ['\n'] + b + ['\n'])
            
        cells = cells.split('\n')
        cells = [list(row) for row in cells]
        del cells[len(cells)-1]
        del cells[len(cells)-1]
        
        return [row for row in cells]
     
    def walk(self, x, y):
        self.vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if self.vis[yy][xx]: continue
            if xx == x: self.hor[max(y, yy)][x] = "# "
            if yy == y: self.ver[y][max(x, xx)] = "  "
            self.walk(xx, yy)
 
    def __repr__(self):
        strlst = [''.join(row) for row in self.matrix]
        return '\n'.join(strlst)
    
    def maze_to_mdp(self):
        
        """Returns a matrix of MDPState objects for each free space in a maze"""
        
        grid = deepcopy(self.matrix)
    
        for i in range(1, len(self.matrix) - 1):
            for j in range(1, len(self.matrix) - 1):
                
                #represent walls as #
                if self.matrix[i][j] == '#':
                    grid[i][j] = '#'
                    continue
                    
                if self.matrix[i-1][j] == '#':
                    north = (i, j)
                else:
                    north = (i-1, j)
                    
                if self.matrix[i+1][j] == '#':
                    south = (i, j)
                else:
                    south = (i+1, j)
                    
                if self.matrix[i][j+1] == '#':
                    east = (i, j)
                else:
                    east = (i, j+1)
                    
                if self.matrix[i][j-1] == '#':
                    west = (i, j)
                else:
                    west = (i, j-1)
                    
                grid[i][j] = MDPState(north, south, west, east)
        
        # Set exit point reward
        grid[1][1].reward = 10
                
        return(grid)
            
if __name__ == '__main__':
    new_maze = Maze()
    print(new_maze.matrix)
