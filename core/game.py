import pygame

from gui.board import Board

from entities.bishop import Bishop
from entities.queen import Queen
from entities.king import King
from entities.knight import Knight
from entities.rook import Rook
from entities.pawn import Pawn

from core.move_manager import MoveManager

class Game():
    def __init__(self, gui, screen) :
        self.is_running = False 
        self.screen = screen
        self.gui = gui
    
    
    def run_game(self): 
        self.is_running = True
        self.board = Board(self.screen)
        self.board.load()
        self.tiles = self.board.tiles
        self.all_sprites = pygame.sprite.Group()
        self.load_game()
                
    # dans class player/client dans le futur (on line)
    def change_player(self):
        if self.currentPlayer == "white" :
            self.currentPlayer = "black"
        else : self.currentPlayer = "white"
        self.active_piece = None
        # print(self.currentPlayer)
        #  board.rotate() ici
    
    def online_mode(self):
        print("online mode à venir")
    
    def register_pieces(self):
        self.pieces = [
            King(0 ,0, (4,7), "white"),
            Queen(64 ,0, (3,7), "white"),
            Bishop(128 ,0, (2,7), "white"),
            Knight(192 ,0, (1,7), "white"),
            Bishop(128 ,0, (5,7), "white"),
            Knight(192 ,0, (6,7), "white"),
            Rook(256 ,0, (0,7), "white"),
            Rook(256 ,0, (7,7), "white"),
            King(0 ,64, (4,0), "black"),
            Queen(64 ,64, (3,0), "black"),
            Bishop(128 ,64, (2,0), "black"),
            Knight(192 ,64, (1,0), "black"),
            Bishop(128 ,64, (5,0), "black"),
            Knight(192 ,64, (6,0), "black"),
            Rook(256 ,64, (0,0), "black"),
            Rook(256 ,64, (7,0), "black")
        ]
        # self.pieces = [
        #     King(0 ,0, (4,7), "white"),
        #     Queen(64 ,0, (0,4), "white"),
        #     Bishop(128 ,0, (4,5), "white"),
        #     Knight(192 ,0, (1,5), "white"),
        #     Bishop(128 ,0, (7,5), "white"),
        #     Knight(192 ,0, (6,7), "white"),
        #     Rook(256 ,0, (0,7), "white"),
        #     Rook(256 ,0, (7,7), "white"),
        #     King(0 ,64, (4,0), "black"),
        #     # Queen(64 ,64, (3,0), "black"),
        #     # Bishop(128 ,64, (2,0), "black"),
        #     Knight(192 ,64, (1,0), "black"),
        #     Bishop(128 ,64, (5,0), "black"),
        #     Knight(192 ,64, (6,0), "black"),
        #     Rook(256 ,64, (0,0), "black"),
        #     Rook(256 ,64, (7,0), "black")
        # ]
        for i in range(0,8):
            self.pieces.append(Pawn(320,0, (i,6), "white"))
            self.pieces.append(Pawn(320,64, (i,1), "black"))

    def set_piece_tile(self):
        for piece in self.pieces:
            for tile in self.tiles :
                if not piece.pos == tile.coord :
                    continue
                else : 
                    piece.rect.topleft = tile.rect.topleft
                    self.all_sprites.add(piece)
                         
    def select_piece(self, pos):                   
        if self.active_piece is None :   
            for piece in self.pieces:
                if piece.rect.collidepoint(pos) and piece.color == self.currentPlayer :    
                    # à partir d'ici j'ai la main sur la pièce selectionnée
                    self.active_piece = piece
                    self.move_manager.set_init_tile()
                    self.board.selected_tile = piece.rect.copy()
                    self.board.illegal_tile = None
                    self.board.all_possible_tiles = None
                   
    # def pawn_promotion(self, newpiece):
    #     if self.active_piece.color == "white" : 
    #         match newpiece : 
    #             case 'queen' : 
    #                 Queen(64,0, self.active_piece.pos, "white")
    
    def pawn_promotion(self):
        if self.active_piece.color == "white" : 
            new_piece = Queen(64,0, self.active_piece.pos, "white")
        else : new_piece = Queen(64,64, self.active_piece.pos, "black")
        
        self.all_sprites.remove(self.active_piece)
        self.pieces.remove(self.active_piece)
        
        self.pieces.append(new_piece)
        self.all_sprites.add(new_piece)
        
        self.set_piece_tile()
                
        
                              
    def drop_piece(self, pos):
        if self.active_piece is None:
            return
        
        for tile in self.tiles:
            rect = tile.rect
            if not rect.collidepoint(pos):
                continue  # Passez à la prochaine pos si pas collision
            
            self.move_manager.set_dest_tile(tile)
            if not self.move_manager.legal_move() or self.move_manager.ally_on_dest_tile(tile.coord):
                self.reset_active_piece(tile.coord)
                return 
               
            if self.active_piece.pos != tile.coord :
                if not self.move_active_piece(rect, tile.coord):
                    self.reset_active_piece(tile.coord)
                    return
                
                if not self.move_manager.check_king_chessmat() :   
                    k = self.find_ally_king()
                    k.chess = False
                    if not k.has_castle :
                        k.can_castle = True
                        
                    self.board.possible_tiles = None
                    self.captured_piece = False
                    print("end turn \n")
                    self.change_player()
                    
                else :
                    self.game_over()
                    self.over = True
                
            return

    
    def kill(self, coord):
        ennemy = self.get_piece_on_tile(coord)
        self.last_piece_killed = ennemy
        self.captured_piece = True 
        self.pieces.remove(ennemy)
        self.all_sprites.remove(ennemy)
        print("piece captured")
      
                
    def cancel_kill(self):
        self.pieces.append(self.last_piece_killed)
        self.all_sprites.add(self.last_piece_killed)
            
    def move_active_piece(self, rect, coord):
        # faire le mouvement et le kill s'il y a, puis recalculer l'état du plateau. Si roi allié echec, les annuler. 
        self.move_manager.check_kill()
        self.active_piece.move(rect, coord)
        
        # check si s'est mis echec si oui, cancel move et kill
        if self.move_manager.check_king_ally_is_chess():
            self.move_manager.cancel_move()
            if self.captured_piece : 
                self.cancel_kill()
                self.captured_piece = False
            print("move and/or kill cancelled, otherwise king chess")
            return False
    
        if isinstance(self.active_piece, King) :
            if not self.active_piece.has_castle and self.active_piece.can_castle :
                distance_x = self.active_piece.pos[0] - self.move_manager.init_coord[0]
                # print(f" distance x : {distance_x}")
                if distance_x == 2 :
                    # print("right castle")
                    if self.move_manager.get_current_player() == "white" :
                        right_tower : Rook = self.get_piece_on_tile((7,7))
                        right_tower.move(right_tower.rect, (5,7))
                    else : 
                        right_tower : Rook = self.get_piece_on_tile((7,0))
                        right_tower.move(right_tower.rect, (5,0))
                        
                if distance_x == -2 : 
                    # print('left castle ')
                    if self.move_manager.get_current_player() == "white" :
                        left_tower : Rook = self.get_piece_on_tile((0,7))
                        left_tower.move(left_tower.rect, (3,7))
                    else : 
                        left_tower : Rook = self.get_piece_on_tile((0,0))
                        left_tower.move(left_tower.rect, (3,0))
                
                self.set_piece_tile()
                self.active_piece.has_castle = True 
        
        if isinstance(self.active_piece, Pawn):
            # si pion a bougé et a capturé en diagonale sur prise en passant, kill 
            if self.active_piece.can_capture_en_passant : 
                print(f"active piece : {self.active_piece}")
                print(f'pawn to capture en passant : {self.move_manager.pawn_to_capture_en_passant}')
                dist_x = abs(self.active_piece.pos[0] - self.move_manager.pawn_to_capture_en_passant.pos[0])
                if dist_x == 0 : 
                    print(f"pion à capturer : {self.move_manager.pawn_to_capture_en_passant}")
                    self.kill(self.move_manager.pawn_to_capture_en_passant.pos)
                self.active_piece.can_capture_en_passant = False

            if self.active_piece.first_move : 
                distance_y = abs(self.active_piece.pos[1] - self.move_manager.init_coord[1])
                print(f"dist_y : {distance_y}")
                if distance_y == 2 : 
                    self.move_manager.pawn_to_capture_en_passant = self.active_piece
                    print(" prise en passant possible ")
                
            self.active_piece.upt_first_move()
            
            if self.active_piece.check_promotion(coord) :
                self.pawn_promotion()
                        
        if self.move_manager.check_king_ennemy_is_chess() :   
            print("king ennemy is chess")
        
            #     if not self.last_piece_killed and self.move_manager.pawn_to_capture_en_passant : 
            # self.move_manager.pawn_to_capture_en_passant = None 
        
       
        print("piece moved")
        return True
        
    def find_ennemy_king(self):
        for piece in self.pieces : 
            if piece.color != self.currentPlayer and isinstance(piece, King) :
                return piece
    
    def find_ally_king(self):
        for piece in self.pieces : 
            if piece.color == self.currentPlayer and isinstance(piece, King) :
                return piece
    
    def reset_active_piece(self, coord):
        if self.active_piece :
            self.board.illegal_tile = self.get_rect_tile(coord)
            self.active_piece.rect.topleft = self.move_manager.init_rect.topleft
            self.board.selected_tile = None
            self.board.all_possible_tiles = None
            self.active_piece = None
        
    def get_piece_on_tile(self, coord) :
        for piece in self.pieces :
            if piece.pos == coord :
                return piece
            
    def get_rect_tile(self, coord) -> pygame.Rect :
        for tile in self.tiles :
            if tile.coord == coord :
                return tile.rect.copy()
    
    def game_over(self):
        print("game over")
        self.active_piece = None
        king = self.find_ennemy_king()
        if king.mat : 
            print(f" Les {self.currentPlayer} ont gagné ")
    
    
    def load_game(self) :
        print("nouvelle partie")
        self.over = False
        self.active_piece = None
        self.captured_piece = False
        self.last_piece_killed = None
        self.board.selected_tile = []
        self.board.all_possible_tiles = []
        self.all_sprites.empty()
        self.register_pieces()
        self.set_piece_tile()
        self.currentPlayer = "white"
        self.move_manager = MoveManager(self)
        
    
    def update(self):
        self.all_sprites.update() 
    
    def draw(self, screen):
        self.board.draw()
        self.all_sprites.draw(screen)
           
        
    