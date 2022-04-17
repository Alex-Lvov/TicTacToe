from tictactoe import FIELD_X as X, FIELD_O as O
from tictactoe import Board, Player, GameOverException, CantRedefineFieldException


b = Board()

px = Player(X)
px.assign_board(b)
po = Player(O)
po.assign_board(b)

# AUTO_PLAY = False
AUTO_PLAY = True

try:
  for move in range(5):
    px.move()
    b.draw()
    if AUTO_PLAY:
      po.move()
    else:
      a = True
      while a:
        try:
          pos = [int(x) for x in input("You move (row col): ").split()]
          po.move(pos[0], pos[1])
          a = False
        except CantRedefineFieldException:
          print("You can not move to this field. Try again!")
except GameOverException:
  print(b)
  print("Game over!")


