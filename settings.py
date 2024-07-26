class Node:
    def __init__ (self, i, j, g, h, n):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = n

#SETTINGS
map_size = (800, 600)
instructions_size = (200, 200)

screen_size = (map_size[0] + instructions_size[0], map_size[1] + instructions_size[1])
cell_size = 25
i_begin = 5
j_begin = 1
i_final = 0
j_final = 0
running = False
extreme = False
Time = 0
Map = []