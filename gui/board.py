import pygame
from dataclasses import dataclass

@dataclass
class Tile:
    coord : tuple
    rect : pygame.Rect
    
class Board:
    def __init__(self, screen) :
        self.screen = screen
        self.size = 8
        self.px = 64
        self.xoffset, self.yoffset = 64, 128
        self.tiles = []
        
        self.selected_tile = None
        self.illegal_tile = None
        self.possible_tiles = None
        self.all_possible_tiles = None
        
        
    def load(self):
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(x * self.px + self.xoffset, y * self.px + self.yoffset, self.px, self.px)
                coord = (x, y)
                tile = Tile(coord, rect)
                self.tiles.append(tile)
        # print(self.tiles)
                
        
    def draw(self):
        for y in range(self.size):
            for x in range(self.size):
                rect = x*self.px+self.xoffset, y*self.px+self.yoffset, self.px, self.px
                color = "Brown" if (x + y) % 2 == 1 else "White"
                pygame.draw.rect(self.screen, color, rect)
                self.draw_bordure()

    def draw_bordure(self):
        for tile in self.tiles :
            rect = tile.rect
            pygame.draw.rect(self.screen, "Gold", rect, width=1)
            
            if self.selected_tile and rect == self.selected_tile :
                pygame.draw.rect(self.screen, "Blue", rect, width=2)
                
            if self.possible_tiles and self.possible_tiles.__contains__(tile.coord) : 
                pygame.draw.rect(self.screen, "Green", rect, width=2)
                
            if self.all_possible_tiles and self.all_possible_tiles.__contains__(tile.coord) :
                pygame.draw.rect(self.screen, "Purple", rect, width=2)
                
                
            if self.illegal_tile and rect == self.illegal_tile  :
                pygame.draw.rect(self.screen, "Red", rect, width=2)
                
        