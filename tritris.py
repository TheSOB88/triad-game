#!/usr/bin/env python
import pygame, os, random, pygame.draw as draw

#import basic pygame modules
from pygame.locals import *


#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit( "Sorry, extended image module required" )
    
cGrid = Color(0x80,0x80,0x80)
cGameBG = Color(0xF8,0xF8,0xEC)
cGameGrid = Color(0x40,0x40,0x40)
cBlack = Color('black')

#0 is empty, 1 is top left tri, next 3 are clockwise rotations, 
#5 is 1+3, 6 is 2+4
class Piece:
    matrix = [[0]*2]*2
    x, y = 0, 0
    type = None
    def __init__( self, type, x = None, y = None ):
        self.type = type
        if type == 1:
            self.matrix = [ [ 4, 0 ],
                            [ 5, 0 ] ]
        elif type == 2:
            self.matrix = [ [ 4, 0 ],
                            [ 6, 0 ] ]
        elif type == 3:
            self.matrix = [ [ 3, 0 ],
                            [ 5, 0 ] ]
        elif type == 4:
            self.matrix = [ [ 3, 0 ],
                            [ 6, 0 ] ]
        elif type == 5:
            self.matrix = [ [ 4, 0 ],
                            [ 2, 4 ] ]
        elif type == 6:
            self.matrix = [ [ 4, 0 ],
                            [ 2, 1 ] ]
        elif type == 7:
            self.matrix = [ [ 3, 0 ],
                            [ 2, 4 ] ]
        elif type == 8:
            self.matrix = [ [ 3, 0 ],
                            [ 2, 1 ] ]
        else:
            Error()
            
        if x:
            self.x = x
        if y:
            self.y = y
        
    def rotate( self, clockwise = True ):
        if clockwise:
            #rotate triangles individually
            for i in range(0, 2):
                for j in range(0, 2):
                    triType = self.matrix[j][i]
                    if triType in range(1,4):
                        self.matrix[j][i] = triType + 1
                    elif triType == 4:
                        self.matrix[j][i] = 1
                    elif triType == 5:
                        self.matrix[j][i] = 6
                    elif triType == 6:
                        self.matrix[j][i] = 5
                    elif triType == 0:
                        pass
                    else:
                        Error()
            #rotate triangle arrangement
            temp = self.matrix[0][0]
            self.matrix[0][0] = self.matrix[1][0]
            self.matrix[1][0] = self.matrix[1][1]
            self.matrix[1][1] = self.matrix[0][1]
            self.matrix[0][1] = temp
        else:
            #rotate triangles individually
            for i in range(0, 2):
                for j in range(0, 2):
                    triType = self.matrix[j][i]
                    if triType in range(1,4):
                        self.matrix[j][i] = triType + 1
                    elif triType == 4:
                        self.matrix[j][i] = 1
                    elif triType == 5:
                        self.matrix[j][i] = 6
                    elif triType == 6:
                        self.matrix[j][i] = 5
                    elif triType == 0:
                        pass
                    else:
                        Error()
            #rotate triangle arrangement
            temp = self.matrix[0][0]
            self.matrix[0][0] = self.matrix[1][0]
            self.matrix[1][0] = self.matrix[1][1]
            self.matrix[1][1] = self.matrix[0][1]
            self.matrix[0][1] = temp
        
        #move tiles to the top/left
        if self.matrix[0][0] == 0:
            if self.matrix[1][0] == 0:
                self.matrix[0][0] = self.matrix[0][1]
                self.matrix[0][1] = 0
                self.matrix[1][0] = self.matrix[1][1]
                self.matrix[1][1] = 0
            elif self.matrix[0][1] == 0:
                self.matrix[0][0] = self.matrix[1][0]
                self.matrix[1][0] = 0
                self.matrix[0][1] = self.matrix[1][1]
                self.matrix[1][1] = 0
        
        
        
    @classmethod
    def drawTriangle( cls, surface, color, type, x, y ):
        if type not in range(1, 7):
            return
        #points
        topLeft = (x * 48, y * 48)
        topRight = ((x+1) * 48 - 1, y * 48)
        botLeft = (x * 48, (y+1) * 48 - 1)
        botRight = ((x+1) * 48 - 1, (y+1) * 48 - 1)

        if type == 1 or type == 5:
            draw.polygon( surface, color, [topLeft, topRight, botLeft] )
        if type == 3 or type == 5:
            draw.polygon( surface, color, [topRight, botRight, botLeft] )
        if type == 2 or type == 6:
            draw.polygon( surface, color, [topLeft, topRight, botRight] )
        if type == 4 or type == 6:
            draw.polygon( surface, color, [topLeft, botLeft, botRight] )
                    
        if type in (1, 5, 2, 6):
            draw.line( surface, cBlack, topLeft, topRight )
        if type in (1, 5, 4, 6):
            draw.line( surface, cBlack, topLeft, botLeft )
        if type in (1, 3, 5):
            draw.line( surface, cBlack, botLeft, topRight )
        # if type in ( 3, 5, 2, 6):
            # draw.line( surface, cBlack, topRight, botRight )
        # if type in ( 3, 5, 4, 6):
            # draw.line( surface, cBlack, botLeft, botRight )
        if type in ( 2, 4, 6):
            draw.line( surface, cBlack, topLeft, botRight )

        
    def draw( self, surface ):
        for i in range(0, 2):
            for j in range(0, 2):
                Piece.drawTriangle( surface, cGameGrid, self.matrix[i][j], self.x + j, self.y + i )
    
