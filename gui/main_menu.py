from gui.gui import * 
import pygame

class MainMenu : 
    def __init__(self, screen : pygame.Surface, start, online, exit ) -> None:
        self.screen = screen
        self.is_running = True 
        
        self.btns = {
            start :  Btn("Start Game", 0, self.screen.get_rect().centery, 300, 64, start),
            # online : Btn("Play Online",0, self.screen.get_rect().centery+75, 300, 64, online ),
            exit :   Btn("Exit", 0, self.screen.get_rect().centery+150, 300, 64 , exit),
        }
        
        self.btns_rect = [btn.rect for btn in self.btns.values()] 
        
    
    def draw(self):
        for btn in self.btns.values() : 
            btn : Btn
            btn.rect.centerx = self.screen.get_rect().centerx
            btn.draw(self.screen)
            
    def get_btn_by_rect(self, rect) : 
        for btn in self.btns.values() : 
            if rect == btn.rect : 
                return btn 