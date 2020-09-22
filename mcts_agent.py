import math
from game import Game
from collections import defaultdict
from agents import Agent
from agents import RandomAgent

class MCTSAgent(Agent):
  def __init__(self, mcts_config, game_config):
    # Data structures
    self.children = dict()
    self.Q = defaultdict(int)
    self.N = defaultdict(int)
    # Parameters
    self.agents = mcts_config["agents"]
    self.exploration_weight = 0.2
    # Constraints
    self.max_time_limit = 10000
    self.max_rollout_num = 50
    self.max_simulation_steps = 10
    # Game
    game_config["agents"] = [RandomAgent() for _ in range(2)]
    self.game = Game(game_config)
    self.my_turn = mcts_config["my_turn"]

  def act(self, board, legal_actions):
    rollout_num = 0
    elapsed_time = 0
    self._reset()

    while  rollout_num < self.max_rollout_num and elapsed_time < self.max_time_limit:
      self.game.reset_state(board, self.my_turn)
      path, reward = self._do_rollout()


  def _do_rollout(self):
    path = self._select()
    leaf = path[-1]
    reward = self._simulate(leaf)
    self._backpropagate(path, reward)
    return path, reward


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


  def _uct_select(self, board):
    "Select a child of node, balancing exploration & exploitation"
    # Now select which leaf node of the current fully explored tree to explore nodes for
    log_N_vertex = math.log(self.N[board])
    def uct(n):
      "Upper confidence bound for trees"
      return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
        log_N_vertex / self.N[n]
      )
    selected_child = max(self.children[board], key=uct)
    return selected_child


  def _expand(self, board):
    legal_actions = Game.get_legal_actions(board)
    children = []
    for action in legal_actions:
      new_board = board.copy()
      new_board[Game.row_from_action(new_board, action), action] = self.game.turn
      children.append(new_board)
    self.children[board] = children


  def _simulate(self, board, turn):
    "MB: Returns outcome from simulation (>= 0 for turn win, -1 for draw, None for non-terminal)"
    self.game.reset_turn(board, turn)
    outcome = None
    steps = 0
    while not outcome and steps < self.max_simulation_steps:
      outcome = self.game.step()
      steps += 1
    return outcome


  def _backpropagate(self, path, reward):
    "Send the reward back up to the ancestors of the leaf"
    for board in reversed(path):
      self.N[board] += 1
      self.Q[board] += reward


  def _choose(self, node):
    ''' Choose the final move in game by best average score'''
    def score(n):
      if self.N[n] <= 1:
        return float("-inf")  # avoid rarely seen moves
      return self.Q[n] / self.N[n]  # average reward
    return max(self.children[node], key=score)


  def _reset(self):
    self.children = dict()
    self.Q = defaultdict(int)
    self.N = defaultdict(int)
    self.N[self.root_board] = 0
    self.Q[self.root_board] = 0



