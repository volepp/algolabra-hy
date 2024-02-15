from board import Board, Position, Result
from board.piece import Move, Color
import numpy as np
import math
import time

class Engine:

    MIN_EVAL_WHITE = -math.inf
    MIN_EVAL_BLACK = math.inf

    def __init__(self):
        # Max depth the minmax algorithm searches
        self.max_depth = 2
        self.latest_evaluation = 0

    def make_move(self, board: Board) -> Move:
        """ Returns the next move
        """
        (move, eval) = self.find_best_move(board)
        self.latest_evaluation = eval
        return move
    
    def find_best_move(self, board: Board):
        """ Finds the best move in the position using a minmax algorithm.
        At each step, the position is evaluated using the evaluate_position function.
        In the end, the move that leads to the best position (according to evaluate_position)
        for the player who moves next will be played.
        Returns the best move and the evaluation for that move.
        """
        player_to_move = board.next_move_color()
        legal_moves = board.get_legal_moves(player_to_move)
        self.sort_moves_by_potential(board, legal_moves)
        best_move_eval = self.MIN_EVAL_WHITE if player_to_move == Color.White else self.MIN_EVAL_BLACK
        best_move = None
        for move in legal_moves:
            print("Evaluating", move, end=" ")
            eval_start_time = time.time()
            # self.max_depth-1 because this loop can be considered the first level
            eval, nr_nodes_visited = self.minmax_ab_eval_move(board, self.max_depth-1, move)
            print(", eval:", eval, "nr nodes:", nr_nodes_visited, ", time:", time.time()-eval_start_time)
            if player_to_move == Color.White and eval > best_move_eval:
                best_move_eval = eval
                best_move = move
                if eval == math.inf:
                    # Stop after finding the first checkmate
                    break
            elif player_to_move == Color.Black and eval < best_move_eval:
                best_move_eval = eval
                best_move = move
                if eval == -math.inf:
                    # Stop after finding the first checkmate
                    break

        return (best_move, best_move_eval)
    
    def minmax_ab_eval_move(self, board: Board, depth: int, move: Move, alpha: float = -math.inf, beta: float = math.inf):
        """ Minmax algorithm with alpha-beta pruning that evaluates the given move by recursively going through the 
        possible variations that can follow with the given depth and evaluates the position at each step. 
        It will return the best possible evaluation it can find for the given player to move. 
        The evaluation should be interpreted such that the more positive the value is, 
        the better the position is for white and viceversa.
        """
        nr_nodes_visited = 1
        result, move_played = board.play_move(move)
        if depth == 0 or result is not None:
            eval = self.evaluate_board(board)
            if move_played:
                board.undo_last_move()
            return eval, nr_nodes_visited
        
        player_to_move = board.next_move_color()
        legal_moves = board.get_legal_moves(player_to_move)
        self.sort_moves_by_potential(board, legal_moves)
        if player_to_move == Color.White:
            best_eval = -math.inf
            for nmove in legal_moves:
                eval, nnodes = self.minmax_ab_eval_move(board, depth-1, nmove, alpha=alpha, beta=beta)
                nr_nodes_visited += nnodes
                best_eval = max(best_eval, eval)
                if best_eval > beta:
                    print("beta cutoff")
                    break
                alpha = max(alpha, best_eval)
            board.undo_last_move()
            return best_eval, nr_nodes_visited
        else:
            best_eval = math.inf
            for nmove in legal_moves:
                eval, nnodes = self.minmax_ab_eval_move(board, depth-1, nmove, alpha=alpha, beta=beta)
                nr_nodes_visited += nnodes
                best_eval = min(best_eval, eval)
                if best_eval < alpha:
                    print("alpha cutoff")
                    break
                beta = min(beta, best_eval)
            board.undo_last_move()
            return best_eval, nr_nodes_visited

    def evaluate_board(self, board: Board) -> float:
        result = board.get_result()
        if result != None:
            return self.get_evaluation_from_result(result)

        return self.evaluate_position(board.position)
    
    def evaluate_position(self, position: Position) -> float:
        """ Evaluates the given position.
        Currently just calculates the amount of material each player has
        on the board and returns the difference.
        """
        pos_material = np.array([piece.value if piece is not None else 0 \
                                  for (_,_), piece in np.ndenumerate(position.position)])
        # White -> 1, black -> -1, None -> 0
        pos_color = np.array([int(piece.color) if piece is not None else 0\
                              for (_,_), piece in np.ndenumerate(position.position)])
        # Element-wise multiplication
        pos_material = np.multiply(pos_material, pos_color)
        eval = np.sum(pos_material)

        # Also take into account the controlled squares weighted by how important they are
        white_control_score, black_control_score = position.get_control_scores()
        eval += white_control_score-black_control_score

        return eval

    def get_evaluation_from_result(self, result: Result) -> float:
        if result == Result.WHITE_WIN:
            return math.inf
        elif result == Result.BLACK_WIN:
            return -math.inf
        else: 
            return 0
        
    def sort_moves_by_potential(self, board: np.array, moves):
        """ Sorts the moves by how much potential they have to be good.  
        """
        # Sort by score. Highest score first
        moves.sort(key=lambda m: self.score_move_potential(board, m), reverse=True)
        return moves

    def score_move_potential(self, board: np.array, move):
        """ Scores the move by how interesting it is. 
        Captures are given higher values than
        other moves.
        """
        moved_piece = board.position[tuple(move.from_square)]
        captured_piece = board.position[tuple(move.to_square)]
        if captured_piece is None:
            return 0
        elif captured_piece.color == moved_piece.color:
            return 0
        
        return 1