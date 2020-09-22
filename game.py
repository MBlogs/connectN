import numpy as np
import time


class Game:
  def __init__(self, game_config):
    self.turn = 0
    self.delay = 0
    self.connect_length = game_config["connect_length"]
    self.agents = game_config["agents"]
    self.board_gui = game_config["board_gui"]
    self.board = -np.ones((game_config["rows"], game_config["cols"]))
    self.visualise = game_config["visualise"]
    self.write_board = game_config["write_board"]
    self.reset()


  def reset(self):
    rows, cols = self.board.shape
    self.turn = 0
    self.board = -np.ones((rows, cols))
    self.board.fill(-1)


  def reset_turn(self, board, turn):
    self.board = board.copy()
    self.turn = turn


  def apply_action(self, action):
    row = row_from_action(self.board, action)
    self.board[row, action] = self.turn
    return self.check_win(row, action)


  def check_win(self, row, col):
    """Check for win after a play on row and col. Returns True if win and None if draw"""
    debug = False

    def win(line):
      count = 0
      if debug: print(f"Line is {line}")
      for counter in line:
        if counter == self.turn:
          count += 1
          if count >= self.connect_length:
            return True
        else:
          count = 0
      return False

    # Return True by checking for connecting runs on the horizontal, vertical, and both diagonals
    rows, cols = self.board.shape
    # Check Draw
    if -1 not in self.board:
      return None
    # Check Win along horizontal, vertical or (both) diagonal axes
    return (win(self.board[row, :])
            or win(self.board[:, col])
            or win(np.diagonal(self.board, offset=col - row))
            or win(np.diagonal(np.fliplr(self.board), offset=cols - (col + row) - 1)))


  def step(self):
    """Returns outcome: int >= 0 for player win. -1 for draw. None for non-terminal"""
    current_agent = self.agents[self.turn]
    legal_actions = get_legal_actions(self.board)
    action = current_agent.act(self.board, legal_actions)
    assert action in legal_actions
    win = self.apply_action(action)

    if self.visualise:
      self.board_gui.update(self.board)
    if self.write_board:
      print_board(self.board)

    if win:
      outcome = self.turn
    elif win is None:
      outcome = -1
    else:
      outcome = None

    self.turn = (self.turn + 1) % 2
    return outcome


def get_legal_actions(board):
  # Return all columns that aren't full
  rows, cols = board.shape
  legal_actions = []
  for col in range(cols):
    if board[rows - 1, col] == -1:
      legal_actions.append(col)
  return legal_actions


def row_from_action(board, action):
  # Action = column to place next counter
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