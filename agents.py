import random


class Agent(object):
  def act(self, board, legal_actions):
    raise NotImplementedError


class RandomAgent(Agent):
  def act(self, board, legal_actions):
    return random.choice(legal_actions)


class HumanAgent(Agent):
  def __init__(self, game_config):
    self.visualise = game_config["visualise"]
    if self.visualise:
      self.board_gui = game_config["board_gui"]

  def act(self, board, legal_actions):
    while True:
      if self.visualise:
        action = self.board_gui.action(board)
      else:
        action = input(f"Play in a column: 0 1 2 3")
        action = int(action) if action.isdigit() else action

      if action in legal_actions:
        return action
