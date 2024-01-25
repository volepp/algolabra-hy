from dotenv import load_dotenv
import os
import argparse
import ui
from game import Game
from board import Board
import engine
import random

# Enable loading secrets from secret/.env (e.g. LICHESS_TOKEN)
dotenv_path = os.path.join(os.path.dirname(__file__), "/secret/.env")
load_dotenv(dotenv_path)

def run(args):
    ui_client = ui.Ascii()
    player_starts = True # Player always plays white for now
    lichess_token = args.token if args.token is not None else os.getenv("LICHESS_TOKEN")
    if lichess_token is not None and args.lichess:
        ui_client = ui.Lichess(lichess_token)
        # TODO: set player_starts

    eng = engine.RandomEngine() # For now using RandomEngine for testing

    Game(ui_client=ui_client, engine=eng, player_starts=player_starts).run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lichess", help="Play in Lichess", action="store_true")
    parser.add_argument("-t", "--token", help="Lichess bot token")
    args = parser.parse_args()

    run(args)