import berserk

class Lichess:

    def __init__(self, token: str):
        session = berserk.TokenSession(token)
        self.client = berserk.Client(session=session)
        self.game_id = None

    def start(self):
        self.wait_for_challenge()
    
    def update(self, move):
        """Updates the given move to the UI if the move is not None.
        Then waits for the user to make a move and returns it.
        Returns None if the player resigns.
        """

        if self.game_id is None:
           return None
        
        print(move)
        if move is not None:
            self.client.bots.make_move(self.game_id, move)
        
        # TODO: wait for player move

        if self.game_id is None:
            return None
        
        return None

    def wait_for_challenge(self):
        for event in self.client.bots.stream_incoming_events():
            if event["type"] == "challenge":
                self.client.challenges.accept(event["challenge"]["id"])
            elif event["type"] == "gameStart":
                self.game_id = event["game"]["gameId"]