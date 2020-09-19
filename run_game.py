from game import Game
from board_gui import BoardGUI
from agents import RandomAgent
from agents import HumanAgent


if __name__ == "__main__":
  rows = 7
  cols = 9
  connect_length = 4
  visualise = True
  board_gui = BoardGUI(rows, cols)
  # agents = [HumanAgent(board_gui), HumanAgent(board_gui)]
  agents = [RandomAgent(board_gui), RandomAgent(board_gui)]
  game = Game(rows, cols, connect_length, agents, board_gui, visualise)
  running = True

  while running:
    game.run()
    if visualise:
      choice = board_gui.end_game()
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


