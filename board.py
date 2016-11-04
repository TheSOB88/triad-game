import pygame, os, random, pygame.draw as draw
from pygame.locals import *

import piece
Piece = piece.Piece



class Board:
    matrix = [[0]*12]*8
    colorMatrix = [[None]*12]*8
    width, height = 8, 12
    
    def __init__( self ):
        pass
        
    def addPiece( self, piece, x, y ):
        iCap = 2 if x < 7 else 1
        jCap = 2 if x < 11 else 1
        for i in range(0, iCap):
            for j in range(0, jCap):
                selfTri = self.matrix[y+j][x+i]
                pieceTri = piece.matrix[j][i]
                newTri = Piece.addTri( pieceTri, selfTri )
                self.matrix[y][x] = newTri
                if pieceTri == newTri:
                    colorMatrix[y][x] = piece.color
                else:
                    if pieceTri == 1 or pieceTri == 4:
                        colorMatrix[y][x] = ( piece.color, self.colorMatrix[y][x] )
                    else:
                        colorMatrix[y][x] = ( self.colorMatrix[y][x], piece.color )
                
    def removeLine( self, line ):
        for y in reversed( range( 1, line + 1 ) ):
            for x in range( 0, 8 ):
                self.matrix[y][x] = self.matrix[y-1][x] 
                self.colorMatrix[y][x] = self.colorMatrix[y-1][x] 
        self.matrix[0] = [0]*width
        self.colorMatrix[0] = [None]*width
        
    #check if there are lines to remove
    def update( self ):
        for y in range(0,12):
            x = -1
            broke = False
            while not broke:
                x += 1
                if x == 8 or (self.matrix[y][x] != 5 and self.matrix[y][x] != 6):
                    broke = True
            if not broke:
                self.removeLine( y )
                
    def draw( self, surface ):
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                Piece.drawTriangle( surface, self.colorMatrix[y][x], self.matrix[y][x], x, y )
                