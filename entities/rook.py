from entities.sprite import Piece

class Rook(Piece):
    def __init__(self, x, y, tile, color ):
        self.rule_move = [(1, 0),(-1, 0),(0, 1),(0, -1)]
        super().__init__(x, y, tile, color, self.rule_move)
        
    def __repr__(self) -> str:
        return f' {__class__.__name__} {self.color} '
    
    def get_moves(self, init_coord, game):
        moves = []    
        for move in self.rule_move:
            for i in range(1, 8):
                coord = self.calculate_coord_i(init_coord, move, i)
                if self.coord_in_board(coord):
                    moves.append(coord)
                    
                    #  refaire une fonction avec for coord in moves (dans movemanager après avoir le get_moeves())
                piece = game.get_piece_on_tile(coord)
                if piece:
                    moves.append(coord) 
                    break 
                else:
                    moves.append(coord)

        # print(f" move {self.color} rook :", moves)
        return moves