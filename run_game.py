from game import Game
from board_gui import BoardGUI
from agents import RandomAgent
from agents import HumanAgent
from mcts_agent import MCTSAgent
import numpy as np


if __name__ == "__main__":
  #  Test update
  game_config = {}
  mcts_config = {}
  game_config["rows"] = 6
  game_config["cols"] = 7
  game_config["connect_length"] = 4
  game_config["board_gui"] = BoardGUI(game_config["rows"], game_config["cols"])
  game_config["board"] = -np.ones((game_config["rows"], game_config["cols"]))
  game_config["visualise"] = True
  game_config["write_board"] = True

  mcts_config["my_turn"] = 0
  mcts_config["agents"] = [RandomAgent(), RandomAgent()]

  # game_config["agents"] = [MCTSAgent(mcts_config, game_config), RandomAgent()]
  game_config["agents"] = [RandomAgent(), RandomAgent()]
  game_config["agents"] = [HumanAgent(game_config["board_gui"]), RandomAgent()]
  game = Game(game_config)

  running = True

  while running:
    outcome = game.run()

    if outcome == -1:
      print("Draw!")
    else:
      print(f"Player {outcome} wins!")


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


