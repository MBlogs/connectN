import random


class Agent(object):
  def act(self, board, legal_actions):
    raise NotImplementedError


class RandomAgent(Agent):
  def act(self, board, legal_actions):
    return random.choice(legal_actions)


class HumanAgent(Agent):
  def __init__(self, board_gui):
    self.board_gui = board_gui

  def act(self, board, legal_actions):
    while True:
      action = self.board_gui.action(board)
      if action in legal_actions:
        return action
