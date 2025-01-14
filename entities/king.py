
from entities.sprite import Piece

class King(Piece):
    def __init__(self, x, y, tile, color):
        self.rule_move = [(1, 1),(1, -1),(-1, -1),(-1, 1), (1, 0),(-1, 0),(0, 1),(0, -1)] 
        # self.rule_castle = [()]
        super().__init__(x, y, tile, color, self.rule_move)
        self.chess = False
        self.mat = False
        
        self.can_castle = True 
        self.can_left_castle = False
        self.can_right_castle = False
        self.has_castle = False
        
    def __repr__(self) -> str:
        return f' {__class__.__name__} {self.color} '
    
    def get_moves(self, init_coord, game):
        moves = [] 
        
        if not self.has_castle and self.can_castle :
            if self.can_left_castle :
                print("added coord because can left castle")
                self.rule_move.append((-2,0))
                
            if self.can_right_castle :
                print("added coord because can right castle")
                self.rule_move.append((2,0))
                
                
        for move in self.rule_move:
            coord = self.calculate_coord(init_coord, move)
            if self.coord_in_board(coord):
                moves.append(coord)
        
            piece = game.get_piece_on_tile(coord)
                # Vérifier si une pièce bloque le chemin
            if piece :
                if piece.color == self.color : 
                    moves.remove(coord)
                    
      
        if not self.has_castle and self.can_castle :
            if self.can_left_castle :
                self.rule_move.remove((-2,0))
                
            if self.can_right_castle : 
                self.rule_move.remove((2,0))
        
        print(f"move {self.color} king {moves}")
        return moves
    


        

        