import pygame

class Text():
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 32) 
        self.color = (60, 30, 255)
        self.list_texts = []
        
    def AfficherVariable(self, screen, var, text_var, color, coord):
        self.var_surface = self.font.render(f" {text_var}{var}", True, color, (255,255,255))
        screen.blit(self.var_surface, coord)
        
    def AfficherText(self, screen, text, color, coord):
        self.text_surface = self.font.render(text, True, color, (255,255,255))
        screen.blit(self.text_surface, coord)

