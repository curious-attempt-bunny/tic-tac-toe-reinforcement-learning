import network
import state
import random
import numpy as np
import sys

class TicTacToe(object):

  def __init__(self):
    self.net = network.Network([9, 20, 10, 1])
    self.table = {}

  def value_of(self, state):
    inputs = self.inputs_for(state)
    value = self.net.feedforward(inputs)[0][0]
    if state.next == 1:
      value = -value # O seeks to minimize the value of X's position
    return value

  def inputs_for(self, state):
    return sum(state.grid, [])

  def train_with(self, training_data):
    np_training_data = []
    for x, y in training_data:
      np_desired = np.zeros((1,1))
      np_desired[0] = y
      np_inputs = np.reshape(x, (len(x), 1))
      np_training_data.append((np_inputs, np_desired))

    self.net.SGD(np_training_data, 1, len(np_training_data), 0.01, lmbda = 5)

  # def value_of(self, state):
  #   key = str(state)
  #   if not(key in self.table):
  #     # if state.next == 1:
  #     #   self.table[key] = -1
  #     # else:
  #     #   self.table[key] = 1
  #     self.table[key] = random.random()
  #   return self.table[key]

  # def inputs_for(self,state):
  #   return str(state)

  # def train_with(self,training_data):
  #   for x,y in training_data:
  #     self.table[x] = y

  def make_best_move(self,state,debug=False):
    moves = state.moves()
    best_move = None
    best_value = None

    for move in moves:
      candidate = state.move(move)
      value = self.value_of(candidate)
      if state.next == -1:
        value = -value # O seeks to minimize the value of X's position

      if debug:
        print "{} is worth {} to {}".format(move, value, state.render(state.next))

      if best_move is None or value > best_value or (value == best_value and random.random() >= 0.5):
        best_move = move
        best_value = value

    if debug:
      print "best was {} with worth {} to {}".format(best_move, best_value, state.render(state.next))

    # s = s.move(random.choice(moves))
    state = state.move(best_move)

    return state

  def play(self):
    s = state.State()
    while not(s.is_end()):
      if s.next == 1:
        print s
        print "Enter your move coordinates mn:"
        move = sys.stdin.readline()
        move = (int(move[0]), int(move[1]))
        if s.grid[move[0]][move[1]] == 0:
          s = s.move(move)
      else:
        s = self.make_best_move(s)

      print s

  def assess(self):
    # X..
    # ..f
    # .f.
    s = state.State().move((0,0))
    s = self.make_best_move(s)
    if s.grid[2][1] == -1 or s.grid[1][2] == -1:
      sys.stdout.write("Fail    ")
    else:
      sys.stdout.write("Success ")
    # X..
    # .Xf
    # .fO
    s = state.State().move((0,0)).move((2,2)).move((1,1))
    s = self.make_best_move(s)
    if s.grid[2][1] == -1 or s.grid[1][2] == -1:
      sys.stdout.write("Fail    ")
    else:
      sys.stdout.write("Success ")
    # XOf
    # fOf
    # X.X
    s = state.State().move((0,0)).move((1,1)).move((2,2)).move((1,0)).move((0,2))
    s = self.make_best_move(s)
    if s.grid[1][2] == 0:
      sys.stdout.write("Fail    ")
    else:
      sys.stdout.write("Success ")
    # X.X
    # fff
    # ffO
    s = state.State().move((0,0)).move((2,2)).move((2,0))
    s = self.make_best_move(s)
    if s.grid[1][0] == 0:
      sys.stdout.write("Fail    ")
    else:
      sys.stdout.write("Success ")
    print


  def iterate(self, iterations=1):
    while iterations > 0:
      # debugIteration = iterations % 1000 == 0
      debugIteration = False
      s = state.State()
      visited = [s]
      while not(s.is_end()):

        debug = False
        # if debugIteration and len(s.moves()) >= 8:
        #   debug = True

        if debug:
          print "Iteration "+str(iterations)+" "+str(s)

        if random.random() < 0.1:
          best_move = random.choice(s.moves())
          s = s.move(best_move)
          visited = []
        else:
          s = self.make_best_move(s,debug=debug)

        visited.insert(0, s)

      #   if iterations % 500 == 0:
      #     print s

      # if iterations % 500 == 0:
      #   print

      if debugIteration:
        print visited[-2]
        print s

      # if iterations % 500 == 0:
      #   print s.summary()

      if s.is_won_by(1):
        reinforcement_signal = 1
      elif s.is_won_by(-1):
        reinforcement_signal = -1
      else:
        reinforcement_signal = 0.5

      blame = 1

      training_data = []

      for s in visited:
        actual = self.value_of(s)
        inputs = self.inputs_for(s)

        desired = blame*reinforcement_signal + (1-blame)*actual
        # desired = actual + 0.1*(0.9*reinforcement_signal - actual)
        # reinforcement_signal = desired

        if debugIteration:
          print "{} --> {} (signal: {}, blame: {}) ".format(actual, desired, reinforcement_signal, blame) + str(s)

        training_data.append([inputs, desired])
        blame = blame * 0.90

      self.train_with(training_data)

      if debugIteration:
        actual = self.value_of(state.State())
        print "start -> {}".format(actual)

      if iterations % 100 == 0:
        self.assess()
      # print iterations

      iterations -= 1

