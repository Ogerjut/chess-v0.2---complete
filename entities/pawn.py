

from entities.sprite import Piece

        
class Pawn(Piece):
    def __init__(self, x, y, tile, color ):
        self.rule_move = [(0,1) , (0,2), (-1,1) , (1,1)]
        super().__init__(x, y, tile, color, self.rule_move)
        self.first_move = True
        
        self.can_capture_en_passant = False
        
    def __repr__(self) -> str:
        return f' {__class__.__name__} {self.color} '
    
    def calculate_coord(self, tup, tup1):
        if self.color == "white" :
            return (tup[0]-tup1[0], tup[1]-tup1[1])
        else : return (tup[0]+tup1[0], tup[1]+tup1[1])
        
    def get_moves(self, init_coord, game):
        moves = []    
        for move in self.rule_move:
            coord = self.calculate_coord(init_coord, move)

            # Vérifier si la coordonnée est dans les limites de l'échiquier
            if not self.coord_in_board(coord):
                continue

            # Gestion spécifique pour (0, 2) : vérifier d'abord (0, 1)
            if move == (0, 2):
                coord_1 = self.calculate_coord(init_coord, (0, 1))  # Case (0, 1)
                piece_1 = game.get_piece_on_tile(coord_1)           # Pièce sur (0, 1)

                if piece_1:  # Si une pièce bloque (0, 1), ne pas ajouter (0, 2)
                    # print(f"Mouvement (0,2) bloqué par une pièce sur {coord_1}")
                    continue

            # Ajouter le mouvement à la liste des mouvements possibles
            moves.append(coord)

            # Vérifier si une pièce bloque le mouvement ou la capture
            piece = game.get_piece_on_tile(coord)
            if not piece  :
                # Si aucune pièce n'est sur les cases de capture, retirer les captures
                if move in [(1, 1), (-1, 1)] and coord in moves:
                    moves.remove(coord)
                    # print(f"Move retiré : pas de pièce sur case capture {coord}")
            else:
                # Si une pièce bloque les mouvements (0, 1) ou (0, 2)
                if move in [(0, 1), (0, 2)] and coord in moves:
                    moves.remove(coord)
                    # print(f"Coord retirée, pièce sur le passage {coord}")
                
                # Si une pièce alliée bloque une case de capture, retirer
                if piece.color == self.color and move in [(1, 1), (-1, 1)] and coord in moves:
                    moves.remove(coord)
                    # print(f"Case alliée sur case capture {coord}")
                    
      
        # print("Move pawn :", moves)
        return moves


        
    def upt_first_move(self): 
        if self.first_move : 
            self.rule_move = [(0,1), (-1,1) , (1,1)]
            self.first_move = False
            

    def get_moves_check(self, init_coord, game):
        moves = []    
        for move in self.rule_move:
            coord = self.calculate_coord(init_coord, move)
            if self.coord_in_board(coord):
                moves.append(coord)

                if move in [(0,1), (0,2)]:
                    moves.remove(coord)


    
        # print("move pawn chess :", moves)
        return moves
    
    def get_move_direction(self, pos, coord):
        # calculer les coords pour la piece, si coord donnée = crd return le move
        for move in self.rule_move :
            crd = self.calculate_coord(pos, move)
            if crd == coord :
                # print("direction", move)
                return move
            
    
    def check_promotion(self, coord):
        if self.color == "white" and coord[1] == 0 :
            print("check white pawn promotion")
            return True
         
        elif self.color == "black" and coord[1] == 7 :
            self.isPromoting = True 
            print("check black pawn promotion")
            return True 
            
        else : 
            print("no promotion for this move")
            return False
            
            