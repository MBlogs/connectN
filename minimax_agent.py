from agents import Agent
from game import Game
from game import get_legal_actions
import numpy as np
import random

class MiniMaxAgent(Agent):


  def __init__(self, game_config, my_player, prune=True):
    game_config["visualise"] = False
    game_config["write_board"] = False
    self.game = Game(game_config)
    self.my_player = my_player
    self.prune = prune
    return

  def act(self, board, legal_actions):
    root_state = State(board.copy(), self.my_player, False)
    score, action = self.minimax(self.my_player == 0, root_state, 0)
    return legal_actions[action]

  def minimax(self, isMaxPlayer, state, depth, alpha=float('-inf'), beta=float('inf')):
    # Assumes player 0 is maximising. Returns: score, action.
    if state.is_terminal():
      if state.win is None:
        score = 0  #Draw
      elif state.player == 1:
        score = 1 #Player 0 (Max) won
      else:
        score = -1  #Player 1 (Min) won
      return score, None

    scores = []
    next_states = state.find_next_states(self.game)

    for next_state in next_states:
      score, action = self.minimax(not isMaxPlayer, next_state, depth+1, alpha, beta)

      # Update Alpha-Beta
      if isMaxPlayer and score > max(scores, default=-2):
        alpha = max(alpha, score)
      elif not isMaxPlayer and score < min(scores, default=2):
        beta = min(beta, score)

      # Add new score
      scores.append(score)

      # Alpha Beta Pruning
      if beta <= alpha and self.prune:
        break

    # Return the score and index of max/min score
    if isMaxPlayer:
      return max(scores), scores.index(max(scores))
    else:
      return min(scores), scores.index(min(scores))


class State:
  def __init__(self, board, player, win):
    self.board = board.copy()  # Current board as np array. First row is 'bottom' of the board
    self.player = player  # Player who will perform next move
    self.win = win  # True = Previous player won the game. False = Nonterminal. None = Draw.

  def find_next_states(self, game):
    children = []
    if not self.is_terminal():
      legal_actions = get_legal_actions(self.board)
      for action in legal_actions:
        game.reset_state(self.board, self.player)
        outcome = game.apply_action(action)
        children.append(State(game.board, game.player, outcome))
    return children

  def is_terminal(self):
    return self.win is None or self.win

  def __str__(self):
    rev = np.fliplr(self.board)
    return str(np.flip(rev.flatten()))

  def __repr__(self):
    return str(self)

  def __hash__(self):
    return hash(tuple(map(tuple, self.board)))

  def __eq__(node1, node2):
    return np.array_equal(node1.board, node2.board)
