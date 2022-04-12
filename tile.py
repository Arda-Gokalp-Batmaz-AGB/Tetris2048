import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
import random # used for creating tetrominoes with random types/shapes
# Class used for modeling numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self):
      # set the number on the tile
      tetromino_types = [2, 4]
      color_types = [Color(255, 204, 102),Color(255, 153, 0)]
      random_index = random.randint(0, len(tetromino_types) - 1)
      self.number = tetromino_types[random_index]
      # set the colors of the tile
      self.background_color = color_types[random_index] # background (tile) color
      self.foreground_color = Color(0, 100, 200) # foreground (number) color
      self.box_color = Color(132,122,113)#Color(0, 100, 200) # box (boundary) color

   # Method for drawing the tile
   def draw(self, position, length = 1):
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))

   # Doubles the number and changes the color of a tile
   def DoubleNumber(self):
      self.number = self.number * 2
      number_list = [2,4,8,16,32,64,128,256,512,1024,2048,4096,8192]
      index=number_list.index(self.number)
      color_list = [Color(255, 204, 102),Color(255, 153, 0),Color(255, 128, 0),Color(230, 115, 0),Color(204, 102, 0),Color(102, 51, 0),Color(230, 230, 0),Color(255, 102, 0),Color(255, 140, 102),Color(255, 83, 26),Color(204, 51, 0),Color(102, 26, 0),Color(26, 6, 0)]
      self.background_color = color_list[index]

   def __str__(self):
      return str(self.number)

   def __repr__(self):
      return str(self.number)
