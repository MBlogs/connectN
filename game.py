import numpy as np
import time


class Game:
  def __init__(self, game_config):
    self.player = 0
    self.delay = game_config["delay"]
    self.connect_length = game_config["connect_length"]
    self.agents = game_config["agents"]
    self.board_gui = game_config["board_gui"]
    self.board = -np.ones((game_config["rows"], game_config["cols"]))
    self.visualise = game_config["visualise"]
    self.write_board = game_config["write_board"]
    self.reset()


  def reset(self):
    rows, cols = self.board.shape
    self.player = 0
    self.board = -np.ones((rows, cols))
    self.board.fill(-1)


  def reset_state(self, board, turn):
    self.board = board.copy()
    self.player = turn


  def show(self):
    if self.visualise:
      self.board_gui.update(self.board)
    if self.write_board:
      print_board(self.board)

  def player_pos(self, increment):
    """Return position of a player relative to current player"""
    return (self.player + increment) % len(self.agents)


  def check_win(self, row, col):
    """Check for win after a play on row and col. Returns True if win, False if non-terminal and None if draw"""
    def win(line):
      count = 0
      for counter in line:
        if counter == self.player:
          count += 1
          if count >= self.connect_length:
            return True
        else:
          count = 0
      return False

    rows, cols = self.board.shape
    # Check Win along horizontal, vertical or (both) diagonal axes
    win = (win(self.board[row, :])
            or win(self.board[:, col])
            or win(np.diagonal(self.board, offset=col - row))
            or win(np.diagonal(np.fliplr(self.board), offset=cols - (col + row) - 1)))
    # Check for draw
    if not win and -1 not in self.board:
      return None
    else:
      return win


  def step(self):
    # Steps game based on next agent
    current_agent = self.agents[self.player]
    legal_actions = get_legal_actions(self.board)
    action = current_agent.act(self.board, legal_actions)
    outcome = self.apply_action(action)
    time.sleep(self.delay)
    return outcome


  def apply_action(self, action):
    """Returns outcome: int >= 0 for player win. -1 for draw. None for non-terminal"""
    legal_actions = get_legal_actions(self.board)
    assert action in legal_actions
    row = row_from_action(self.board, action) # Find the row that the counter will fall to
    self.board[row, action] = self.player # Update the board
    win = self.check_win(row, action) # Check if counter position forms a win
    self.player = (self.player + 1) % 2
    self.show()
    return win

  def run(self):
    self.reset()
    self.show()
    while True:
      outcome = self.step()
      if outcome is True:
        return self.player_pos(-1)
      elif outcome is None:
        return None


def infer_action(new_board, old_board):
  """Takes two boards. Returns first column where there is a difference"""
  # Check for differences in the boards
  rows, cols = new_board.shape
  for col in range(cols):
    for row in range(rows):
      if new_board[row, col] != old_board[row, col]:
        return col
      if old_board[row, col] == -1:
        break
  return None


def reward(outcome, turn):
  """Outcome is who won. Reward is what that outcome means for a particular player"""
  if outcome is None or outcome == -1:
    # Outcome is non-terminal or draw
    return 0
  elif outcome >= 0:
    # Someone has won
    if turn == outcome:
      return 1
    else:
      return -1
  else:
    raise Exception("Outcome is not None (non-terminal), -1 (Draw), >= 0 (Winner)")


def get_legal_actions(board):
  """Returns all column indexes that aren't full"""
  rows, cols = board.shape
  legal_actions = []
  for col in range(cols):
    if board[rows - 1, col] == -1:
      legal_actions.append(col)
  return legal_actions


def row_from_action(board, action):
  """Takes board and action (= column to place next counter). Returns the row that the counter will fall to."""
  rows, cols = board.shape
  for row in range(rows):
    if board[row, action] == -1:
      return row
  return None


def print_board(board):
  rows, cols = board.shape
  for row in range(rows-1, -1, -1):
    for col in range(cols):
      if board[row, col] == 0:
        print("0", end=" ")
      elif board[row, col] == 1:
        print("1", end=" ")
      else:
        print("x", end=" ")
    print()
  print("- "*cols)