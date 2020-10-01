from game import Game
from board_gui import BoardGUI
from agents import RandomAgent
from agents import HumanAgent
from minimax_agent import MiniMaxAgent
import numpy as np


if __name__ == "__main__":
  # 3 - 2x3: Draw
  # 3 - 3x2: Draw
  # 3 - 3x3: Draw
  # 3 - 3x4: Red
  # 3 - 4x3: Draw
  # 3 - 4x4: Red
  # 3 - 4x5: Red

  # 4 - 3x4: Draw
  # 4 - 4x3: Draw
  # 4 - 4x4: Draw
  # 4 - 4x5: Draw
  # 4 - 5x4: Draw
  game_config = {}
  game_config["rows"] = 3
  game_config["cols"] = 3
  game_config["connect_length"] = 3
  game_config["board"] = -np.ones((game_config["rows"], game_config["cols"]))
  game_config["visualise"] = True
  game_config["write_board"] = True
  if game_config["visualise"]:
    game_config["board_gui"] = BoardGUI(game_config["rows"], game_config["cols"])

  game_config["agents"] = [RandomAgent(), RandomAgent()]
  #game_config["agents"] = [MiniMaxAgent(game_config.copy(), 0), HumanAgent(game_config.copy())]
  #game_config["agents"] = [HumanAgent(game_config.copy()), MiniMaxAgent(game_config.copy(), 1)]
  #game_config["agents"] = [MiniMaxAgent(game_config.copy(), 0), MiniMaxAgent(game_config.copy(), 1)]
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


