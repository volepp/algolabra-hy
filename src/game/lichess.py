from game import Game
import berserk
from engine import *
from board.piece import Color
from board import Result

class LichessGame(Game):

    def __init__(self, token: str, engine: Engine):
        super().__init__(engine)
        session = berserk.TokenSession(token)
        self.client = berserk.Client(session=session)
        self.engine = engine

        self.game_id = None
        self.color = None

    def run(self):
        """ Starts to wait for any challenges in Lichess.
        Once a challenge is received, it is accepted and the game is played through.
        """
        while True:
            self.wait_for_challenge()
            print("Challenge accepted. Game starting...")
            self.play()

    def play(self):
        """ Play through the current game.
        Current game is defined by self.game_id.
        """
        if self.color == Color.White:
            self.make_engine_move()
        for gs in self.client.bots.stream_game_state(self.game_id):
            self.handle_game_event(gs)
            if self.game_id is None:
                break

    def handle_game_event(self, event):
        """ Handles the given game event.
        Sets self.game_id and self.color to None if the player resigns.
        """
        if event["type"] == "gameState":
            self.handle_game_state(event)

    def handle_game_state(self, gs):
        if gs["status"] == "resigned":
            self.game_id = None
            self.color = None
            print("Opponent resigned")
            return
        
        # Get player move
        self.board.update_moves(gs["moves"])
        result = self.board.get_result()
        if result is not None:
            self.print_result_and_exit(result)
        if self.board.next_move_color() == self.color:
            self.make_engine_move()
    
    def print_result_and_exit(self, result):
        if result == Result.WHITE_WIN:
            print("White won")
        elif result == Result.BLACK_WIN:
            print("Black won")
        elif result == Result.STALEMATE:
            print("Stalemate")
        elif result == Result.DRAW:
            print("Draw")
        exit(0)

    def make_engine_move(self):
        engine_move = self.engine.make_move(self.board)
        self.client.bots.make_move(self.game_id, engine_move)
        # Don't make the move on the internal board as making a bot 
        # move will generate a new game state event.

    def get_last_move(self, movestr: str):
        """ Gets the last move from the given string of moves.
        Returns None if no moves have been made.
        """
        if len(movestr) == 0:
            return None
        moves = movestr.strip().split(" ")
        return moves[-1]

    def wait_for_challenge(self):
        """ Wait for a challenge in Lichess and accept it.
        Set self.game_id and self.color when the game starts.
        """
        for event in self.client.bots.stream_incoming_events():
            if event["type"] == "challenge":
                self.client.challenges.accept(event["challenge"]["id"])
            elif event["type"] == "gameStart":
                self.game_id = event["game"]["gameId"]
                if event["game"]["color"] == "white":
                    self.color = Color.White
                else:
                    self.color = Color.Black
                return