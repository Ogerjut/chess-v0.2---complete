import pygame


from entities.pawn import Pawn
from entities.king import King
from entities.knight import Knight
from entities.queen import Queen
from entities.bishop import Bishop
from entities.rook import Rook 

pygame.font.init()
font = pygame.font.Font(None, 32)

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.btns = []
        self.txts = []
    
    # def drawGUI(self):
    #     for btn in self.btns:
    #         btn.draw()
    #     for txt in self.txts:
    #         txt.draw()
            
    # def loadGUI(self):
    #     for btn in self.btns:
    #         self.btns.append()
    #     for txt in self.txts:
    #         txt.draw()


        
    
    
class Btn():
    """_summary_
    Create a button and display it, onClick is a method
    
        soon : can choose color ? ou avoir image png des boutons
    """
    def __init__(self, name, x, y, w, h, onClick):
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.name = name
        # self.surface = pygame.surface.Surface((w, h))
        # self.rect = self.surface.get_rect()
        # self.rect.center = (x, y)
        self.onClick = onClick
        
    def draw(self, screen) : 
        # blit l'image au lieu text, doit être une surface
        pygame.draw.rect(screen, "White", self.rect)
        text = font.render(self.name, True, "Black", "White")
        pygame.draw.rect(screen, "Yellow", self.rect, width = 2, border_radius=2)
        textrect = text.get_rect()
        textrect.center = self.rect.center
        screen.blit(text, textrect)


class Txt():
    """_summary_
    Create text
    
    """
    def __init__(self, text, x, y, w, h):
        # self.rect = pygame.rect.Rect(x, y, w, h)
        self.text = text
        self.surface = pygame.surface.Surface((w, h))
        self.rect = self.surface.get_rect()
        self.rect.center = (x, y)
        
    def draw(self, screen) : 
        # pygame.draw.rect(screen, "White", self.rect)
        # pygame.draw.rect(screen, "White", self.rect, width = 1, border_radius=3)
        text = font.render(self.text, True, "White")
        textrect = text.get_rect()
        textrect.center = self.rect.center
        screen.blit(text, textrect)
        
    
class Label():
    """_summary_
    Create text
    
    """
    def __init__(self, x, y, w, h):
        # self.rect = pygame.rect.Rect(x, y, w, h)
        self.surface = pygame.surface.Surface((w, h))
        self.rect = self.surface.get_rect()
        self.rect.center = (x, y)
        
    def draw(self, screen, txt) : 
        # pygame.draw.rect(screen, "White", self.rect)
        pygame.draw.rect(screen, "White", self.rect, width = 2, border_radius=9)
        text = font.render(txt, True, "White")
        textrect = text.get_rect()
        textrect.center = self.rect.center
        screen.blit(text, textrect)

    