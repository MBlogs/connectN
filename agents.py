import random


class Agent(object):
  def act(self, board, legal_actions):
    raise NotImplementedError


class RandomAgent(Agent):
  def act(self, board, legal_actions):
    # print(f"agents.RandomAgent: board is {board}, legal_actions is {legal_actions}")
    return random.choice(legal_actions)


class HumanAgent(Agent):
  def __init__(self, game_config):
    self.board_gui = game_config["board_gui"]

  def act(self, board, legal_actions):
    while True:
      action = self.board_gui.action(board)
      if action in legal_actions:
        return action