class Board:
    matrix = [[0]*12]*8
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
    gameWindow = Rect( 0, 0, 800, 704 )
    clock = pygame.time.Clock()

    main_dir = os.path.split( os.path.abspath( __file__ ) )[0]
    
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ( 'Warning, no sound' )
        pygame.mixer = None    
    pygame.display.set_caption( 'Tritris v0.1' )
    
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok( gameWindow.size, winstyle, 32 )
    screen = pygame.display.set_mode( gameWindow.size, winstyle, bestdepth )
    
    board = pygame.Surface( (128 * 3, 192 * 3), pygame.SRCALPHA )    
    boardCorner = (24 * 16, 64) 
    boardX, boardY = boardCorner
    
    #instantiate demo pieces
    pieces = [None]*8
    for i in range(0, 8):
        pieces[i] = Piece( i + 1, (i % 4 ) * 2, int( i/4 ) * 2 )
    ticks = -1
    
    while True:
        #get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        keystate = pygame.key.get_pressed()
        
        screen.fill( Color(0,0,0) )
        board.fill( Color(0,0,0,0) )
        
        for x in range(1, int( gameWindow.w/16 ) + 1):
            draw.line( screen, cGrid, (x * 16, 0), (x * 16, gameWindow.h) )
        for y in range(1, int( gameWindow.h/16 ) + 1):
            draw.line( screen, cGrid, (0, y * 16), (gameWindow.w, y * 16) )
        draw.rect( screen, cGameBG, (boardCorner,(128 * 3, 192 * 3)) )
        
        for x in range( 1, 8 ):
            draw.line( screen, cGameGrid, (boardX + x * 48, boardY), (boardX + x * 48, boardY +48 * 12) )
        for y in range( 1, 12 ):
            draw.line( screen, cGameGrid, (boardX, boardY + y * 48), (boardX + 48 * 8, boardY + y * 48) )
        
        ticks += 1        
        if ticks == 30:
            for i in range(0, 8):
                pieces[i].rotate()
            ticks = 0
        
        for i in range(0, 8):
            pieces[i].draw( board )
        
        screen.blit( board, boardCorner )
        
        pygame.display.update()
        #cap the framerate
        clock.tick(60)

    pygame.quit()

 
#call the "main" function if running this script
if __name__ == '__main__': main()