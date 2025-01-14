from entities.sprite import Piece
        
class Bishop(Piece):
    def __init__(self, x, y, tile , color):
        self.rule_move = [(1, 1),(1, -1),(-1, -1),(-1, 1)]
        super().__init__(x, y, tile, color, self.rule_move)
    
    def __repr__(self) -> str:
        return f' {__class__.__name__} {self.color} '
    
    def get_moves(self, init_coord, game):
        moves = []    
        for move in self.rule_move:
            # print(f"check direction en cours {move} ")
            for i in range(1, 8):
                coord = self.calculate_coord_i(init_coord, move, i)
                # print(f"check coord en cours {coord} ")
                if not self.coord_in_board(coord):
                    break  # Arrêter si la coordonnée sort du plateau
                
                piece = game.get_piece_on_tile(coord)
                if piece:
                    moves.append(coord) 
                    break 
                else:
                    moves.append(coord)

        # print(f"move {self.color} bishop :", moves)
        return moves

