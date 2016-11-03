        
        if type in (1, 3, 4, 6):
            draw.line( surface, topLeft, topRight )
        if type in (1, 3, 5, 6):
            draw.line( surface, topLeft, botLeft )
        if type in (1, 2, 3):
            draw.line( surface, botLeft, topRight )
        if type in (2, 3, 4, 6):
            draw.line( surface, topRight, botRight )
        if type in (2, 3, 5, 6):
            draw.line( surface, botLeft, botRight )
        if type in (4, 5, 6):
            draw.line( surface, topLeft, botRight )