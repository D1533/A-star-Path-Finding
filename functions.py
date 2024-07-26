import pygame
import time
from settings import Node, map_size, instructions_size, screen_size, cell_size, i_begin, j_begin, i_final, j_final, running, extreme, Time, Map



#CREATE MAP WITH ZEROES
def createMap():
    global Map
    for i in range(int(map_size[1]/cell_size)):
        l = []
        for j in range(int(screen_size[0]/cell_size)):
            l.append(0)
        Map.append(l)
    Map[i_begin][j_begin] = 2

def clean_last_path():
    for y in range(int(map_size[1]/cell_size)):
        for x in range(int(screen_size[0]/cell_size)):
            if Map[y][x] == 5:
                Map[y][x] = 0


def draw_map(screen, Map):
    #Map draw
    screen.fill((100,100,100))
    k = 0
    l = 0
    for i in range(0, int(map_size[1]/cell_size),1 ):
        for j in range(0, int(screen_size[0]/cell_size), 1):
            #WALL (LIGHT GREY)
            if Map[i][j] == 1:
                pygame.draw.rect(screen, (200,200,200), (k, l, cell_size, cell_size))  
            #EXTREMES (BLUE)
            if Map[i][j] == 2:
                pygame.draw.rect(screen, (0,0,255), (k, l, cell_size, cell_size)) 
            #OPEN NODE (GREEN)
            if Map[i][j] == 3:
                pygame.draw.rect(screen, (0,255, 0), (k, l, cell_size, cell_size))
            #CLOSED NODE (RED)
            if Map[i][j] == 4:
                pygame.draw.rect(screen, (255,0, 0), (k, l, cell_size, cell_size)) 
            #FINAL PATH (YELLOW)
            if Map[i][j] == 5:
                pygame.draw.rect(screen, (255,255, 0), (k, l, cell_size, cell_size))
                
            pygame.draw.rect(screen, (0,0,0), (k, l, cell_size, cell_size), 2)
            k += cell_size
        k = 0
        l += cell_size  
      
    

#CALCULATE DISTANCE
def dist(i, j, i_final, j_final):
    dist = 0
    while i != i_final or j != j_final:
        if i < i_final:
            i += 1
            dist += 1
        if i > i_final:
            i -= 1
            dist += 1
        if j < j_final:
            j += 1
            dist += 1
        if j > j_final:
            j -= 1
            dist +=1
    return dist

#RETURN IF A NODE IS IN LIST
def is_in_list(node, list):
    for k in range(len(list)):
        if node.i == list[k].i and node.j == list[k].j:
            return True
    return False

def find_path(i, j, i_final, j_final):

    global running
    global Time
    running = True
    clean_last_path()

    i_begin = i
    j_begin = j
    openList = []
    closedList = []
    
    currentNode = Node(i, j, 0, 0, None)
    openList.append(currentNode)
    neighbors = []
    start_time = time.time()
    while True:
        maximum = float('inf')
        index = 0
        #FIND MINIMUM VALUE F IN NODES OF THE OPEN LIST
        for i in range(len(openList)):
            if openList[i].f < maximum:
                index = i
                maximum = openList[i].f

        #TRANSFER THE NODE WITH MINIMUM DISTANCE TO CLOSED LIST AND SET IT AS CURRENT NODE
        currentNode = openList[index]
        openList.pop(index)
        closedList.append(currentNode) 
        
        #IF CURRENT NODE IS FINAL POSITION OF PATH -> END FUNCTION
        if currentNode.i == i_final and currentNode.j == j_final:
            currentNode = currentNode.parent
            while currentNode.i != i_begin or currentNode.j != j_begin:
                Map[currentNode.i][currentNode.j] = 5
                currentNode = currentNode.parent  
            Time = time.time() - start_time 
            break
        
        #CALCULATE NEIGHBOURS
        #LEFT
        if currentNode.j - 1 >= 0:
            n = Node(currentNode.i, currentNode.j - 1, 0, 0, None)
            neighbors.append(n)
        #RIGTH
        if currentNode.j + 1 < int(screen_size[0]/cell_size):
            n = Node(currentNode.i, currentNode.j + 1, 0, 0, None)
            neighbors.append(n)
        #TOP
        if currentNode.i - 1 >= 0:
            n = Node(currentNode.i - 1, currentNode.j, 0, 0, None)
            neighbors.append(n)
        #BOT
        if currentNode.i + 1 < int(map_size[1]/cell_size):
            n = Node(currentNode.i + 1, currentNode. j, 0, 0, None)
            neighbors.append(n)
        


        for i in range(len(neighbors)):
            #IF NEIGHBOUR IS IN THE CLOSED LIST OR IT IS A WALL -> CONTINUE
            if is_in_list(neighbors[i], closedList) or Map[neighbors[i].i][neighbors[i].j] == 1:
                continue
            #IF NEIGHBOUR IS IN THE OPEN LIST AND ITS DISTANCE IS BETTER, CALCULATE ITS NEW DISTANCE AND BIND IT TO CURRENT NODE
            if is_in_list(neighbors[i], openList) == True:
                if dist(currentNode.i, currentNode.j, neighbors[i].i, neighbors[i].j) + currentNode.g < neighbors[i].g:
                    neighbors[i].g = currentNode.g + dist(currentNode.i, currentNode.j, neighbors[i].i, neighbors[i].j)
                    neighbors[i].parent = currentNode
            #IF NEIGHBOUR IS NOT IN THE OPEN LIST -> CALCULATE ITS DISTANCES, BIND IT TO CURRENT NODE AND ADD IT TO OPEN LIST
            if is_in_list(neighbors[i], openList) == False:
                neighbors[i].g = currentNode.g + dist(neighbors[i].i, neighbors[i].j, currentNode.i, currentNode.j)
                neighbors[i].h = dist(neighbors[i].i, neighbors[i].j, i_final, j_final)
                neighbors[i].parent = currentNode
                openList.append(neighbors[i])
                
        neighbors.clear()
        
        if len(openList) == 0:
            Time = time.time() - start_time
            break

