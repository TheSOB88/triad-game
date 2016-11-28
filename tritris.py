#!/usr/bin/env python

import pygame, os, random, pygame.draw as draw
from pygame.locals import *

import piece, board
Piece = piece.Piece
Board = board.Board
from gameSettings import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit( "Sorry, extended image module required" )
    
controls = {} #hash of which controls are currently held
newControls = None #array of which controls pressed this frame
for key in ['up', 'down', 'left', 'right', 'a', 'b', 'x', 'y']:
    controls[key] = False
keysToControls = {
    K_UP: 'up',
    K_DOWN: 'down',
    K_LEFT: 'left',
    K_RIGHT: 'right',
    K_w: 'up',
    K_s: 'down',
    K_a: 'left',
    K_d: 'right',
    K_SPACE: 'rotateR',
    K_LSHIFT: 'rotateL',
    K_RSHIFT: 'rotateR'
}

globalTicks = -1

def processControls():
    global newControls, controls, globalTicks
    
    newControls = set()#controls pressed this frame
    #get input  
    for event in pygame.event.get():
        if event.type == QUIT:
            return "quit"
        #game buttons
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return "quit"
            elif event.key in keysToControls:
                controls[keysToControls[event.key]] = globalTicks
                newControls.add( keysToControls[event.key] )
        elif event.type == KEYUP:
            if event.key in keysToControls:
                controls[keysToControls[event.key]] = False
        #demo buttons
        if event.type == KEYDOWN and doDemo:
            return "clock"
            
def drawScreenGrid( screen, cGrid, gameWindow ):
    for x in range(1, int( gameWindow.w/16 ) + 1):
        draw.line( screen, cGrid, (x * 16, 0), (x * 16, gameWindow.h) )
    for y in range(1, int( gameWindow.h/16 ) + 1):
        draw.line( screen, cGrid, (0, y * 16), (gameWindow.w, y * 16) )

def drawBoardGrid( screen, cGameGrid, boardX, boardY ):
    for x in range( 1, BOARD_WIDTH ):
        draw.line( screen, cGameGrid, (boardX + x * 48, boardY), 
                (boardX + x * 48, boardY +48 * BOARD_HEIGHT) )
    for y in range( 1, BOARD_HEIGHT ):
        draw.line( screen, cGameGrid, (boardX, boardY + y * 48), 
                (boardX + 48 * BOARD_WIDTH, boardY + y * 48) )


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
    
    boardSurface = pygame.Surface( (BOARD_WIDTH * 48, BOARD_HEIGHT * 48), pygame.SRCALPHA )
    boardCorner = (24 * 16, 64) 
    boardX, boardY = boardCorner
    board = Board( BOARD_WIDTH, BOARD_HEIGHT )
    
    if doDemo:
        #instantiate demo pieces
        demoPieces = [None]*8
        for i in range(0, 8):
            demoPieces[i] = Piece( i + 1, (i % 4 ) * 2, 8 + int( i/4 ) * 2, colors[i] )
            board.addPiece( demoPieces[i] )
            demoPieces[i].y -= 8
    else:
        #instantiate game stuff
        pieceType = 8
        currentPiece = None
        moveControls = set( ( 'left', 'right', 'down' ) )
        moveTicks = 0
        moveDelay = 20
        gravityTicks = -1
        
    demoClockwise = True
    ticks = -1
    globalTicks = -1
    
    quitGame = False
        
    gameBG = pygame.Surface( gameWindow.size )
    if demoGrids:
        drawScreenGrid( gameBG, cGrid, gameWindow )
    draw.rect( gameBG, cGameBG, ( boardCorner, (BOARD_WIDTH * 48, BOARD_HEIGHT * 48) ) )
    if demoGrids:
        drawBoardGrid( gameBG, cGameGrid, boardX, boardY )
    
    while not quitGame:
        globalTicks += 1
    
        controlsReturnVal = processControls()
        if controlsReturnVal == "quit":
            quitGame = True
            print( 'quittin\'' )
        elif controlsReturnVal == "clock":
            demoClockwise = not demoClockwise    
            
        screen.fill( Color(0,0,0) )
        boardSurface.fill( Color(0,0,0,0) )
           
        if doDemo:
            ticks += 1     
            if ticks == 30:
                for i in range(0, 8):
                    demoPieces[i].rotate( demoClockwise )
                ticks = 0
            
            board.draw( boardSurface )
            for i in range(0, 8):
                demoPieces[i].draw( boardSurface )
        #game logic
        else:
            #create new piece if none currently
            if not currentPiece:
                currentPiece = Piece( pieceType, 4 if pieceType < 5 else 3, 0, colors[pieceType-1] )
                gravityTicks = 0
                
            #update timers
            if len( newControls ) > 0:
                newDirections = newControls.intersection( moveControls )
                if len( newDirections ) > 0:
                    moveTicks = -1
                    moveDelay = 20
                if 'rotateR' in newControls:
                    board.rotate( currentPiece, True )
                if 'rotateL' in newControls:
                    board.rotate( currentPiece, False )
            moveTicks += 1
            gravityTicks += 1
            
            currentPiece.oldX = currentPiece.x
            currentPiece.oldY = currentPiece.y
                
            #check for directional move
            if ( controls['down'] or controls['left'] or controls['right'] ) and moveTicks == 0:
                moveTicks = moveDelay * -1
                moveDelay = 8
                #do move
                if controls['down']:
                    currentPiece.y += 1
                    gravityTicks = 0
                if controls['left']:
                    currentPiece.x -= 1 
                if controls['right']:
                    currentPiece.x += 1
            
            #gravity
            if gravityTicks == 45:
                gravityTicks = 0
                ##pieceMoved = True
                
                currentPiece.y += 1 
                
            doNewPiece = board.checkBoundaries( currentPiece )
            if doNewPiece:
                board.addPiece( currentPiece )
                pieceType = pieceType + 1 if pieceType < PIECE_TYPES else 1
                currentPiece = None
                board.draw( boardSurface )
            else:
                if currentPiece.oldX != currentPiece.x or currentPiece.oldY != currentPiece.y:
                    x, y = currentPiece.x, currentPiece.y
                    xDelta = ( x - currentPiece.oldX ) * .334
                    yDelta = ( y - currentPiece.oldY ) * .334
                    currentPiece.x = currentPiece.oldX + xDelta
                    currentPiece.y = currentPiece.oldY + yDelta
                    times = 0
                    while times < 3:
                        screen.blit( gameBG, (0,0) )
                        boardSurface.fill( Color(0,0,0,0) )
                        board.draw( boardSurface )
                        currentPiece.draw( boardSurface )
                        screen.blit( boardSurface, boardCorner )
                        pygame.display.update()
                        clock.tick(60)
                        currentPiece.x += xDelta
                        currentPiece.y += yDelta
                        times += 1
                        
                currentPiece.x = round( currentPiece.x )
                currentPiece.y = round( currentPiece.y )
                        
                board.draw( boardSurface )
                currentPiece.draw( boardSurface )
                
        screen.blit( gameBG, (0,0) )
        screen.blit( boardSurface, boardCorner )
        pygame.display.update()
        #cap the framerate
        clock.tick(60)

    pygame.quit()

 
#call the "main" function if running this script
if __name__ == '__main__': main()