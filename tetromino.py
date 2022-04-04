from tile import Tile  # used for modeling each tile on the tetromino
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # module for generating random values/permutations
import numpy as np  # the fundamental Python module for scientific computing
from copy import copy, deepcopy
from lib.color import Color
#import lib.stddraw as stddraw
#import time
# Class used for modeling tetrominoes with 3 out of 7 different types/shapes 
# as (I, O and Z)
class Tetromino:
   # The dimensions of the game grid
   grid_height, grid_width = None, None

   # Constructor for creating a tetromino with a given type (shape)
   def __init__(self, type):
      # set the shape of the tetromino based on the given type
      self.type = type
      # determine the occupied (non-empty) tiles in the tile matrix
      occupied_tiles = []
      if type == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial orientation
         occupied_tiles.append((1, 0)) # (column_index, row_index) 
         occupied_tiles.append((1, 1))
         occupied_tiles.append((1, 2))
         occupied_tiles.append((1, 3))
         # occupied_tiles.append((1, 0)) # (column_index, row_index)
         # occupied_tiles.append((1, 1))
         # occupied_tiles.append((1, 2))
         # occupied_tiles.append((1, 3))
      elif type == 'O':
         n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial orientation
         occupied_tiles.append((0, 0)) # (column_index, row_index) 
         occupied_tiles.append((1, 0))
         occupied_tiles.append((0, 1))
         occupied_tiles.append((1, 1)) 
      elif type == 'Z':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         occupied_tiles.append((0, 1)) # (column_index, row_index) 
         occupied_tiles.append((1, 1))
         occupied_tiles.append((1, 2))
         occupied_tiles.append((2, 2))
      elif type == 'S':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         occupied_tiles.append((1, 1)) # (column_index, row_index)
         occupied_tiles.append((2, 1))
         occupied_tiles.append((1, 2))
         occupied_tiles.append((0, 2))
      elif type == 'T':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         occupied_tiles.append((0, 1)) # (column_index, row_index)
         occupied_tiles.append((1, 1))
         occupied_tiles.append((2, 1))
         occupied_tiles.append((1, 2))
      elif type == 'L':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         occupied_tiles.append((0, 1)) # (column_index, row_index)
         occupied_tiles.append((1, 1))
         occupied_tiles.append((2, 1))
         occupied_tiles.append((0, 2))
      elif type == 'J':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         occupied_tiles.append((0, 1)) # (column_index, row_index)
         occupied_tiles.append((1, 1))
         occupied_tiles.append((2, 1))
         occupied_tiles.append((2, 2))
      # create a matrix of numbered tiles based on the shape of the tetromino
      self.tile_matrix = np.full((n, n), None)
      # create the four tiles (minos) of the tetromino and place these tiles
      # into the tile matrix
      for i in range(len(occupied_tiles)):
         col_index, row_index = occupied_tiles[i][0], occupied_tiles[i][1]
         # create the tile at the computed position 
         self.tile_matrix[row_index][col_index] = Tile()
      # initialize the position of the tetromino (the bottom left cell in the 
      # tile matrix) with a random horizontal position above the game grid 
      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = self.grid_height - 1
      self.bottom_left_cell.x = random.randint(0, self.grid_width - n)

   # Method that returns the position of the cell in the tile matrix specified 
   # by the given row and column indexes
   def get_cell_position(self, row, col,type="default"):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      position = Point()
      # horizontal position of the cell
      position.x = self.bottom_left_cell.x + col
      # vertical position of the cell
      if(type=="rotation"):
         position.y = self.bottom_left_cell.y
      else:
         position.y = self.bottom_left_cell.y + (n - 1) - row

      # if(self.bottom_left_cell.y + (n - 1) - row >=20 and type == "rotation"):
      #    print("stop")
      #print(position.y)
      return position

   # Method that returns a copy of tile_matrix omitting empty rows and columns
   # and the position of the bottom left cell when return_position is set
   def get_min_bounded_tile_matrix(self, return_position = False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # determine rows and columns to copy (omit empty rows and columns)
      min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               if row < min_row:
                  min_row = row
               if row > max_row:
                  max_row = row
               if col < min_col:
                  min_col = col
               if col > max_col:
                  max_col = col
      # copy the tiles from the tile matrix and return the resulting copy
      copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
      for row in range(min_row, max_row + 1):
         for col in range(min_col, max_col + 1):
            if self.tile_matrix[row][col] is not None:
               row_ind = row - min_row
               col_ind = col - min_col
               copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
      # return just the resulting copy matrix when return_position is not set
      if not return_position:
         return copy
      # otherwise return the position of the bottom left cell in copy as well
      else:
         blc_position = cp.copy(self.bottom_left_cell)
         blc_position.translate(min_col, (n - 1) - max_row)
         return copy, blc_position
      
   # Method for drawing the tetromino on the game grid
   def draw(self):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw each occupied tile (not equal to None) on the game grid
            if self.tile_matrix[row][col] is not None:
               # get the position of the tile
               position = self.get_cell_position(row, col)
               # draw only the tiles that are inside the game grid
               if position.y < self.grid_height:
                  self.tile_matrix[row][col].draw(position) 

   # Method for moving the tetromino in a given direction by 1 on the game grid
   def move(self, direction, game_grid):
      # check if the tetromino can be moved in the given direction by using the
      # can_be_moved method defined below
      if(direction!="up"):
       if not(self.can_be_moved(direction, game_grid)):
          return False  # the tetromino cannot be moved in the given direction
      # move the tetromino by updating the position of the bottom left cell in 
      # the tile matrix 
      if direction == "left":
         self.bottom_left_cell.x -= 1
      elif direction == "right":
         self.bottom_left_cell.x += 1
      elif direction == "down":
         self.bottom_left_cell.y -= 1
      else:
        #print("tuş basıldı 2")
        self.tile_matrix= self.rotateTetromino(game_grid)
      return True  # successful move in the given direction
   
   # Method to check if the tetromino can be moved in the given direction or not
   def can_be_moved(self, dir, game_grid):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # check for moving left or right
      if dir == "left" or dir == "right":
         for row in range(n):
            for col in range(n): 
               # direction = left --> check the leftmost tile of each row
               if dir == "left" and self.tile_matrix[row][col] is not None:
                  leftmost = self.get_cell_position(row, col)
                  # tetromino cannot go left if any leftmost tile is at x = 0
                  if leftmost.x == 0:
                     return False
                  # skip each row whose leftmost tile is out of the game grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if leftmost.y >= self.grid_height:
                     break
                  # the tetromino cannot go left if the grid cell on the left of 
                  # any leftmost tile is occupied
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                     return False
                  break  # end the inner for loop
               # direction = right --> check the rightmost tile of each row
               elif dir == "right" and self.tile_matrix[row][n-1-col] is not None:
                  rightmost = self.get_cell_position(row, n - 1 - col)
                  # the tetromino cannot go right if any rightmost tile is at
                  # x = grid_width - 1
                  if rightmost.x == self.grid_width - 1:
                     return False
                  # skip each row whose rightmost tile is out of the game grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if rightmost.y >= self.grid_height:
                     break
                  # the tetromino cannot go right if the grid cell on the right 
                  # of any rightmost tile is occupied
                  if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False
                  break  # end the inner for loop
      # direction = down --> check the bottommost tile of each column
      elif dir=="down":
         for col in range(n):
            for row in range(n - 1, -1, -1):
               if self.tile_matrix[row][col] is not None:
                  bottommost = self.get_cell_position(row, col)
                  # skip each column whose bottommost tile is out of the grid
                  # (possible for newly entered tetrominoes to the game grid)
                  if bottommost.y > self.grid_height:
                     break
                  # tetromino cannot go down if any bottommost tile is at y = 0
                  if bottommost.y == 0:
                     return False
                  # or the grid cell below any bottommost tile is occupied
                  if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                     return False
                  break  # end the inner for loop


      elif dir=="up":
         pass
         # rotated_tetromino_matrix = deepcopy(self.tile_matrix)
         # pivot_x = 1
         # pivot_y = 1
         # for col in range(n):
         #    for row in range(n - 1, -1, -1):
         #       current_tile = self.tile_matrix[row][col]
         #       if current_tile is not None:
         #          newcolumn = col - pivot_y
         #          newrow = row - pivot_x
         #
         #          #Swap row-column
         #          temp = newrow
         #          newrow = newcolumn
         #          newcolumn = -1 * temp
         #          # Swap row-column
         #          newrow = newrow + pivot_x
         #          newcolumn = newcolumn + pivot_y
         #          rotated_tetromino_matrix[row][col]=None
         #          rotated_tetromino_matrix[newrow][newcolumn]=current_tile

      return True  # tetromino can be moved in the given direction


   def rotateTetromino(self,game_grid):
      #print("tuş basıldı 3")
      n = len(self.tile_matrix)
      rotated_tetromino_matrix = np.full((n, n), None)
      pivot_x = 1
      pivot_y = 1
      if(n!=4):#n==3
         for col in range(0,n):
            for row in range(0,n):
               current_tile = self.tile_matrix[row][col]
               if current_tile is not None:
                  newcolumn = col - pivot_y
                  newrow = row - pivot_x
                  # Swap row-column (m,n) -> (-n,m)
                  temp = newrow
                  newrow = newcolumn
                  newcolumn = -1 * temp
                  # Swap row-column
                  newrow = newrow + pivot_x
                  if(n==3):
                     newcolumn = newcolumn + pivot_y
                  rotated_tetromino_matrix[newrow][newcolumn] = current_tile

                 #  coord = self.get_cell_position(newrow, newcolumn)
                 # # print(coord)
                 #  if (not game_grid.is_inside(coord.y, coord.x)) or game_grid.tile_matrix[coord.y][coord.x] != None :
                 #     #print("Its out of bound so rotation cancelled")
                 #     return self.tile_matrix

      elif(n==4):
         position = None
         if(self.tile_matrix[0][1] !=None or self.tile_matrix[0][2] !=None):
            position="vertical"
         else:
            position="horizontal"
         for col in range(0,n):
            for row in range(0,n):
               current_tile = self.tile_matrix[row][col]
               if current_tile is not None:
                  newcolumn = col
                  newrow = row
                  # Swap row-column (m,n) -> (n,m)
                  temp = newrow
                  newrow = newcolumn
                  newcolumn = temp
                  # Swap row-column
                  if(position == "horizontal"):
                     if(newcolumn + 1 == 3):
                        newcolumn = newcolumn-1
                     else:
                        newcolumn = newcolumn + 1
                        #newrow = -1 * (newrow - 3)
                  else:
                     newcolumn = -1 * (newcolumn - 3)
                  rotated_tetromino_matrix[newrow][newcolumn] = current_tile

                  # coord = self.get_cell_position(newrow, newcolumn)
                  # #print(coord)
                  # if (not game_grid.is_inside(coord.y, coord.x)) or game_grid.tile_matrix[coord.y][coord.x] != None :
                  #   # print("Its out of bound so rotation cancelled")
                  #    return self.tile_matrix

      rotatable,relocateable = self.CheckRotatedTetromino(rotated_tetromino_matrix,game_grid)
      if (rotatable==False):
          #vnew_relocated_rotated_tetromino =
          if(relocateable == True):
             self.ReLocateTetromino(rotated_tetromino_matrix, game_grid)
             print("Relocated")
             return rotated_tetromino_matrix
          print("Cant rotated")
          return self.tile_matrix

      # if (self.CheckRotatedTetromino(rotated_tetromino_matrix,game_grid)==False):
      #    return self.tile_matrix
      #return self.tile_matrix
      #print(rotated_tetromino_matrix.__str__())
      print("rotated")
      return rotated_tetromino_matrix

   # coord = self.get_cell_position(newrow, newcolumn)
   # print(coord)
   # if not game_grid.is_inside(coord.y, coord.x):
   #    print("Its out of bound so rotation cancelled")
   #    return self.tile_matrix

   def CheckRotatedTetromino(self,rotated_tetromino_matrix,game_grid):
      n = len(self.tile_matrix)
      for col in range(0, n):
         for row in range(0, n):
            current_tile = rotated_tetromino_matrix[row][col]
            if current_tile is not None:
               coord = self.get_cell_position(row, col,"rotation")
               if (not game_grid.is_inside(coord.y, coord.x)) or game_grid.tile_matrix[coord.y][coord.x] != None:

                  if(game_grid.is_inside_horizontal(coord.x) == False and game_grid.is_inside_vertical(coord.y)==True):
                     return False, True
                  elif(game_grid.is_inside_vertical(coord.y) == False):
                     return False,False

                  if(game_grid.tile_matrix[coord.y][coord.x] != None):
                     return False,False

      return True,None

   def ReLocateTetromino(self,rotated_tetromino_matrix,game_grid):
      n = len(self.tile_matrix)
      temp = Point()
      temp.y = self.bottom_left_cell.y
      temp.x = self.bottom_left_cell.x
      if(self.bottom_left_cell.x == -1 and n == 3):
         temp.x = self.bottom_left_cell.x +1
      elif(n == 3):
         temp.x = self.bottom_left_cell.x - 1
      elif(n== 4):
         if (self.bottom_left_cell.x == -1):
            temp.x = self.bottom_left_cell.x + 2
         else:
            temp.x = self.bottom_left_cell.x - 2

      print(f"x={self.bottom_left_cell.x}")
      print(f"y={self.bottom_left_cell.y}")

      # if(self.bottom_left_cell.x == temp.x or self.bottom_left_cell.y < 0 or self.bottom_left_cell.x < 0):
      #    return False,None

      self.bottom_left_cell = temp
      print("Normally Can't Rotate!")

      return rotated_tetromino_matrix

   def MakeTetrominoTransparent(self):
      n = len(self.tile_matrix)
      for col in range(0, n):
         for row in range(0, n):
            current_tile = self.tile_matrix[row][col]
            if current_tile is not None:

               current_tile.background_color = Color(154,146,145)#Color(206,195,181)#Color(42, 69, 99)
               current_tile.foreground_color = Color(104,45,102)#Color(255, 117, 26)
               current_tile.box_color = Color(255, 117, 26)

   # def PauseGame(self):
   #    stddraw.clearKeysTyped()
   #    #print("Game is paused")
   #   # stddraw.show(100)
   #    while True:
   #       stddraw.setFontSize(60)
   #       stddraw.boldText(self.grid_width / 2, self.grid_height / 2, "Game Paused")
   #       if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
   #          key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
   #
   #          if key_typed == "space":
   #             stddraw.show(100)
   #             print("Game is running")
   #             break
   #       stddraw.clearKeysTyped()
   #       stddraw.show(100)


















   #
   # def ReLocateTetromino(self,rotated_tetromino_matrix,game_grid):
   #    n = len(self.tile_matrix)
   #    new_relocated_tetromino_matrix = np.full((n, n), None)
   #    col = 0
   #    row = 0
   #    relocate = False
   #    while col < n:
   #       while row < n:
   #          current_tile = rotated_tetromino_matrix[row][col]
   #          if current_tile is not None:
   #             coord = self.get_cell_position(row, col,"rotation")
   #             print(f"x:{coord.x},y:{coord.y}")
   #             # if(coord.x == game_grid.grid_width):#game_grid.grid_width <= coord.x and
   #             #    print("Boing")
   #             #    if(relocate == False):
   #             #       relocate = True
   #             #       row = 0
   #             #       col = 0
   #             #       continue
   #             #    else:
   #             ##new_relocated_tetromino_matrix[row][col-1] = current_tile
   #             #row = row + 1
   #             #continue
   #
   #             #return False,None
   #          row = row + 1
   #       col = col + 1
   #       row = 0
   #    temp = Point()
   #    temp.x = self.bottom_left_cell.x -1
   #    temp.y = self.bottom_left_cell.y
   #    self.bottom_left_cell = temp
   #    return True,self.tile_matrix

      # def CheckRotatedTetromino(self, rotated_tetromino_matrix, game_grid):
      #    #      print("tuş basıldı 4")
      #    n = len(self.tile_matrix)
      #    locatable_count = 0
      #    tile_count = 0
      #    for col in range(0, n):
      #       for row in range(0, n):
      #          current_tile = rotated_tetromino_matrix[row][col]
      #          if current_tile is not None:
      #             tile_count = tile_count + 1
      #             coord = self.get_cell_position(row, col, "rotation")
      #             if (not game_grid.is_inside(coord.y, coord.x)) or game_grid.tile_matrix[coord.y][coord.x] != None:
      #
      #                if (game_grid.tile_matrix[coord.y][coord.x] != None):
      #                   return False, False
      #
      #                if (game_grid.is_inside_horizontal(coord.x) == False and game_grid.is_inside_vertical(
      #                        coord.y == True)):
      #                   locatable_count = locatable_count + 1
      #                elif (game_grid.is_inside_vertical(coord.y == False)):
      #                   return False, False
      #                # return False
      #
      #    if (locatable_count == tile_count):
      #       return False, True
      #
      #    return True, None




      # def CheckRotatedTetromino(self, rotated_tetromino_matrix, game_grid):
      #    #      print("tuş basıldı 4")
      #    n = len(self.tile_matrix)
      #    for col in range(0, n):
      #       for row in range(0, n):
      #          current_tile = rotated_tetromino_matrix[row][col]
      #          if current_tile is not None:
      #             coord = self.get_cell_position(row, col, "rotation")
      #             if (not game_grid.is_inside(coord.y, coord.x)) or game_grid.tile_matrix[coord.y][coord.x] != None:
      #                # print(f"{coord.x},{coord.y}")
      #                return False
      #       # print(f"{coord.x},{coord.y}")
      #    return True


   #
   # def CheckRotatedTetromino(self,rotated_tetromino_matrix,game_grid):
   #    n = len(self.tile_matrix)
   #    for col in range(0, n):
   #       for row in range(0, n):
   #          current_tile = rotated_tetromino_matrix[row][col]
   #          if current_tile is not None:
   #             coord = self.get_cell_position(row, col,"rotation")
   #             if (not game_grid.is_inside(coord.y, coord.x)) or game_grid.tile_matrix[coord.y][coord.x] != None:
   #
   #                if(game_grid.is_inside_horizontal(coord.x) == False and game_grid.is_inside_vertical(coord.y == True)):
   #                   return False, True
   #                elif(game_grid.is_inside_vertical(coord.y == False)):
   #                   return False,False
   #
   #                if(game_grid.tile_matrix[coord.y][coord.x] != None):
   #                   return False,False
   #
   #    return True,None