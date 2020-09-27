import math
import random
import numpy as np
from game import Game
from game import get_legal_actions
from game import reward
from game import print_board
from game import infer_action
from collections import defaultdict
from agents import Agent
from agents import RandomAgent


class Node:
  """
  A representation of a single board state.
  MCTS works by constructing a tree of these Nodes.
  """
  def __init__(self, board, turn, terminal, outcome):
    self.board = board.copy() # Board is the board after the action was made
    self.turn = turn # Turn is turn of person about to take action
    self.terminal = terminal
    self.outcome = outcome # >=0 is a Win, -1 is Draw, None is Non-terminal

  def find_children(self, game):
    children = []
    if self.terminal == False:
      legal_actions = get_legal_actions(self.board)
      for action in legal_actions:
        game.reset_turn(self.board, self.turn)

        outcome = game.apply_action(action)
        if outcome is None:
          terminal = False
        else:
          terminal = True

        children.append(Node(game.board, game.turn, terminal, outcome))
    return children

  def find_random_child(self, game):
    return random.choice(self.find_children(game))

  def is_terminal(self):
    return self.terminal

  def __str__(self):
    rev = np.fliplr(self.board)
    return str(np.flip(rev.flatten()))

  def __repr__(self):
    return str(self)

  def __hash__(self):
    return hash(tuple(map(tuple, self.board)))

  def __eq__(node1, node2):
    return np.array_equal(node1.board, node2.board)

class MCTSAgent(Agent):
  # ToDo: Minimax agent will break this one
  def __init__(self, game_config, mcts_config):
    # Data structures. Dictionary keys are board_id, hashable representation of board
    self.children = dict()
    self.Q = defaultdict(int)
    self.N = defaultdict(int)
    # Parameters
    self.exploration_weight = 0.2
    # Constraints
    self.max_rollout_num = 100
    self.max_simulation_steps = 5
    # Game
    game_config = game_config.copy()
    game_config["agents"] = mcts_config["agents"]
    game_config["visualise"] = False
    game_config["write_board"] = False
    self.game = Game(game_config)
    self.my_turn = mcts_config["my_turn"]


  def act(self, board, legal_actions):
    rollout_num = 0
    self._reset_tree(board)
    root_node = Node(board, self.my_turn, False, 0)

    while rollout_num < self.max_rollout_num:
      # print(f"----- ROLLOUT {rollout_num} -----")
      self.do_rollout(root_node)
      rollout_num += 1

    print(f"Tree string {self.tree_string()}")
    chosen_node = self.choose(root_node)
    print(f"Chosen node {chosen_node}")
    chosen_action = infer_action(chosen_node.board, board)
    return chosen_action


  def choose(self, node):
    "Choose the best successor of node. (Choose a move in the game)"
    if node.is_terminal():
      raise RuntimeError(f"choose called on terminal node {node}")
    if node not in self.children:
      return node.find_random_child()
    def score(n):
      if self.N[n] == 0:
        return float("-inf")  # avoid unseen moves
      return self.Q[n] / self.N[n]  # average reward
    return max(self.children[node], key=score)


  def do_rollout(self, node):
    "Make the tree one layer better. (Train for one iteration.)"
    path = self._select(node)
    leaf = path[-1]
    self._expand(leaf)
    reward = self._simulate(leaf)
    self._backpropagate(path, reward)


  def _select(self, node):
    "Find an unexplored descendent of `node`"
    path = []
    while True:
      path.append(node)
      if node not in self.children or not self.children[node]:
        # node is either unexplored or terminal
        return path
      unexplored = self.children[node] - self.children.keys()
      if unexplored:
        n = unexplored.pop()
        path.append(n)
        return path
      node = self._uct_select(node)  # descend a layer deeper


  def _expand(self, node):
    "Update the `children` dict with the children of `node`"
    if node in self.children:
      return  # already expanded
    self.children[node] = node.find_children(self.game)


  def _simulate(self, node):
    "Returns the reward for a random simulation (to completion) of `node`"
    if node.is_terminal():
      return reward(node.outcome, self.my_turn)

    self.game.reset_turn(node.board, node.turn)

    outcome = None
    steps = 0
    while outcome is None and steps < self.max_simulation_steps:
      outcome = self.game.step()
      steps += 1

    return reward(outcome, self.my_turn)


  def _backpropagate(self, path, reward):
    "Send the reward back up to the ancestors of the leaf"
    for node in reversed(path):
      self.N[node] += 1
      self.Q[node] += reward


  def _uct_select(self, node):
    "Select a child of node, balancing exploration & exploitation"
    # All children of node should already be expanded:
    assert all(n in self.children for n in self.children[node])

    log_N_vertex = math.log(self.N[node])

    def uct(n):
      "Upper confidence bound for trees"
      return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
        log_N_vertex / self.N[n]
      )

    return max(self.children[node], key=uct)


  def _reset_tree(self, root_board):
    self.children = dict()
    self.Q = defaultdict(int)
    self.N = defaultdict(int)

  def tree_string(self):
    tree_string = ""
    for node, children in self.children.items():
      tree_string += f"[{node}: {self.N[node]}, {self.Q[node]/self.N[node]}] "
    return tree_string



