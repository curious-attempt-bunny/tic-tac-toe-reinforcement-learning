import numpy as np

class State(object):
  def __init__(self):
    self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    self.next = 1

  def __str__(self):
    return "{}\n{}|{}|{}\n------\n{}|{}|{}\n------\n{}|{}|{}\n".format(
      self.summary(), annotation,
      self.render(self.grid[0][0]), self.render(self.grid[1][0]), self.render(self.grid[2][0]),
      self.render(self.grid[0][1]), self.render(self.grid[1][1]), self.render(self.grid[2][1]),
      self.render(self.grid[0][2]), self.render(self.grid[1][2]), self.render(self.grid[2][2]))

  def render(self, value):
    if value == 1:
      return 'X'
    elif value == -1:
      return 'O'
    else:
      return ' '

  def summary(self):
    if self.is_draw():
      return 'Draw'
    elif self.is_won_by(1):
      return 'X won'
    elif self.is_won_by(-1):
      return 'O won'
    elif self.next == 1:
      return 'X to play'
    elif self.next == -1:
      return 'O to play'
    else:
      return '???'

  def moves(self):
    return [(x,y) for x, y in zip([0,0,0,1,1,1,2,2,2], [0,1,2]*3) if self.grid[x][y] == 0]

  def is_end(self):
    return not(self.moves()) or self.is_won_by(1) or self.is_won_by(-1)

  def is_draw(self):
    return not(self.moves()) and not(self.is_won_by(1)) and not(self.is_won_by(-1))

  def is_won_by(self, player):
    if self.grid[0][0] == player and self.grid[1][0] == player and self.grid[2][0] == player:
      return True
    elif self.grid[0][1] == player and self.grid[1][1] == player and self.grid[2][1] == player:
      return True
    elif self.grid[0][2] == player and self.grid[1][2] == player and self.grid[2][2] == player:
      return True
    elif self.grid[0][0] == player and self.grid[0][1] == player and self.grid[0][2] == player:
      return True
    elif self.grid[1][0] == player and self.grid[1][1] == player and self.grid[1][2] == player:
      return True
    elif self.grid[2][0] == player and self.grid[2][1] == player and self.grid[2][2] == player:
      return True
    elif self.grid[0][0] == player and self.grid[1][1] == player and self.grid[2][2] == player:
      return True
    elif self.grid[0][2] == player and self.grid[1][1] == player and self.grid[2][0] == player:
      return True
    else:
      return False

  def move(self, (x,y)):
    s = State()
    s.grid = [row[:] for row in self.grid]
    s.grid[x][y] = self.next
    s.next = -self.next
    return s