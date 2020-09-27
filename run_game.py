from game import Game
from board_gui import BoardGUI
from agents import RandomAgent
from agents import HumanAgent
from mcts_agent import MCTSAgent
from minimax_agent import MiniMaxAgent
import numpy as np


if __name__ == "__main__":
  game_config = {}
  mcts_config = {}
  game_config["rows"] = 4
  game_config["cols"] = 4
  game_config["delay"] = 0.5
  game_config["connect_length"] = 3
  game_config["board_gui"] = BoardGUI(game_config["rows"], game_config["cols"])
  game_config["board"] = -np.ones((game_config["rows"], game_config["cols"]))
  game_config["visualise"] = True
  game_config["write_board"] = True
  game_config["agents"] = [RandomAgent(), RandomAgent()]
  game_config["agents"] = [MiniMaxAgent(game_config.copy(), 0), HumanAgent(game_config.copy())]
  game_config["agents"] = [MiniMaxAgent(game_config.copy(), 0), MiniMaxAgent(game_config.copy(), 1)]
  game_config["agents"] = [HumanAgent(game_config.copy()), MiniMaxAgent(game_config.copy(), 1)]
  game_config["agents"] = [MiniMaxAgent(game_config.copy(), 1), HumanAgent(game_config.copy())]
  game = Game(game_config)
  running = True

  while running:
    game_result = game.run()

    if game_result is None:
      print("Draw!")
    else:
      print(f"Player {game_result} wins!")

    if game_config["visualise"]:
      choice = game_config["board_gui"].end_game()
    else:
      while True:
        choice = input("Play again? [y/n]")
        if choice.lower() == "y":
          choice = True
          break
        if choice.lower() == "n":
          choice = False
          break
    if not choice:
      running = False


