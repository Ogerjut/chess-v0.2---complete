from entities.sprite import Piece

class Knight(Piece):
    def __init__(self, x, y, tile, color ):
        self.rule_move = [(1, -2),(-1, -2),(2, -1),(-2, -1),(2, 1),(-2, 1),(1, 2),(-1, 2)]
        super().__init__(x, y, tile, color, self.rule_move)
        
    def __repr__(self) -> str:
        return f' {__class__.__name__} {self.color} '
    
    def get_moves(self, init_coord, game):
        moves = []
        for move in self.rule_move :
                coord = self.calculate_coord(init_coord, move )
                if self.coord_in_board(coord):
                    moves.append(coord)
            
        # print(f"move {self.color} knight : {moves}")
        return moves