def drawWall(pos):
    if pos[1]< map_size[1]:
        #NOT IN THE BEGIN POSITION
        if (int(pos[1]/cell_size) != i_begin or int(pos[0]/cell_size) != j_begin):
            #IF IT IS A FINAL POSITION CELL, ERASE IT AND CLEAN
            if Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] == 2:
                clean_last_path() 
                global extreme
                extreme = False
            #IF DRAW WALL IN CURRENT PATH RECALCULATE PATH
            if (Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] == 5):
                Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] = 1
                find_path(i_begin, j_begin , i_final, j_final)

            Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] = 1

def eraseWall(pos):
    if pos[1] < map_size[1]:
        #IF IT IS THE EXTREME NODE, ERASE IT
        if Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] == 2:
            global extreme
            extreme = False
            Time = 0
        #IF IS NOT BEGIN POSITION, ERASE WALL AND RECALCULATE PATH
        if (int(pos[1]/cell_size) != i_begin or int(pos[0]/cell_size) != j_begin ) and Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] == 1:
            clean_last_path()
            Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] = 0
            #IF A WALL IS ERASED, RECALCULATE THE PATH
            if running and extreme:
                find_path(i_begin, j_begin, i_final, j_final)


        '''
        if running == True and extreme:
            find_path(i_begin, j_begin, i_final, j_final)
        '''

def drawExtreme(pos):
    if pos[1] < map_size[1]:
        #IF IS NOT A WALL, SAVE NEW FINAL POSITION AND RECALCULATE PATH
        if Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] != 1 and Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] != 2:
            global i_begin
            global j_begin
            global i_final
            global j_final
            global extreme
            extreme = True
            Map[int(pos[1]/cell_size)][int(pos[0]/cell_size)] = 2
            Map[i_final][j_final] = 0
            i_final = int(pos[1]/cell_size)
            j_final = int(pos[0]/cell_size)
            if running == True:
                find_path(i_begin, j_begin, i_final, j_final)


def drawInstructions(screen):
    font = pygame.font.SysFont("Console", 20, bold = True)

    text = []
    text.append(font.render("Draw a Wall:         Left Mouse Button", True, (0,0,0)))
    text.append(font.render("Erase a Wall:        Right Mouse Button", True, (0,0,0)))
    text.append(font.render("Place Node:          Middle Mouse Button", True, (0,0,0)))
    text.append(font.render("Begin A* algorithm:  ENTER", True, (0,0,0)))
    text.append(font.render("Time Elapsed:        %s seconds" %Time, True, (0,0,0)))
    ypos = 620
    for el in text:
        screen.blit(el, (20, ypos))
        ypos += 20
    
    t = font.render("Programmed by D1533", True, (0,0,0))
    screen.blit(t, (750,620))
    