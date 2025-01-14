import pygame

from entities import *



class Sprite(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        self.sprite_sheet = pygame.image.load('asset/pieces_sprite.png').convert_alpha()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (384, 128))
        
    def get_image(self, x, y): 
        image= pygame.Surface([64, 64], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0,0),(x,y, 64, 64)) 
        return image
        
class Piece(Sprite) : 
    def __init__(self, x, y, coord, color, rule_move):
        super().__init__()
        self.image = self.get_image(x,y)
        self.rect = self.image.get_rect()
        self.pos = coord
        self.color = color
        self.rule_move = rule_move
        self.possible_moves = []
        

    # utiliser pygame.vector2 dans une version ultérieure pour les coord, direction... 
        
    def move(self, rect, coord):
        self.pos = coord
        self.rect.topleft = rect.topleft
    
    def calculate_coord(self, pos, move) -> tuple :
        return (pos[0]+ move[0], pos[1]+move[1])
    
    def calculate_coord_i(self, pos, move, i) -> tuple :
        return (pos[0]+ i*move[0], pos[1]+i*move[1])
    
    def coord_in_board(self, coord):
        if 8 > coord[0] >= 0 and 8 > coord[1] >=0 : 
            return True
        return False
    
    def get_move_direction(self, pos, coord):
        dx= coord[0]-pos[0]
        dy= coord[1]-pos[1]
        dx_normalized = 0 if dx == 0 else dx // abs(dx)
        dy_normalized = 0 if dy == 0 else dy // abs(dy)
    
        return (dx_normalized, dy_normalized)
        
        
    

        
        
