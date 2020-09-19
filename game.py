import numpy as np
import time

def check_win(connect_length, board, turn, row, col):
  """Check for win after a play on row and col. Returns True if win and None if draw"""
  debug = True
  def win(line):
    count = 0
    if debug: print(f"Line is {line}")
    for counter in line:
      if counter == turn:
        count += 1
        if count >= connect_length:
          return True
      else:
        count = 0
    return False
  # Return True by checking for connecting runs on the horizontal, vertical, and both diagonals
  rows, cols = board.shape
  if debug: print(f"Move: ({row}, {col})")
  # Check Draw
  if not -1 in board:
    return None
  # Return Check Win along horizontal, vertical or diagonal axes
  return (win(board[row, :])
          or win(board[:, col])
          or win(np.diagonal(board, offset=col - row))
          or win(np.diagonal(np.fliplr(board), offset=cols - (col + row) - 1)))


def get_legal_actions(board):
  rows, cols = board.shape
  legal_actions = []
  for col in range(cols):
    if board[rows - 1, col] == -1:
      legal_actions.append(col)
  return legal_actions


def row_from_action(board, action):
  "Takes board and action (column number) to put in"
  rows, cols = board.shape
  for row in range(rows):
    if board[row, action] == -1:
      return row
  return None


class Game:
  def __init__(self, rows, cols, connect_length, agents, board_gui, visualise):
    self.connect_length = connect_length
    self.agents = agents
    self.board_gui = board_gui
    self.board = -np.ones((rows, cols))
    self.turn = 0
    self.visualise = visualise
    self.reset()


  def reset(self):
    rows, cols = self.board.shape
    self.turn = 0
    self.board = -np.ones((rows, cols))
    self.board.fill(-1)


  def apply_action(self, action):
    row = row_from_action(self.board, action)
    self.board[row, action] = self.turn
    return check_win(self.connect_length, self.board, self.turn, row, action)


  def print_board(self, board):
    rows, cols = self.board.shape
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


  def run(self):
    self.reset()
    if self.visualise:
      self.board_gui.update(self.board)
      self.print_board(self.board)
    # Stepping through the game
    while True:
      legal_actions = get_legal_actions(self.board)
      current_agent = self.agents[self.turn]
      action = current_agent.act(self.board, legal_actions)
      assert action in legal_actions
      outcome = self.apply_action(action)

      if self.visualise:
        self.print_board(self.board)
        self.board_gui.update(self.board)

      if outcome:
        print(f"Player: {self.turn} wins!")
        return self.turn
      elif outcome is None:
        print(f"It's a draw!")
        return None

      self.turn = (self.turn + 1) % 2
      time.sleep(0.5)
