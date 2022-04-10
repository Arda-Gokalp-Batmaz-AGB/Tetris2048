import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes
import time
from SoundCaller import SoundCaller
from SoundCaller import SoundGlobal
import RecordSaver
# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution

def CreateCanvas():
   grid_h, grid_w = 19, 14#20, 12
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h, 40 * grid_w#40
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, grid_w - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)
   start(grid_h, grid_w)
   return grid_h,grid_w

def start(grid_h, grid_w, Restart = False, diffspeed = None):
   highest_score,highest_time = RecordSaver.ReadRecords()

   # set the dimensions of the game grid
   # grid_h, grid_w = 20, 14#20, 12
   # # set the size of the drawing canvas
   # canvas_h, canvas_w = 40 * grid_h, 40 * grid_w#40
   # stddraw.setCanvasSize(canvas_w, canvas_h)
   # # set the scale of the coordinate system
   # stddraw.setXscale(-0.5, grid_w - 0.5)
   # stddraw.setYscale(-0.5, grid_h - 0.5)
   #grid_h, grid_w = CreateCanvas()
   if(Restart == False):
      display_game_menu(grid_h, grid_w,highest_score,highest_time)
   stddraw.clearKeysTyped()
     # must be smaller than 6
   old_grid_w = grid_w
   grid_w = 10
   # set the dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w

   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino(grid_h, grid_w)
   #next_tetromino = create_tetromino(grid_h, grid_w)
   NEXT_TETROMINO_COUNT = 3
   #next_tetrominos = [create_tetromino(grid_h, grid_w),create_tetromino(grid_h, grid_w),create_tetromino(grid_h, grid_w)]
   next_tetrominos = []
   for i in range(0,NEXT_TETROMINO_COUNT):
      next_tetrominos.append(create_tetromino(grid_h, grid_w))
   #print(f"Next: {next_tetromino.type}")
   grid.current_tetromino = current_tetromino
   #grid.next_tetromino = next_tetromino#
   grid.next_tetrominos = next_tetrominos  #
   #grid.ShowNextTetromino()

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   #display_game_menu(grid_h, grid_w)
   if(Restart == False):
      #HowtoPlayMenu(grid_h, old_grid_w, Color(154,146,145))
      speed = ChooseDifficulity(grid_h, old_grid_w, Color(154,146,145))#Color(42, 69, 99)
   else:
      speed = diffspeed
   movetimer = 6 - speed # Negative speed
   startingtime = time.time()
   PlayTime = time.time()
   # the main game loop (keyboard interaction for moving the tetromino) 
   while True:
      global background_sound_time
      if (time.time()-background_sound_time >= 205):
         SoundCaller('sounds/theme1.wav')
         background_sound_time = time.time()
         print("Background sound restarted")
      # check user interactions via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid) 
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one 
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         elif key_typed == "up":
           #print("Tuş basıldı")
            current_tetromino.move(key_typed, grid)
         elif key_typed == "space":
            grid.PauseGame()
         elif key_typed == "escape":
            StopMenu(grid,grid_h,old_grid_w,speed)
         elif key_typed == "x":
            grid.DropCurrentTetromino()
         elif key_typed == "m":
            SoundGlobal.allow_sound = not SoundGlobal.allow_sound
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      if time.time() - startingtime > movetimer:
         success = current_tetromino.move("down", grid)
         startingtime = time.time()
      else:
         success = True # success = current_tetromino.move("down", grid)

      # place the active tetromino on the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            break
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         #current_tetromino = next_tetromino #         current_tetromino = create_tetromino(grid_h, grid_w)
         current_tetromino = next_tetrominos.pop(0)
         grid.current_tetromino = current_tetromino
         #next_tetromino = create_tetromino(grid_h, grid_w)#
         next_tetrominos.append(create_tetromino(grid_h, grid_w))
         #print(f"Next: {next_tetromino.type}")
         #grid.next_tetromino = next_tetromino
         grid.next_tetrominos = next_tetrominos
         #Sound("sounds/BlockPlace.mp3").CallSound()
         # grid.MergeTiles()
         # grid.CheckIsolateds()
         # grid.ClearHorizontal()
         print(grid.score)
         #playsound('sounds/bp.mp3')
         SoundCaller('sounds/bp.mp3')

      # display the game grid and the current tetromino
      grid.MergeTiles()
      grid.CheckIsolateds()
      grid.ClearHorizontal()
      grid.CalculateTime(PlayTime)
      grid.display()
   # print a message on the console when the game is over
   UpdateRecords(grid,highest_score,highest_time,grid_h,old_grid_w)
   current_dir = os.path.dirname(os.path.realpath(__file__))
   stddraw.picture(Picture(current_dir + "/images/gameovertext.png"), old_grid_w / 2, grid_h / 2)
   SoundCaller('sounds/gameover.wav')
   # print("Game over")
   # stddraw.setFontSize(60)
   # stddraw.boldText(old_grid_w / 2, grid_h / 2, "GAME OVER")
   stddraw.show(100)
   time.sleep(5)
   start(grid_h,old_grid_w)#

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'I', 'O', 'Z','S','T','L','J' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_h, grid_w,highest_score,highest_time):
   # colors used for the menu
   background_color =  Color(154,146,145)#Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_w - 1) / 2, grid_h - 5 #grid_h - 8
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_w - 6, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   stddraw.picture(Picture(current_dir + "/images/guideline_2.png"), button_w/2+2.5, button_h*1.4)
   # display the start game button as a filled rectangle
   # stddraw.setPenColor(button_color)
   # stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   #stddraw.filledRectangle(img_center_x, img_center_y-5, button_w, button_h)
   # display the text on the start game button

   button_file = current_dir + "/images/button.png"
   button_image = Picture(button_file)
   stddraw.picture(button_image, img_center_x, img_center_y-4)# img_center_x, img_center_y-7

   text_file = current_dir + "/images/starttext.png"
   text_image = Picture(text_file)
   stddraw.picture(text_image, img_center_x, img_center_y-4)#-5

   stddraw.picture(Picture(current_dir + "/images/bestscoretext.png"), img_center_x-1, img_center_y - 6.5)
   stddraw.setFontSize(26)
   stddraw.setPenColor(Color(0, 100, 200))
   stddraw.boldText(img_center_x+2, img_center_y - 6.5, f"{highest_score}")  # {self.score}x+2
   stddraw.picture(Picture(current_dir + "/images/besttimetext.png"), img_center_x-1, img_center_y - 7.5)
   stddraw.boldText(img_center_x+2, img_center_y - 7.5, f"{highest_time:.0f}")  # {self.score}

   stddraw.setPenColor(Color(77,77,77))
   stddraw.rectangle(0.6, img_center_y - 13.7, button_w*2-4, button_h*2.7)
   #stddraw.rectangle(0.6, img_center_y - 8.2, button_w*2-4, button_h*6)

   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has 
         # most recently been left-clicked  
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= img_center_y-5 and mouse_y <= img_center_y-5 + button_h:
               break # break the loop to end the method and start the game

