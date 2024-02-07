from dotenv import load_dotenv
import os
import argparse
from game import *
from board import Board
import engine
import random

# Enable loading secrets from secret/.env (e.g. LICHESS_TOKEN)
load_dotenv("secret/.env")

def run(args):
    #eng = engine.RandomEngine() # For now using RandomEngine for testing
    eng = engine.Engine()

    game = AsciiGame(engine=eng)
    lichess_token = args.token if args.token else os.getenv("LICHESS_TOKEN")
    if lichess_token is not None and args.lichess:
        game = LichessGame(lichess_token, eng)

    game.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lichess", help="Play in Lichess", action="store_true")
    parser.add_argument("-t", "--token", help="Lichess bot token")
    args = parser.parse_args()

    run(args)