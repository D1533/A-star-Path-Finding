import sys
import pygame
import functions

def main():
    
    screen = pygame.display.set_mode(functions.screen_size)
    pygame.display.set_caption('A* pathfinding algorithm')
    clock = pygame.time.Clock()
    functions.createMap()
    pygame.font.init()
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #DRAW WALL
            if pygame.mouse.get_pressed() == (1,0,0):
                pos = pygame.mouse.get_pos()
                functions.drawWall(pos)
            #ERASE WALL
            if pygame.mouse.get_pressed() == (0,0,1):
                pos = pygame.mouse.get_pos()
                functions.eraseWall(pos)
            #DRAW EXTREME NODE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    # Call your function here
                    pos = pygame.mouse.get_pos()  # Assuming you still need the mouse position
                    functions.drawExtreme(pos)

            #BEGIN TO FIND PATH
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and functions.extreme:
                    functions.find_path(functions.i_begin, functions.j_begin , functions.i_final, functions.j_final)
                    
        functions.draw_map(screen, functions.Map)
        functions.drawInstructions(screen)
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()