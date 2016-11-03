#!/usr/bin/env python
import pygame, os, random, pygame.draw as draw

#import basic pygame modules
from pygame.locals import *


#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit( "Sorry, extended image module required" )


gameWindow = Rect( 0, 0, 800, 704 )
clock = pygame.time.Clock()

main_dir = os.path.split( os.path.abspath( __file__ ) )[0]

class Board:
    def __init__( self ):
        pass
    def addPiece( self ):
        pass
    def removeLine( self ):
        pass
    #check if there are lines to remove
    def update( self ):
        pass

def main():
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ( 'Warning, no sound' )
        pygame.mixer = None    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok( gameWindow.size, winstyle, 32 )
    screen = pygame.display.set_mode( gameWindow.size, winstyle, bestdepth )
    
    pygame.display.set_caption( 'Tritris v0.1' )
    
    cGrid = Color(0x80,0x80,0x80)
    cGameBG = Color(0xF8,0xF8,0xEC)
    cGameGrid = Color(0x40,0x40,0x40)
    
    while True:        
        #get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        keystate = pygame.key.get_pressed()
        
        gameBoard = Rect(0, 0, 128, 196)
        
        for x in range(1, int( gameWindow.w/16 ) + 1):
            draw.line( screen, cGrid, (x * 16, 0), (x * 16, gameWindow.h) )
        for y in range(1, int( gameWindow.h/16 ) + 1):
            draw.line( screen, cGrid, (0, y * 16), (gameWindow.w, y * 16) )
            
        gameBoardCorner = (23 * 16, 64)
        boardX, boardY = gameBoardCorner
        draw.rect( screen, cGameBG, (gameBoardCorner, (128 * 3, 192 * 3)) )
        
        for x in range( 1, 8 ):
            draw.line( screen, cGameGrid, (boardX + x * 48, boardY), (boardX + x * 48, boardY +48 * 12) )
        for y in range( 1, 12 ):
            draw.line( screen, cGameGrid, (boardX, boardY + y * 48), (boardX + 48 * 8, boardY + y * 48) )
        
        
        pygame.display.update()
        #cap the framerate
        clock.tick(60)

    pygame.quit()

 
#call the "main" function if running this script
if __name__ == '__main__': main()