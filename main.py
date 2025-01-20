####################################################### AMELIORATIONS ##########################################
# classe Player (online mode) 
# restructurer le jeu avec architecture type Modèle, Vue, Controlleur
# promotion pion : ok mais a rendre asynchrone, avec choix de la pièce (reine auto)
# log avec move piece précédente
# meilleur gui : vignette pièces capturées, temps écoulé, différents modes de jeu (sans temps, avec temps)
####################################################################################################################

import pygame

from core.game import Game
from gui.gui import *
from gui.main_menu import MainMenu

VERSION = 0.2

class App:
    def __init__(self) -> None:
        self.isRunning = True
        self.window = pygame.display.set_mode((768,768))
        pygame.display.set_caption(f'Chess Game {VERSION} ')
        self.clock = pygame.time.Clock()
        
        self.gui = GUI(self.window)
        
        self.game = Game(self.gui, self.window)
        
        self.main_menu = MainMenu(self.window, self.game.run_game, self.game.online_mode, self.exit)
        # passer ces variables en mode liste dans une fonction du gui ??
        self.label1 = Label(660, 334, 96, 32)
        self.txt1 = Txt("Trait au : ", 660, 304, 96, 32)
        # self.btn_replay = Btn("Rejouer", self.window.get_rect().centerx,  self.window.get_rect().centery, 200,20, self.game.load_game)
        self.btn_replay = Btn("Rejouer", 600,  334, 96, 32, self.game.load_game)
        
        # promotion ui
        # self.txt_promo = Txt("Promotion du pion",self.window.get_rect().centerx,25,300,0)
        # self.queen_promo = Txt("Reine", self.window.get_rect().centerx,50,300,64)

        
    def draw(self):
        # faire fonction dans gui : drawGU
        self.game.draw(self.window)
        if self.game.over : 
            self.btn_replay.draw(self.window)
            
        else : 
            self.label1.draw(self.window, self.game.currentPlayer)
            self.txt1.draw(self.window)
            
        # if self.game.pawn_promoting :
        #     self.txt_promo.draw(self.window)
        #     self.queen_promo.draw(self.window)
            
        
    def update(self):
        self.game.update()
        
    def exit(self) :
        self.isRunning = False
    
    def run(self):
        
        while self.isRunning :
            self.window.fill("Black")
            
            if self.game.is_running : 
                self.draw()
                self.update()
            
            if self.main_menu.is_running : 
                self.main_menu.draw()
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.exit()
                    
                if e.type == pygame.MOUSEBUTTONDOWN :
                    pos = pygame.mouse.get_pos()
                    # print(pos)
                    if e.button == 1 :
                        if self.game.is_running : 
                            if not self.game.over : 
                                self.game.select_piece(pos)
                            else : 
                                if self.btn_replay.rect.collidepoint(pos):
                                    self.btn_replay.onClick()
                        
                        if self.main_menu.is_running : 
                            for rect in self.main_menu.btns_rect : 
                                if rect.collidepoint(pos) : 
                                    btn : Btn = self.main_menu.get_btn_by_rect(rect)
                                    btn.onClick() 
                                    self.main_menu.is_running = False 
                    
                if e.type == pygame.MOUSEMOTION :
                    if self.game.is_running : 
                        if self.game.active_piece is not None : 
                            self.game.active_piece.rect.move_ip(e.rel)
                        
                if e.type == pygame.MOUSEBUTTONUP :
                    if self.game.is_running : 
                        pos = pygame.mouse.get_pos()
                        if e.button == 1:
                            self.game.drop_piece(pos)
                    
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

if __name__ == '__main__' :
    pygame.init()
    app= App()
    app.run()   