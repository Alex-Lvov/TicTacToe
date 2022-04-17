BOARD_SIZE = 3

# FIELDS_VALUES
FIELD_EMPTY = 0
FIELD_X = 1
FIELD_O = 2

class GameOverException(Exception):
  pass

class CantMoveException(GameOverException):
  pass


class CantRedefineFieldException(Exception):
  pass

class BoardSizeException(Exception):
  pass

class FieldValueException(Exception):
  pass

class PlayerTypeException(FieldValueException):
  pass


class Board:
  def __init__(self, size=BOARD_SIZE):
    self.size = size
    self.fields = self.init_board()

  def init_board(self):
    fields = [[FIELD_EMPTY] * self.size for i in range(self.size)]
    return fields

  def get_field(self, row, col):
    if col >= self.size or row >= self.size:
      raise BoardSizeException()
    return self.fields[row][col]

  def set_field(self, row, col, value=FIELD_EMPTY):
    if col >= self.size or row >= self.size:
      raise BoardSizeException()
    if value not in (FIELD_EMPTY, FIELD_X, FIELD_O):
      raise FieldValueException
    if not self.is_field_empty(row, col):
      raise CantRedefineFieldException
    self.fields[row][col] = value
    self.chk_game_over()
    return self.fields[row][col]
    
  def cmp_fields(self, field1, field2):
    row1, col1 = field1
    row2, col2 = field2
    return True if self.get_field(row1, col1) == self.get_field(row2, col2) else False

  def is_fields_eq(self, field1, field2, chk_for=FIELD_EMPTY):
    if chk_for not in (FIELD_EMPTY, FIELD_X, FIELD_O):
      raise FieldValueException
    return self.cmp_fields(field1, field2) and self.get_field(field1[0], field1[1]) == chk_for

  def is_field_empty(self, row, col):
    return True if self.get_field(row, col) == FIELD_EMPTY else False

  def chk_game_over(self):
    for row in self.fields:
      self.chk_three_in_row(row)

    line = []
    for i in range(self.size):
      for j in range(self.size):
        line.append(self.get_field(j, i))
      self.chk_three_in_row(line)
   
    diagonals = (
      ((0,0), (1,1), (2,2)),
      ((0,2), (1,1), (2,0)),
    )
    for d in diagonals:
      line = []
      for f in d:
        line.append(self.get_field(f[0], f[1]))
      self.chk_three_in_row(line)
    return False

  def chk_three_in_row(self, row):
      if all(x == row[0] and x != FIELD_EMPTY for x in row):
        raise GameOverException()
      return False

  def __str__(self):
    ret = ""
    for row in self.fields:
      for col in row:
        ret += str(col)
      ret += "\n"
    ret += "\n"
    return ret

  def draw(self):
    print(self)
    

class Player:

  def __init__(self, play_as=FIELD_X):
    self.type = play_as
    self.oppotype = FIELD_O if play_as == FIELD_X else FIELD_X

  def assign_board(self, board):
    self.board = board

  @property
  def type(self):
    return self._play_as
    
  @type.setter
  def type(self, play_as=FIELD_X):
    if play_as not in (FIELD_X, FIELD_O):
      raise PlayerTypeException
    self._play_as = play_as

  def chk_two_in_row(self, chk_for=None):
    if chk_for is None:
      chk_for = self.type
    ret = (None, None)

    # check all rows
    for row in range(BOARD_SIZE):
      if self.board.is_fields_eq((row,0), (row,1), chk_for) and self.board.is_field_empty(row, 2):
        ret = (row, 2)
        return ret
      if self.board.is_fields_eq((row,1), (row,2), chk_for) and self.board.is_field_empty(row, 0):
        ret = (row, 0)
        return ret
      if self.board.is_fields_eq((row,0), (row,2), chk_for) and self.board.is_field_empty(row, 1):
        ret = (row, 1)
        return ret

    # check all columns
    for col in range(BOARD_SIZE):
      if self.board.is_fields_eq((0, col), (1, col), chk_for) and self.board.is_field_empty(2, col):
        ret = (2, col)
        return ret
      if self.board.is_fields_eq((1, col), (2, col), chk_for) and self.board.is_field_empty(0, col):
        ret = (0, col)
        return ret
      if self.board.is_fields_eq((0, col), (2, col), chk_for) and self.board.is_field_empty(1, col):
        ret = (1, col)
        return ret

    # check diagonals
    if self.board.is_fields_eq((0, 0), (1, 1), chk_for) and self.board.is_field_empty(2, 2):
      ret = (2, 2)
      return ret
    if self.board.is_fields_eq((1, 1), (2, 2), chk_for) and self.board.is_field_empty(0, 0):
      ret = (0,0)
      return ret
    if self.board.is_fields_eq((0, 0), (2, 2), chk_for) and self.board.is_field_empty(1, 1):
      ret = (1,1)
      return ret

    if self.board.is_fields_eq((0, 2), (1, 1), chk_for) and self.board.is_field_empty(2, 0):
      ret = (2, 0)
      return ret
    if self.board.is_fields_eq((1, 1), (2, 0), chk_for) and self.board.is_field_empty(0, 2):
      ret = (0,2)
      return ret
    if self.board.is_fields_eq((0, 2), (2, 0), chk_for) and self.board.is_field_empty(1, 1):
      ret = (1,1)
      return ret

    return ret

  def move(self, row=None, col=None):

    if row != None and col != None:
      if self.board.is_field_empty(row, col):
        self.board.set_field(row, col, self.type)
        return (row,col)
      else:
        raise CantRedefineFieldException

    # print('Chck win')
    row, col = self.chk_two_in_row(self.type)
    if row != None and col != None:
      # print(row, col, self.board.get_field(row, col))
      self.board.set_field(row, col, self.type)
      return (row,col)

    # print('Chck oppo')
    row, col = self.chk_two_in_row(self.oppotype)
    # print(row, col)
    if row != None and col != None:
      self.board.set_field(row, col, self.type)
      return (row,col)

    # print('Free move')
    free_move = (
      (1,1),
      (0,0), (0,2), (2,2), (2,0),
      (0,1), (1,2), (1,0), (2,1),
    )

    for row, col in free_move:
      if self.board.is_field_empty(row, col):
        self.board.set_field(row, col, self.type)
        return (row, col)

    raise CantMoveException


