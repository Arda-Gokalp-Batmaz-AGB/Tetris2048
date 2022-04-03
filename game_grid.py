import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import os
from lib.picture import Picture
# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles landed onto the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      self.next_tetromino = None#
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(42, 69, 99)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(0, 100, 200) 
      self.boundary_color = Color(0, 100, 200)
      # thickness values used for the grid lines and the boundaries
      self.line_thickness = 0.002
      self.box_thickness = 10 * self.line_thickness

      self.score = 0
   # Method used for displaying the game grid
   def display(self):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current/active tetromino if it is not None (the case when the 
      # game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # draw a box around the game grid
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      self.ShowNextTetromino()
      self.ShowScore()
      stddraw.show(250)
         
   # Method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value            
      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness/10)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have 
      # tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None
      
   # Method used for checking whether the cell with given row and column indexes 
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid 
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # return the game_over flag
      #print(self.tile_matrix.__str__())
      return self.game_over

   def ClearHorizontal(self):
      #will_cleared_horizontal = self.CheckHorizontal()
      will_cleared_horizontal_rows = self.CheckHorizontal()
      #print(will_cleared_horizontal)
      n_cols = len(self.tile_matrix[0])
      if(len(will_cleared_horizontal_rows) != 0):
         for row in will_cleared_horizontal_rows:
            for col in range(n_cols):
               self.score = self.score + self.tile_matrix[row][col].number
               self.tile_matrix[row][col]=None

         #self.FallTilesInAir()
      else:
         pass

   def CheckHorizontal(self):
      n_rows, n_cols = len(self.tile_matrix), len(self.tile_matrix[0])
      rows_will_cleared = []
      for row in range(n_rows):
         horizontal_count = 0
         for col in range(n_cols):
            if (self.tile_matrix[row][col] != None):
               horizontal_count = horizontal_count + 1
            else:
               break

         if(horizontal_count == n_cols):
            rows_will_cleared.append(row)
      return rows_will_cleared

   def FallTilesInAir(self):
      self.ClearHorizontal()
      pass

   def MergeTiles(self):
      n_rows, n_cols = len(self.tile_matrix), len(self.tile_matrix[0])
      row = 0
      col = 0
      while row < n_rows:
         while col < n_cols:
            current_tile = self.tile_matrix[row][col]
            if current_tile is not None and row + 1 < n_rows:#row + 1 >= 0:
               upper_tile = self.tile_matrix[row+1][col]
               if upper_tile is not None:
                  if current_tile.number == upper_tile.number:# merge
                     #current_tile.number = current_tile.number * 2
                     current_tile.DoubleNumber()
                     self.tile_matrix[row+1][col] = None
                     row = 0
                     col = 0
                     self.score = self.score + current_tile.number
                     continue
            col = col + 1
         row = row + 1
         col = 0

   def CheckIsolateds(self):
      n_rows, n_cols = len(self.tile_matrix), len(self.tile_matrix[0])
      row = 0
      col = 0
      while row < n_rows:
         while col < n_cols:
            current_tile = self.tile_matrix[row][col]
            if current_tile is not None:
               if(row==0):
                  col = col + 1
                  continue
               elif(row + 1 < n_rows and self.tile_matrix[row + 1][col] is not None):#upper neighbour
                  col = col + 1
                  continue
               elif(col + 1 < n_cols and self.tile_matrix[row][col+1] is not None): #right neighbour
                  col = col + 1
                  continue
               elif(row -1 >= 0 and self.tile_matrix[row - 1][col] is not None): #bottom neighbour
                  col = col + 1
                  continue
               elif(col - 1 >=0 and self.tile_matrix[row][col-1] is not None): # left neighbour
                  col = col + 1
                  continue
               else: #It is a isolated tile
                  newrow = row
                  newrow = newrow -1
                  next_location = self.tile_matrix[newrow][col]
                  while next_location == None and newrow - 1 >= 0:
                     if (newrow == 0):
                        break
                     if (newrow + 1 < n_rows and self.tile_matrix[newrow + 1][col] is not None):  # upper neighbour
                        break
                     elif (col + 1 < n_cols and self.tile_matrix[newrow][col + 1] is not None):  # right neighbour
                        break
                     elif (newrow - 1 >= 0 and self.tile_matrix[newrow - 1][col] is not None):  # bottom neighbour
                        break
                     elif (col - 1 >= 0 and self.tile_matrix[newrow][col - 1] is not None):   # left neighbour
                        break
                     newrow = newrow - 1
                  self.tile_matrix[newrow][col] = current_tile
                  self.tile_matrix[row][col] = None
                  row = 0
                  col = 0
            col = col + 1
         row = row + 1
         col = 0
   def ShowNextTetromino(self):
      current_dir = os.path.dirname(os.path.realpath(__file__))
      img_file = current_dir + F"/images/{self.next_tetromino.type}.png"
      # center coordinates to display the image
      img_center_x, img_center_y = (self.grid_width - 1) / 0.75, self.grid_height - 7
      # image is represented using the Picture class
      image_to_display = Picture(img_file)
      stddraw.picture(image_to_display, img_center_x, img_center_y)

   def ShowScore(self):
      stddraw.setFontSize(30)
      stddraw.boldText(self.grid_width * 1.1, self.grid_height / 1.1, f"  Score:   {self.score}")

   def PauseGame(self):
      stddraw.clearKeysTyped()
      #print("Game is paused")
     # stddraw.show(100)
      while True:
         stddraw.setFontSize(60)
         stddraw.boldText(self.grid_width / 2, self.grid_height / 2, "Game Paused")
         if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key

            if key_typed == "space":
               stddraw.show(100)
               print("Game is running")
               break
         stddraw.clearKeysTyped()
         stddraw.show(100)