def ChooseDifficulity(grid_h,grid_w,backcolor):
   stddraw.clear(backcolor)
   stddraw.clearKeysTyped()
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   img_center_x, img_center_y = (grid_w - 1) / 2, grid_h - 6
   button_w, button_h = grid_w - 6, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   # stddraw.setPenColor(button_color)
   # stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # stddraw.filledRectangle(button_blc_x, button_blc_y + 4, button_w, button_h)
   # stddraw.filledRectangle(button_blc_x, button_blc_y + 8, button_w, button_h)

   current_dir = os.path.dirname(os.path.realpath(__file__))
   button_file = current_dir + "/images/button.png"
   button_image = Picture(button_file)

   stddraw.picture(button_image, img_center_x, img_center_y)
   stddraw.picture(button_image, img_center_x, img_center_y-4)
   stddraw.picture(button_image, img_center_x, img_center_y-8)

   # display the text on the start game button
   stddraw.picture(Picture(current_dir + "/images/hardtext.png"), img_center_x, img_center_y)
   stddraw.picture(Picture(current_dir + "/images/mediumtext.png"), img_center_x, img_center_y-4)
   stddraw.picture(Picture(current_dir + "/images/easytext.png"), img_center_x, img_center_y-8)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               print("Easy Mode")
               return 5.3 #Easy
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + 4 + button_h:
               print("Normal Mode")
               return 5.7 # Normal
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + 8 + button_h:
               print("Hard Mode")
               return 6 # Hard

   # Three Difficulties Hard,Normal,Easy, 6 , 5.7 , 5.3


def StopMenu(grid,grid_h,grid_w,diffspeed):
   response = grid.ShowMenu()
   if(response == "Menu"): # GO back main menu
      start(grid_h,grid_w,False)
   elif(response == "Restart"): # Restart the game
      start(grid_h,grid_w,True,diffspeed)
   elif(response == "cont"): # Continue to the game
      stddraw.clearKeysTyped()
      return

def UpdateRecords(grid,highest_score,highest_time,grid_h,grid_w):
   current_dir = os.path.dirname(os.path.realpath(__file__))
   if(grid.score > highest_score):
      print("New highest score!")
      highest_score = grid.score
      stddraw.picture(Picture(current_dir + "/images/newhighestscoretext.png"), grid_w / 2, (grid_h / 2)-2)
   if(grid.time > highest_time):
      print("New highest time!")
      highest_time = grid.time
      stddraw.picture(Picture(current_dir + "/images/newhighesttimetext.png"), grid_w / 2, (grid_h / 2)-4)
   RecordSaver.SaveRecords(highest_score,highest_time)

if __name__== '__main__':
   #start()
   SoundGlobal.allow_sound = True
   background_sound_time = time.time()
   SoundCaller('sounds/theme1.wav')
   CreateCanvas()