
# from core.game import Game
# from gui.board import Tile

from entities.pawn import Pawn
from entities.king import King
from entities.knight import Knight
from entities.queen import Queen
from entities.bishop import Bishop
from entities.rook import Rook 
from entities.sprite import Piece

# from entities import *

# ajjouter pleisn de mécaniques simples comme :
# si coor dans list pos
#  si coord roi dans list pos controle alliée / ennemie


# get piece move (piece)
# get pieces moves (list piece)
# cases controlées par pièce ennemies et alliées
# 
# à partir de tout cela je peux savoir si piece.coord dans list pos ennemie ... et construire toute ma logique dans game

class MoveManager:
    # def __init__(self, game = Game) :
    def __init__(self, game ) :
        self.game = game
        self.pieces = game.pieces
        self.pawn_to_capture_en_passant : Pawn = None 
        
    def set_dest_tile(self, tile):
        self.dest_coord = tile.coord
        self.dest_rect = tile.rect.copy()

    def set_init_tile(self):
        piece = self.get_active_piece()
        self.init_rect = piece.rect.copy()
        self.init_coord = piece.pos
        
    def get_active_piece(self): return self.game.active_piece
    
    def get_current_player(self): return self.game.currentPlayer
    
    def get_ennemy_color(self) : 
        if self.get_current_player() == "white" :
            return "black"
        else : return "white "
    
    def legal_move(self) :
        self.possible_moves = []
        active_piece = self.get_active_piece()
        if active_piece :
            print(active_piece)
            print(f"from {self.init_coord} to {self.dest_coord} coord ? ")
            
            if isinstance(active_piece, King) : 
                self.check_castle()
                
            self.possible_moves = active_piece.get_moves(self.init_coord, self.game)
            
            if isinstance(active_piece, Pawn) :
                self.check_prise_en_passant()
                
            self.game.board.possible_tiles = self.possible_moves.copy()
            if self.move_is_possible() :
                return True
            
        print("coup interdit")
        return False       
    
    def cancel_move(self):
        piece = self.get_active_piece()
        piece.rect = self.init_rect
        piece.pos = self.init_coord
        
    def move_is_possible(self):
        if self.dest_coord in self.possible_moves and self.dest_coord != self.init_coord :
            print('move possible')
            return True
    
    def ally_on_dest_tile(self, tile):
        for pce in self.pieces :
            if pce.pos == tile :
                if pce.color == self.get_current_player() :
                    print("il y a une pièce alliée sur cette case" )
                    return True
        return False
                
    def ennemy_on_dest_tile(self, tile):
        for pce in self.pieces :
            if pce.pos == tile :
                if pce.color != self.get_current_player() :
                    print("il y a une pièce ennemie sur cette case" )
                    return True
        return False
                  
    def check_kill(self):
        if self.ennemy_on_dest_tile(self.dest_coord) :
            # piece = self.get_active_piece()
            # if isinstance(piece, King) :
            #     if self.check_king_ally_is_chess():
            #         return 
            self.game.kill(self.dest_coord)
        # fonction gui affichage pièces capturées
        
    def check_king_ennemy_is_chess(self) :
        # calculer si roi ennemy pos == une des nouvelles pos de la piece qui vient d'être joué ainsi que toutes les autres poices alliées (découverte)
        news_poses = []
        king : King = self.game.find_ennemy_king()
        piece = self.get_active_piece()
        # news_poses.extend(piece.get_moves(self.dest_coord, self.game)) 
        # pieces = [pce for pce in self.pieces if not pce == piece]
        
        print(f"debut check chess pour le roi ennemi {self.get_ennemy_color()}")
        for pce in self.pieces :
            if pce.color == piece.color  :
                if isinstance(pce, Pawn):
                    news_pos = pce.get_moves_check(pce.pos, self.game)
                else : news_pos = pce.get_moves(pce.pos, self.game)  
                news_poses.extend(news_pos)
        
        # à décommenter pour montrer toutes les cases possibles : 
        # self.game.board.all_possible_tiles = news_poses.copy()
        # print(self.game.board.all_possible_tiles)
                
        if king and news_poses.__contains__(king.pos) :
            king.chess = True
            king.can_castle = False
            self.game.board.illegal_tile = king.rect.copy()
            return True
        return False
    
    def king_ally_is_chess(self):
        king = self.game.find_ally_king()
        piece = self.get_active_piece()
        if king.chess and not isinstance(piece, King) :
            print("your king is chess")
            return True
        return False
        
    def check_king_ally_is_chess(self) :
        # calculer si roi pos == une des nouvelles pos de toute les piece ennemies
        
        king = self.game.find_ally_king()
        print(f"debut check chess pour le roi allié {self.get_current_player()}")
        
        # news_poses.extend(piece.get_moves(self.dest_coord, self.game)) 
        # pieces = [pce for pce in self.pieces if not pce == piece]
        
        # ------------ Faire une fonction ici
        news_poses = []
        piece = self.get_active_piece()
        for pce in self.pieces :
            if pce.color != piece.color  :
                if isinstance(pce, Pawn):
                    news_pos = pce.get_moves_check(pce.pos, self.game)
                else : news_pos = pce.get_moves(pce.pos, self.game)  
                news_poses.extend(news_pos)
        # ---------------------------------
        
        # idem L103
        # self.game.board.all_possible_tiles = news_poses.copy()
        # print(self.game.board.all_possible_tiles)
                
        if king and king.pos in news_poses :
            return True
        
        print("king not chess, active piece can move")
        return False
     
    def check_king_chessmat(self):
        active_piece = self.get_active_piece()
        king : King = self.game.find_ennemy_king()
        if not king.chess :
            return False
        
        print(f"debut check mat pour le roi {self.get_ennemy_color()}")
        #--------------------------- récupère la ligne de vue de la pièce qui a mis échec (case à couvrir)
        ldv = []
        # roi et pion n'ont pas de ldv 
        if not isinstance(active_piece,(Knight, Pawn)):
            ldv= (self.LDV()) 
        # attention avec pion, prendre en compte case capture et non move      
        
        # vérifier si piece ennemis peuvent couvrir la ldv (if coord piece dans ldv)
        # récupère toutes les positions possibles des pièces et si une pos correspond à une pos dans ldv alors peut couvrir et pas echec et mat
        all_moves = [] #moves ennemis
        king_moves = []
        for piece in self.pieces  :
            if piece.color != self.get_current_player() :
                if isinstance(piece, King):
                    king_moves = piece.get_moves(piece.pos, self.game)
                elif isinstance(piece, Pawn):
                    pce_moves = piece.get_moves(piece.pos, self.game)
                    pce_moves.extend(piece.get_moves_check(piece.pos, self.game))
                    all_moves.extend(pce_moves)
                elif isinstance(piece, (Queen, Rook, Bishop, Knight)) : 
                    pce_moves = piece.get_moves(piece.pos, self.game)  
                    all_moves.extend(pce_moves)
        
    
        #-------------- récupère les cases possibles des pièces alliées pour savoir si roi pourra s'y déplacer et si active pièce protégée
        poses = []
        # print(f"Active piece : {active_piece}")
        for pce in self.pieces :
            if pce.color == self.get_current_player() :
                if isinstance(pce, Pawn):
                    news_pos = pce.get_moves_check(pce.pos, self.game)
                else : news_pos = pce.get_moves(pce.pos, self.game)  
                poses.extend(news_pos)
                # print(f"piece : {pce}")
                # print(f"pos : {news_pos}")
                      
        # print('king ennemy moves (before validation)', king_moves)               
        # print("positions controlled by ally :", poses)
        valid_king_moves = [move for move in king_moves if move not in poses]
        king_moves = valid_king_moves
        # print('king moves :', king_moves)
        
        # ------------------ s'il y a au moins une case possible, pas d'echec et mat
        final_poses = []
        for move in all_moves :
            if move in ldv :
                final_poses.append(move)
        # print(f"final poses : {final_poses} \nking moves : {king_moves}")
        
        if len(king_moves)==0 and len(final_poses) == 0 :
            king.mat = True 
            return True
        else : return False
                
    def LDV (self):
        ldv = [self.dest_coord]
        piece = self.get_active_piece()
        king = self.game.find_ennemy_king()
        direction_move = piece.get_move_direction(self.dest_coord, king.pos)
        king_pos = king.pos
        piece_pos = piece.pos
        nb = 0
    
        dx = abs(king_pos[0]-piece_pos[0])
        dy = abs(king_pos[1]-piece_pos[1])
        
        if dx == dy : nb = dx
        if dx == 0 : nb = dy
        if dy == 0 : nb = dx 
        
        # print("distance king - 1st piece : ", nb)
        if nb >= 1 :
            for i in range(1, nb):
                coord = piece.calculate_coord_i(self.dest_coord, direction_move, i)
                # print("coord ldv",coord)
                if piece.coord_in_board(coord) :
                        if not coord == king_pos : 
                            ldv.append(coord)
                        
        # print("ldv", ldv)
        return ldv
    
    def get_all_moves_capture(self, piece) :
        moves = []
        for pce in self.pieces :
            if pce.color == piece.color  :
                if isinstance(pce, Pawn):
                    news_pos = pce.get_moves_check(pce.pos, self.game)
                else : news_pos = pce.get_moves(pce.pos, self.game)  
                moves.extend(news_pos)    
        return moves
    
    # ------------------- A faire : idem mais avec pièces alliés -----------------
    def get_tiles_controlled_by_ennemy(self) :
        moves = []
        for pce in self.pieces :
            if pce.color != self.get_current_player()  :
                if isinstance(pce, Pawn):
                    news_pos = pce.get_moves_check(pce.pos, self.game)
                else : news_pos = pce.get_moves(pce.pos, self.game)  
                moves.extend(news_pos)    
        return moves
    # ------------------------------------------------------------------
    
    def check_castle(self): 
        print("check possibilities to do castle")
        king : King = self.game.find_ally_king()
        
        if not king.can_castle :
            print("king cannot castle") 
            return 
        
        if king.has_castle :
            print("king has already castle") 
            return 
        
        coord_to_test_for_left_castle = [(king.pos[0]-1, king.pos[1]), (king.pos[0]-2, king.pos[1]), (king.pos[0]-3, king.pos[1])]
        coord_to_check_for_left_castle = [(king.pos[0]-1, king.pos[1]), (king.pos[0]-2, king.pos[1])]
        coord_to_test_for_right_castle = [(king.pos[0]+1, king.pos[1]), (king.pos[0]+2, king.pos[1])]
            
        left_castle_list = [self.game.get_piece_on_tile(coord) for coord in coord_to_test_for_left_castle if self.game.get_piece_on_tile(coord) is not None]
        right_castle_list = [self.game.get_piece_on_tile(coord) for coord in coord_to_test_for_right_castle if self.game.get_piece_on_tile(coord) is not None ]
        
        #-----récupérer toutes les cases controlées par le camp ennemi, si une de ces cases est sur la ligne de castle 
        if self.check_can_castle(coord_to_check_for_left_castle) and len(left_castle_list) == 0: 
            king.can_left_castle = True
            print("king can left castle")
        
        if self.check_can_castle(coord_to_test_for_right_castle) and len(right_castle_list) == 0: 
            king.can_right_castle = True
            print("king can right castle")
                
    def check_can_castle(self, coords: list):
        tiles_controlled_by_ennemy = self.get_tiles_controlled_by_ennemy()
        for coord in coords : 
            if coord in tiles_controlled_by_ennemy :
                print("king cannt castle, ennemy piece control")
                return False 
        return True 
    
    def check_prise_en_passant(self): 
        active_piece : Pawn = self.get_active_piece()
        if not self.pawn_to_capture_en_passant : 
            print("pas de pion à capturer en passant")
            return
        else :
            if active_piece.color == "white" and active_piece.pos[1] == 3  : 
                self.possible_moves.append((self.pawn_to_capture_en_passant.pos[0], self.pawn_to_capture_en_passant.pos[1]-1))
                active_piece.can_capture_en_passant = True
                
            if active_piece.color == "black" and  active_piece.pos[1] == 4 :
                self.possible_moves.append((self.pawn_to_capture_en_passant.pos[0], self.pawn_to_capture_en_passant.pos[1]+1))
                active_piece.can_capture_en_passant = True

            
                    