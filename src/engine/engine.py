from board import Board, Position, Result
from board.piece import Move, Color, King
import numpy as np
import math
import time

class Engine:

    MIN_EVAL_WHITE = -math.inf
    MIN_EVAL_BLACK = math.inf

    def __init__(self):
        # Max depth the minmax algorithm searches
        self.latest_evaluation = 0
        # Stores the best move for a position (position stored as fen)
        # This is used for prioritizing the moves that have previously been found
        # to be the best in certain positions when analyzing with greater depth.
        self.move_memory = {}

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
        max_time_per_iteration_secs = 5
        max_depth = 20

        player_to_move = board.next_move_color()
        legal_moves = board.get_legal_moves(player_to_move)
        # This can be regarded as the first iteration (depth 1)
        legal_moves = self.sort_moves_by_evaluation(board, legal_moves, player_to_move)
        best_move = legal_moves[0]

        board_fen = board.fen()

        start_of_search_ts = time.time()
        for current_depth in range(2, max_depth):
            start_time = time.time()
            alpha = -math.inf
            beta = math.inf
            best_move_eval = -math.inf if player_to_move == Color.White else math.inf
            for move in legal_moves:
                print("Evaluating", move, end=" ")
                eval_start_time = time.time()
                # current_depth-1 as this loop already goes through the depth 1 moves
                eval, nr_nodes_visited = self.minmax_ab_eval_move(board, current_depth-1, move, alpha=alpha, beta=beta)
                print(", eval:", eval, "nr nodes:", nr_nodes_visited, ", time:", time.time()-eval_start_time, ", depth:", current_depth)
                if player_to_move == Color.White and eval > best_move_eval:
                    best_move_eval = eval
                    best_move = move
                    if eval == math.inf:
                        # Stop after finding the first checkmate
                        break
                    alpha = best_move_eval
                elif player_to_move == Color.Black and eval < best_move_eval:
                    best_move_eval = eval
                    best_move = move
                    if eval == -math.inf:
                        # Stop after finding the first checkmate
                        break
                    beta = best_move_eval

            self.move_memory[board_fen] = best_move
            legal_moves = self.sort_best_move_first(board, legal_moves)

            time_elapsed = time.time()-start_time
            if time_elapsed > max_time_per_iteration_secs or abs(best_move_eval) == math.inf:
                print(f"Evaluation: {best_move_eval}, depth: {current_depth}, time: {time.time()-start_of_search_ts} seconds")
                return (best_move, best_move_eval)

        print(f"Evaluation: {best_move_eval}, depth: {current_depth}, time: {time.time()-start_of_search_ts} seconds")
        return (best_move, best_move_eval)

    def sort_best_move_first(self, board: Board, moves):
        """ Sorts the given moves so that the move that has
        previously been categorized the best in the given position
        is placed first. Does nothing if no best move has been stored 
        for the position.
        Returns the sorted moves.
        """
        board_fen = board.fen()
        if board_fen not in self.move_memory:
            return moves

        best_move_index = moves.index(self.move_memory[board_fen])
        return [moves[best_move_index]] + \
                    moves[:best_move_index] + \
                    moves[best_move_index+1:]
    
    def minmax_ab_eval_move(self, board: Board, depth: int, move: Move, alpha: float = -math.inf, beta: float = math.inf):
        """ Minmax algorithm with alpha-beta pruning that evaluates the given move by recursively going through the 
        possible variations that can follow with the given depth and evaluates the position at each step. 
        It will return the best possible evaluation it can find for the given player to move. 
        The evaluation should be interpreted such that the more positive the value is, 
        the better the position is for white and viceversa.
        """
        nr_nodes_visited = 1
        if depth == 0:
            eval = self.evaluate_position_after_move(board.position, move)
            return eval, nr_nodes_visited
        
        # The move can be assumed legal
        result, _ = board.play_move(move, check_legality=False)
        if result is not None:
            board.undo_last_move()
            return self.get_evaluation_from_result(result), nr_nodes_visited
        
        player_to_move = board.next_move_color()
        legal_moves = board.get_legal_moves(player_to_move)
        # Prioritize best evaluated move (from cache)
        legal_moves = self.sort_best_move_first(board, legal_moves)
        
        if player_to_move == Color.White:
            best_eval = -math.inf
            for nmove in legal_moves:
                eval, nnodes = self.minmax_ab_eval_move(board, depth-1, nmove, alpha=alpha, beta=beta)
                nr_nodes_visited += nnodes
                best_eval = max(best_eval, eval)
                alpha = max(alpha, best_eval)

                if best_eval > beta:
                    break
            board.undo_last_move()
            return best_eval, nr_nodes_visited
        else:
            best_eval = math.inf
            for nmove in legal_moves:
                eval, nnodes = self.minmax_ab_eval_move(board, depth-1, nmove, alpha=alpha, beta=beta)
                nr_nodes_visited += nnodes
                best_eval = min(best_eval, eval)
                beta = min(beta, best_eval)

                if best_eval < alpha:
                    break
            board.undo_last_move()
            return best_eval, nr_nodes_visited
    
    def evaluate_position_after_move(self, position: Position, move: Move) -> float:
        """ Evaluates the given position after the move.
        """
        # First calculate the "base" evaluation for the current board

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

        # Then update the evaluation based on the move 

        # First update the score for the piece from the controlled squares
        moved_piece = position[tuple(move.from_square)]
        original_square = moved_piece.square
        piece_control_score_loss = position.get_piece_control_score(moved_piece)
        moved_piece.square = move.to_square
        moved_piece.calculate_controlled_squares(position.position)

        piece_control_score_gain = position.get_piece_control_score(moved_piece)

        if moved_piece.color == Color.White:
            white_control_score += piece_control_score_gain - piece_control_score_loss
        else:
            black_control_score += piece_control_score_gain - piece_control_score_loss

        # Move piece back
        moved_piece.square = original_square
        moved_piece.calculate_controlled_squares(position.position)
        
        # If the moved piece can be captured after the move, we have to remove it's value from
        # the evaluation just to be safe. Otherwise, with odd depth (e.g. 3), we can run into situations
        # where the AI captures a piece in the end without realizing that the opponent can capture it
        # directly after. This could result in the AI making nonsensical moves and not protecting its pieces.

        if moved_piece.color == Color.White:
            if position.black_controlled_squares[tuple(move.to_square)]:
                eval -= (moved_piece.value+piece_control_score_loss)
        elif position.white_controlled_squares[tuple(move.to_square)]:
            eval += (moved_piece.value+piece_control_score_loss)

        # If another piece is captured, update the control score for the captured piece's side
        # and take the material loss into account.
        # Here the move is assumed to be legal.

        captured_piece = position[tuple(move.to_square)]
        if captured_piece is None:
            # No captured piece
            return eval

        # First, update the material count
        if captured_piece.color == Color.White:
            eval -= captured_piece.value
        else:
            eval += captured_piece.value

        # Then update the control score
        if captured_piece.color == Color.White:
            eval -= position.get_piece_control_score(captured_piece)
        else:
            eval += position.get_piece_control_score(captured_piece)

        return eval

    def get_evaluation_from_result(self, result: Result) -> float:
        if result == Result.WHITE_WIN:
            return math.inf
        elif result == Result.BLACK_WIN:
            return -math.inf
        else: 
            return 0
        
    def sort_moves_by_evaluation(self, board: np.array, moves, player_color):
        """ Sorts the moves by how much potential they have to be good.  
        """
        evals = np.empty(len(moves), dtype=float)
        for i, move in enumerate(moves):
            evals[i] = self.evaluate_position_after_move(board.position, move)

        sorted_indices = np.argsort(evals) # Ascending (first is best for black)
        if player_color == Color.White:
            sorted_indices = sorted_indices[::-1] # Descending
        moves = [moves[i] for i in sorted_indices]
        # Sort by score. Highest score first
        return moves