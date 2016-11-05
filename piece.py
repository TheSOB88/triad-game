import pygame, os, random, pygame.draw as draw
from pygame.locals import *

from gameSettings import *

#0 is empty, 1 is top left tri, next 3 are clockwise rotations, 
#5 is 1+3, 6 is 2+4
class Piece:
    matrix = [[0]*2]*2
    x, y = 0, 0
    type = None
    color = None
    rotation = 0
    
    def __init__( self, pieceType, x = None, y = None, color = Color(0,0,0) ):
        self.type = pieceType
        self.color = color
        if pieceType == 1:
            self.matrix = [ [ 4, 0 ],
                            [ 5, 0 ] ]
        elif pieceType == 2:
            self.matrix = [ [ 4, 0 ],
                            [ 6, 0 ] ]
        elif pieceType == 3:
            self.matrix = [ [ 3, 0 ],
                            [ 5, 0 ] ]
        elif pieceType == 4:
            self.matrix = [ [ 3, 0 ],
                            [ 6, 0 ] ]
        elif pieceType == 5:
            self.matrix = [ [ 4, 0 ],
                            [ 2, 4 ] ]
        elif pieceType == 6:
            self.matrix = [ [ 4, 0 ],
                            [ 2, 1 ] ]
        elif pieceType == 7:
            self.matrix = [ [ 3, 0 ],
                            [ 2, 4 ] ]
        elif pieceType == 8:
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
            self.rotation += 1
            if self.rotation > 3:
                self.rotation = 0
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
            #center piece if it's a square + tri
            if not( doDemo ) and self.type in range(1,5):
                if self.rotation == 1:
                    self.y += 1
                elif self.rotation == 3:
                    self.x -= 1
                elif self.rotation == 0:
                    self.x += 1
                    self.y -= 1
                    
        else:
            self.rotation -= 1
            if self.rotation < 0:
                self.rotation = 3
            #rotate triangles individually
            for i in range(0, 2):
                for j in range(0, 2):
                    triType = self.matrix[j][i]
                    if triType in range(2,5):
                        self.matrix[j][i] = triType - 1
                    elif triType == 1:
                        self.matrix[j][i] = 4
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
            self.matrix[0][0] = self.matrix[0][1]
            self.matrix[0][1] = self.matrix[1][1]
            self.matrix[1][1] = self.matrix[1][0]
            self.matrix[1][0] = temp
            #center piece if it's a square + tri
            if not( doDemo ) and self.type in range(1,5):
                if self.rotation == 2:
                    self.x += 1
                elif self.rotation == 3:
                    self.x -= 1
                    self.y += 1
                elif self.rotation == 0:
                    self.y -= 1
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
                
        #keep piece in bounds
        ##TODO: move this logic to the board when it's processing input (allow for different sizes)
        self.x = self.x if self.x >= 0 else 0
        self.x = self.x if self.x < 8 else 7
        self.y = self.y if self.y >= 0 else 0
        self.y = self.y if self.y < 12 else 11
           
    '''Adds two triangles together'''
    @classmethod
    def addTri( cls, a, b ):
        if a == 0:
            return b
        if b == 0:
            return a
        if (a == 1 and b == 3) or (a == 3 and b == 1):
            return 5
        if (a == 2 and b == 4) or (a == 4 and b == 2):
            return 6
        Error()        
        
    @classmethod
    def drawTriangle( cls, surface, color, triType, x, y ):
        if triType not in range(1, 7):
            return
        #points
        topLeft = (x * 48, y * 48)
        topRight = ((x+1) * 48 - 1, y * 48)
        botLeft = (x * 48, (y+1) * 48 - 1)
        botRight = ((x+1) * 48 - 1, (y+1) * 48 - 1)
        
        #need to support two colors for double-triangle blocks
        if type( color ) != type( (0,0) ):
            color1, color2 = color, color
        else:
            color1, color2 = color[0], color[1]

        if triType == 1 or triType == 5:
            draw.polygon( surface, color1, [topLeft, topRight, botLeft] )
        if triType == 3 or triType == 5:
            draw.polygon( surface, color2, [topRight, botRight, botLeft] )
        if triType == 2 or triType == 6:
            draw.polygon( surface, color1, [topLeft, topRight, botRight] )
        if triType == 4 or triType == 6:
            draw.polygon( surface, color2, [topLeft, botLeft, botRight] )
                    
        if triType in (1, 5, 2, 6):
            draw.line( surface, cBlack, topLeft, topRight )
        if triType in (1, 5, 4, 6):
            draw.line( surface, cBlack, topLeft, botLeft )
        if triType in (1, 3, 5):
            draw.line( surface, cBlack, botLeft, topRight )
        # if triType in (3, 5, 2, 6):
            # draw.line( surface, cBlack, topRight, botRight )
        # if triType in (3, 5, 4, 6):
            # draw.line( surface, cBlack, botLeft, botRight )
        if triType in (2, 4, 6):
            draw.line( surface, cBlack, topLeft, botRight )

        
    def draw( self, surface ):
        for i in range(0, 2):
            for j in range(0, 2):
                Piece.drawTriangle( surface, self.color, self.matrix[i][j], self.x + j, self.y + i )
                
               
