import arcade, math, random, time, numpy as np
Screen_width, Screen_height, Screen_title =1070 , 732 , "Snails Game"
Box_height , Box_width, Mod_constant, Margin = 70, 70, 73, 3
Turn_list = ["Human_Left", "Human_Right"]
Next_Backend_grid_row ,Next_Backend_grid_col, Rows , Columns = 0, 0, 10, 10
diff_row_H1 , diff_col_H1, diff_row_H2 , diff_col_H2 , cx , cy, check = 0, 0, 0, 0, 0, 0 , 0

class InstructionMenu(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instruction Menu", Screen_width/2, 600, 
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("1. Objective of the game is to occupy more GridSquares than your opponent.", 60, 550, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("2. Player can move his Snail horizontally or vertically to an adjacent empty GridSquare.", 60, 520, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("In doing so, his score will be increases by 1.", 60, 490, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("3. Besides moving into empty squares, a player can move onto his own trail of slime.", 60, 460, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("Note that in this case, no score will be awarded.", 60, 430, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("4. A player cannot move onto his opponent’s Trail of Slime.", 60, 400, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("5. For any illegal given, player can be panalized. ", 60, 370, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("        # Clicking on an area out of bounds (outside the GridWorld)", 60, 340, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("        # Moving the Snail onto opponent’s Snail or Trail of Slime.", 60, 310, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("        # Non-consecutive moves are illegal.", 60, 280, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("        # If a player moves his sprite in diagonal direction, its legal.", 60, 250, 
                         arcade.color.WHITE, font_size=15, align="center")
        arcade.draw_text("Press Space Button to start the game", Screen_width/2, Screen_height/2-200,
                         arcade.color.GREEN, font_size=35, anchor_x="center")
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            gamePlay =StartGame() 
            self.window.show_view(gamePlay)

class StartGame(arcade.View):
    def __init__(self):
        super().__init__()
        #Initialize the 2D list( Back-end list )
        self.Board = []
        self.status = 0     # 0 means Continue , 50 means Draw , 100 means Human Win & 200 means Bot Win.
        self.Previos_Backend_grid_row_H1 , self.Previos_Backend_grid_col_H1 = 0, 0
        self.Previos_Backend_grid_row_H2 , self.Previos_Backend_grid_col_H2 = 9, 9
        self.Snail_left_list = arcade.SpriteList()
        self.Snail_right_list = arcade.SpriteList()
        self.Snail_left_splash_list = arcade.SpriteList()
        self.Snail_right_splash_list = arcade.SpriteList()
        self.turn = random.choice(Turn_list)
        print(f"turn of {self.turn}") 
        for row in range(Rows):
            #lets add first empty lists in list.
            self.Board.append([])
            for col in range(Columns):
                self.Board[row].append(0)
        self.Board[0][0] = 1
        self.Board[9][9] = 2
        self.Snail_right_sprite = []
        self.Snail_left_sprite = []
        self.Snail_left_splash_sprite = []
        self.Snail_right_splash_sprite = []
        self.Snail_left_sprite = arcade.Sprite("Images/Snail_left.png", scale= 0.1,center_x = Next_Backend_grid_row*74 + 35
                                                            , center_y =  Next_Backend_grid_col* 74 + 35 )
        self.Snail_left_list.append(self.Snail_left_sprite)
        self.Snail_right_sprite = arcade.Sprite("Images/Snail_right.png", scale= 0.1, center_x = Next_Backend_grid_row*74 + 664 + 35
                                                            , center_y =  Next_Backend_grid_col* 74 + 664 + 35  )
        self.Snail_right_list.append(self.Snail_right_sprite)

    def on_draw(self):
        arcade.start_render()
        #Initializa Grid GUI Board
        for row in range(Rows):
            for col in range(Columns):
                color = arcade.color.BLUE
                x = (Margin + Box_width) * col  + Box_width // 2
                y = (Margin + Box_height) * row  + Box_height // 2
                arcade.draw_rectangle_filled(x, y, Box_width, Box_height, color)
        arcade.draw_line(732,0,732,732,arcade.color.WHITE,2)
        arcade.draw_line(732, 367, 1070, 367, arcade.color.WHITE, 2)
        SR = arcade.load_texture("Images/Snail_right.png")
        self.score_SR = f"AI-agent_Score = {self.window.Right_Snail_Score}"
        arcade.draw_lrwh_rectangle_textured(890, 670,54, 54,SR)
        arcade.draw_text( self.score_SR, 845, 640, color= arcade.color.GREEN, font_size= 15)

        SL = arcade.load_texture("Images/Snail_left.png")
        arcade.draw_lrwh_rectangle_textured(890, 80,54, 54,SL)
        self.score_SL = f"Human_Score = {self.window.Left_Snail_Score}"
        arcade.draw_text( self.score_SL, 850, 50, color= arcade.color.RED, font_size= 15)
        if self.turn == "Human_Right":
            turn_line_SR = f"Turn of AI-agent"
            arcade.draw_text(turn_line_SR, 835, 610, color= arcade.color.RED, font_size= 20 )
        else:
            turn_line_SL = f"Turn of Human"
            arcade.draw_text(turn_line_SL, 840, 20, color= arcade.color.GREEN, font_size= 20 )

        self.Snail_left_splash_list.draw()
        self.Snail_left_list.draw()
        self.Snail_right_splash_list.draw()
        self.Snail_right_list.draw()
        
        self.status = self.evaluate_Board(self.Board)
        if self.status != 0: # Stop
            time.sleep(1)
            Game_ovr_object = GameOver()
            self.window.show_view(Game_ovr_object)

    def on_mouse_press(self, x, y, _buttons, _modifiers):
        # print(f"x= {x} & y= {y}")
        self.calculations(x,y)
    
    def calculations(self, x, y):
        Next_Backend_grid_row = int(x / Mod_constant)
        Next_Backend_grid_col = int(y / Mod_constant)
        if Next_Backend_grid_col > 9 or Next_Backend_grid_col < 0:
            print("Click on Out of the Grid World.")
            if self.turn == "Human_Left":
                self.turn = "Human_Right"
                print(f"turn of {self.turn}")
                return
            elif self.turn == "Human_Right":
                self.turn = "Human_Left"
                print(f"turn of {self.turn}")
                return
        if Next_Backend_grid_row > 9 or Next_Backend_grid_row < 0:
            print("Click on Score screen.")
            if self.turn == "Human_Left":
                print(f"turn of {self.turn}")
                return
            elif self.turn == "Human_Right":
                print(f"turn of {self.turn}")
                return
                
        self.status = self.evaluate_Board(self.Board) # Evaluate Board
        print(f"Status = {self.status}") 
        if self.status == 0: # Continue
            if self.turn == "Human_Left":
                self.humanMove(Next_Backend_grid_row, Next_Backend_grid_col)
            else:
                self.botMove(Next_Backend_grid_row, Next_Backend_grid_col)
        else:
            Game_ovr_object = GameOver()
            self.window.show_view(Game_ovr_object)
        print(np.matrix(self.Board))
        

    def humanMove(self, Next_Backend_grid_row, Next_Backend_grid_col):
        check = self.isConsecutiveMoveforHumanLeft(Next_Backend_grid_row, Next_Backend_grid_col)
        if check == 1:
            S1 = self.is_zero_present(self.Board)
            if S1 == 1:
                if self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 0:
                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = 1 # 1 is left snails' number
                    self.Snail_left_sprite = arcade.Sprite("Images/Snail_left.png", scale= 0.1,center_x = Next_Backend_grid_row*74 + 35
                                                    , center_y =  Next_Backend_grid_col* 74 + 35 )
                    self.window.Left_Snail_Score += 1
                    print(f"Score of Human_Left = {self.window.Left_Snail_Score}")
                    self.Snail_left_list.append(self.Snail_left_sprite)
                    self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H1*74 + 35 
                                                            , center_y= self.Previos_Backend_grid_col_H1* 74 +35 )
                    ####
                    self.Collision(self.Snail_left_splash_sprite , self.Snail_left_list)
                    self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1]= 10 # 10 is left snails' splash number
                    self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)
                    self.turn = "Human_Right"
                    self.Previos_Backend_grid_row_H1 = Next_Backend_grid_row 
                    self.Previos_Backend_grid_col_H1 = Next_Backend_grid_col
                    #print(f"in calculation function Previos_Backend_grid_row_H1 = {self.Previos_Backend_grid_row_H1} and Previos_Backend_grid_col_H1 = {self.Previos_Backend_grid_col_H1}")
                elif self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 2 or self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 20:
                    print("illegal move Human_Left because he moved to opponent's area.")
                    self.turn = "Human_Right"
                    print(f"Score of Human_Left = {self.window.Left_Snail_Score}")
                elif self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 10: 
                    print("Entering in Slips area of Human_Left")
                    self.i = Next_Backend_grid_col + 1
                    if self.Previos_Backend_grid_row_H1 == Next_Backend_grid_row: # Horizontal
                        if (Next_Backend_grid_col - self.Previos_Backend_grid_col_H1) == -1: # slip leftward in Horizonal direction
                            print("Horizontal & leftward slip")
                            while(self.i >= 0):
                                if self.Board[self.Previos_Backend_grid_row_H1][Next_Backend_grid_col - 1] == 10:
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                    Next_Backend_grid_col -= 1
                                elif self.Board[self.Previos_Backend_grid_row_H1][Next_Backend_grid_col - 1] != 10:
                                    # Swap values
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1]
                                    self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                    self.Previos_Backend_grid_row_H1 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                    self.Previos_Backend_grid_col_H1 = self.s 
                                    # self.Swap(Next_Backend_grid_col, self.Previos_Backend_grid_col_H1)
                                    self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                            , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)
                                    self.Snail_left_sprite = arcade.Sprite("Images/Snail_Left.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H1*74 + 35
                                                                    , center_y= self.Previos_Backend_grid_col_H1* 74 + 35  )          
                                    self.Snail_left_list.append(self.Snail_left_sprite)
                                    self.Collision(self.Snail_left_splash_sprite , self.Snail_left_list)
                                    break
                                #print(f"i= {self.i}")
                                self.i -= 1
                            self.turn = "Human_Right"
                            print(f"self.Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H1} & self.Previos_Backend_grid_col_H1= {self.Previos_Backend_grid_col_H1}")
                        elif (Next_Backend_grid_col - self.Previos_Backend_grid_col_H1) == 1: # slip rightward in Horizonal direction
                            print("Horizontal rightward slip")
                            # Next_Backend_grid_col -= 1
                            #self.i = Next_Backend_grid_col 
                            while(Next_Backend_grid_col !=9): # while(self.i <= 9 ):
                                #print(f"i= {self.i}")
                                # print(f"Next_Backend_grid_row= {Next_Backend_grid_row} & Next_Backend_grid_col= {Next_Backend_grid_col}")
                                # print(f"Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H1} & self.Previos_Backend_grid_col_H1={self.Previos_Backend_grid_row_H1}")
                                if self.Board[self.Previos_Backend_grid_row_H1][Next_Backend_grid_col + 1 ] == 10:
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                    Next_Backend_grid_col += 1
                                elif self.Board[self.Previos_Backend_grid_row_H1][Next_Backend_grid_col + 1 ] != 10:
                                    # Swap values
                                    # Next_Backend_grid_col += 1
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1]
                                    self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                    self.Previos_Backend_grid_row_H1 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                    self.Previos_Backend_grid_col_H1 = self.s

                                    # self.Swap(Next_Backend_grid_col, self.Previos_Backend_grid_col_H1)
                                    self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                            , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)

                                    self.Snail_left_sprite = arcade.Sprite("Images/Snail_Left.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H1*74 + 35
                                                                    , center_y= self.Previos_Backend_grid_col_H1* 74 + 35  )          
                                    self.Snail_left_list.append(self.Snail_left_sprite)
                                    self.Collision(self.Snail_left_splash_sprite , self.Snail_left_list)
                                    break
                                            
                                #print(f"Next_Backend_grid_row= {Next_Backend_grid_row} & Next_Backend_grid_col= {Next_Backend_grid_col}")
                                #print(f"Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H1} & self.Previos_Backend_grid_col_H1={self.Previos_Backend_grid_row_H1}")
                                #print(f"i= {self.i}")
                                #self.i += 1
                                self.turn = "Huma_Right"
                            if Next_Backend_grid_col == 9:
                                # Next_Backend_grid_col -= 1
                                self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1]
                                self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1] = self.s
                                # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                self.s = Next_Backend_grid_row 
                                Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                self.Previos_Backend_grid_row_H1 = self.s
                                # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                self.s = Next_Backend_grid_col
                                Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                self.Previos_Backend_grid_col_H1 = self.s

                                # self.Swap(Next_Backend_grid_col, self.Previos_Backend_grid_col_H1)
                                self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                            , center_y= Next_Backend_grid_col* 74 + 35)
                                self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)
                                self.Snail_left_sprite = arcade.Sprite("Images/Snail_Left.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H1*74 + 35
                                                                    , center_y= self.Previos_Backend_grid_col_H1* 74 + 35  )          
                                self.Snail_left_list.append(self.Snail_left_sprite)
                                self.Collision(self.Snail_left_splash_sprite , self.Snail_left_list)
                                self.turn = "Human_Right"
                            # print(f"self.Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H1} & self.Previos_Backend_grid_col_H1= {self.Previos_Backend_grid_col_H1}")
                    elif self.Previos_Backend_grid_col_H1 == Next_Backend_grid_col: # Vertical
                        print("Entering in vertical Slips area")
                        # self.i = Next_Backend_grid_row
                        if (Next_Backend_grid_row - self.Previos_Backend_grid_row_H1) == 1: # Upward
                            print("Entering in Verical upward slip")
                            while(Next_Backend_grid_row != 9):
                                if self.Board[Next_Backend_grid_row + 1][self.Previos_Backend_grid_col_H1] == 10:
                                    Next_Backend_grid_row += 1
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                elif self.Board[Next_Backend_grid_row + 1][self.Previos_Backend_grid_col_H1] != 10:
                                    # Swap values
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1]
                                    self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                    self.Previos_Backend_grid_row_H1 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                    self.Previos_Backend_grid_col_H1 = self.s
                                    self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                            , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)

                                    self.Snail_left_sprite = arcade.Sprite("Images/Snail_Left.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H1*74 + 35
                                                                    , center_y= self.Previos_Backend_grid_col_H1* 74 + 35  )          
                                    self.Snail_left_list.append(self.Snail_left_sprite)
                                    self.Collision(self.Snail_left_splash_sprite , self.Snail_left_list)
                                    break
                                            
                                #print(f"i= {self.i}")
                                #self.i += 1
                            self.turn = "Human_Right"
                            # print(f"Next_Backend_grid_row= {Next_Backend_grid_row} & Next_Backend_grid_col= {Next_Backend_grid_col}")
                            # print(f"self.Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H1} & self.Previos_Backend_grid_col_H1= {self.Previos_Backend_grid_col_H1}")
                            if Next_Backend_grid_row == 9:
                                self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1]
                                self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1] = self.s
                                # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                self.s = Next_Backend_grid_row 
                                Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                self.Previos_Backend_grid_row_H1 = self.s
                                # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                self.s = Next_Backend_grid_col 
                                Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                self.Previos_Backend_grid_col_H1 = self.s
                                self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                            , center_y= Next_Backend_grid_col* 74 + 35)
                                self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)
                                self.Snail_left_sprite = arcade.Sprite("Images/Snail_Left.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H1*74 + 35
                                                                    , center_y= self.Previos_Backend_grid_col_H1* 74 + 35  )          
                                self.Snail_left_list.append(self.Snail_left_sprite)
                                self.Collision(self.Snail_left_splash_sprite , self.Snail_left_list)
                                self.turn = "Human_Right"
                        elif (Next_Backend_grid_row - self.Previos_Backend_grid_row_H1) == -1: # Downward
                            print("Entering in Vertical downward slip area")
                            Next_Backend_grid_row += 1
                            while(Next_Backend_grid_row >= 0): 
                                if self.Board[Next_Backend_grid_row - 1][self.Previos_Backend_grid_col_H1] == 10:
                                    Next_Backend_grid_row -= 1 
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                elif self.Board[Next_Backend_grid_row - 1][self.Previos_Backend_grid_col_H1] != 10:
                                    # Swap values
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1]
                                    self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H1
                                    self.Previos_Backend_grid_row_H1 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H1
                                    self.Previos_Backend_grid_col_H1 = self.s
                                    self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                            , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)

                                    self.Snail_left_sprite = arcade.Sprite("Images/Snail_Left.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H1*74 + 35
                                                                    , center_y= self.Previos_Backend_grid_col_H1* 74 + 35  )          
                                    self.Snail_left_list.append(self.Snail_left_sprite)
                                    self.Collision(self.Snail_left_splash_sprite , self.Snail_left_list)
                                    break
                            self.turn = "Human_Right"
            else:
                print("GameOver") #no zero in backend grid. so shift to 3rd View.
                Game_ovr_object = GameOver()
                self.window.show_view(Game_ovr_object)
        else:
            print("illegal move by Human_Left because of non-consective move")
            self.turn = "Human_Right"

    def botMove(self, Next_Backend_grid_row, Next_Backend_grid_col ):
        check = self.isConsecutiveMoveforHumanRight(Next_Backend_grid_row, Next_Backend_grid_col)
        if check == 1:
            S2 = self.is_zero_present(self.Board)
            if S2 == 1:
                if self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 0:
                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = 2
                    self.Snail_right_sprite = arcade.Sprite("Images/Snail_right.png", scale= 0.1, center_x = Next_Backend_grid_row*74 + 35
                                                        , center_y =  Next_Backend_grid_col* 74 + 35  )
                    self.window.Right_Snail_Score += 1
                    print(f"Score of Human_Right = {self.window.Right_Snail_Score}")
                    self.Snail_right_list.append(self.Snail_right_sprite)
                    self.Snail_right_splash_sprite = arcade.Sprite("Images/Right_splash.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H2*74 + 35 
                                                                , center_y= self.Previos_Backend_grid_col_H2* 74 +35 )
                    self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2]= 20 # 20 is right snails' splash number
                    self.Snail_right_splash_list.append(self.Snail_right_splash_sprite)
                    self.Collision(self.Snail_right_splash_sprite , self.Snail_right_list)
                    self.turn = "Human_Left"
                    self.Previos_Backend_grid_row_H2 = Next_Backend_grid_row 
                    self.Previos_Backend_grid_col_H2 = Next_Backend_grid_col
                elif self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 1 or self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 10:
                    print("illegal move Human_Right because he moved to opponent's area.")
                    self.turn = "Human_Left"
                    print(f"Score of Human_Right = {self.window.Right_Snail_Score}")
                    # elif self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 2:
                    #     print("Same location choosen from Human_Right")
                    #     self.turn = "Human_Left"
                elif self.Board[Next_Backend_grid_row][Next_Backend_grid_col] == 20:
                    # Slips for Human_Right
                    if Next_Backend_grid_col == self.Previos_Backend_grid_col_H2: # Vertical
                        print("Entering in vertical Slips area")
                        if (Next_Backend_grid_row - self.Previos_Backend_grid_row_H2) == -1: # Downward
                            print("Entering in Downard slip area")
                            #self.i = Next_Backend_grid_row
                            while(Next_Backend_grid_row >= 0): 
                                if self.Board[Next_Backend_grid_row - 1][self.Previos_Backend_grid_col_H2] == 20:
                                    Next_Backend_grid_row -= 1 
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                elif self.Board[Next_Backend_grid_row - 1][self.Previos_Backend_grid_col_H2] != 20:
                                    # Swap values
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2]
                                    self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                    self.Previos_Backend_grid_row_H2 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                    self.Previos_Backend_grid_col_H2 = self.s
                                    self.Snail_right_splash_sprite = arcade.Sprite("Images/Right_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                                , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_right_splash_list.append(self.Snail_right_splash_sprite)

                                    self.Snail_right_sprite = arcade.Sprite("Images/Snail_Right.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H2*74 + 35
                                                                                , center_y= self.Previos_Backend_grid_col_H2* 74 + 35  )          
                                    self.Snail_right_list.append(self.Snail_right_sprite)
                                    self.Collision(self.Snail_right_splash_sprite , self.Snail_right_list)
                                    break
                                #print(f"i= {self.i}")
                                #self.i -= 1
                            self.turn = "Human_Left"
                            #print(f"Next_Backend_grid_row= {Next_Backend_grid_row} & Next_Backend_grid_col= {Next_Backend_grid_col}")
                            #print(f"self.Previos_Backend_grid_row_H2= {self.Previos_Backend_grid_row_H2} & self.Previos_Backend_grid_col_H2= {self.Previos_Backend_grid_col_H2}")
                        elif (Next_Backend_grid_row - self.Previos_Backend_grid_row_H2) == 1: # Upward
                            print("Entering in Verical upward slip")
                            while(Next_Backend_grid_row != 9):
                                if self.Board[Next_Backend_grid_row + 1][self.Previos_Backend_grid_col_H2] == 20:
                                    Next_Backend_grid_row += 1
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                elif self.Board[Next_Backend_grid_row + 1][self.Previos_Backend_grid_col_H2] != 20:
                                    # Swap values
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2]
                                    self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                    self.Previos_Backend_grid_row_H2 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                    self.Previos_Backend_grid_col_H2 = self.s
                                    self.Snail_right_splash_sprite = arcade.Sprite("Images/Right_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                                        , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_right_splash_list.append(self.Snail_right_splash_sprite)

                                    self.Snail_right_sprite = arcade.Sprite("Images/Snail_Right.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H2*74 + 35
                                                                                , center_y= self.Previos_Backend_grid_col_H2* 74 + 35  )          
                                    self.Snail_right_list.append(self.Snail_right_sprite)
                                    self.Collision(self.Snail_right_splash_sprite , self.Snail_right_list)
                                    break
                            self.turn = "Human_Left"
                            #print(f"Next_Backend_grid_row= {Next_Backend_grid_row} & Next_Backend_grid_col= {Next_Backend_grid_col}")
                            #print(f"self.Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H2} & self.Previos_Backend_grid_col_H1= {self.Previos_Backend_grid_col_H2}")
                            if Next_Backend_grid_row == 9:
                                self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2]
                                self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2] = self.s
                                # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                self.s = Next_Backend_grid_row 
                                Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                self.Previos_Backend_grid_row_H2 = self.s
                                # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                self.s = Next_Backend_grid_col
                                Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                self.Previos_Backend_grid_col_H2 = self.s

                                # self.Swap(Next_Backend_grid_col, self.Previos_Backend_grid_col_H1)
                                self.Snail_right_splash_sprite = arcade.Sprite("Images/Right_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                                        , center_y= Next_Backend_grid_col* 74 + 35)
                                self.Snail_right_splash_list.append(self.Snail_right_splash_sprite)
                                self.Snail_right_sprite = arcade.Sprite("Images/Snail_Right.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H2*74 + 35
                                                                                , center_y= self.Previos_Backend_grid_col_H2* 74 + 35  )          
                                self.Snail_right_list.append(self.Snail_right_sprite)
                                self.Collision(self.Snail_right_splash_sprite , self.Snail_right_list)
                                self.turn = "Human_Left" 
                    elif self.Previos_Backend_grid_row_H2 == Next_Backend_grid_row: # Horizontal
                        if (Next_Backend_grid_col - self.Previos_Backend_grid_col_H2) == -1: # slip leftward in Horizonal direction
                            print("Horizontal leftward slip")
                            self.i = Next_Backend_grid_col
                            while(self.i >= 0):
                                if self.Board[self.Previos_Backend_grid_row_H2][Next_Backend_grid_col - 1] == 20:
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                    Next_Backend_grid_col -= 1
                                elif self.Board[self.Previos_Backend_grid_row_H2][Next_Backend_grid_col - 1] != 20:
                                    # Swap values
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2]
                                    self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                    self.Previos_Backend_grid_row_H2 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                    self.Previos_Backend_grid_col_H2 = self.s

                                    # self.Swap(Next_Backend_grid_col, self.Previos_Backend_grid_col_H1)
                                    self.Snail_right_splash_sprite = arcade.Sprite("Images/Right_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                                        , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_right_splash_list.append(self.Snail_right_splash_sprite)

                                    self.Snail_right_sprite = arcade.Sprite("Images/Snail_Right.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H2*74 + 35
                                                                                , center_y= self.Previos_Backend_grid_col_H2* 74 + 35  )          
                                    self.Snail_right_list.append(self.Snail_right_sprite)
                                    # self.Snail_left_splash_sprite = arcade.Sprite("Images/Left_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                    #                                        , center_y= Next_Backend_grid_col* 74 + 35)
                                    # self.Snail_left_splash_list.append(self.Snail_left_splash_sprite)
                                    self.Collision(self.Snail_right_splash_sprite , self.Snail_right_list)
                                    break
                                #print(f"i= {self.i}")
                                self.i -= 1
                            self.turn = "Human_Left"
                            print(f"self.Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H2} & self.Previos_Backend_grid_col_H1= {self.Previos_Backend_grid_col_H2}")
                        elif (Next_Backend_grid_col - self.Previos_Backend_grid_col_H2) == 1: # slip rightward in Horizonal direction
                            print("Horizontal rightward slip")
                            # Next_Backend_grid_col -= 1
                            #self.i = Next_Backend_grid_col 
                            while(Next_Backend_grid_col !=9): # while(self.i <= 9 ):
                                #print(f"i= {self.i}")
                                # print(f"Next_Backend_grid_row= {Next_Backend_grid_row} & Next_Backend_grid_col= {Next_Backend_grid_col}")
                                # print(f"Previos_Backend_grid_row_H1= {self.Previos_Backend_grid_row_H1} & self.Previos_Backend_grid_col_H1={self.Previos_Backend_grid_row_H1}")
                                if self.Board[self.Previos_Backend_grid_row_H2][Next_Backend_grid_col + 1 ] == 20:
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                    Next_Backend_grid_col += 1
                                elif self.Board[self.Previos_Backend_grid_row_H2][Next_Backend_grid_col + 1 ] != 20:
                                    # Swap values
                                    # Next_Backend_grid_col += 1
                                    self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                    self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2]
                                    self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2] = self.s
                                    # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                    self.s = Next_Backend_grid_row 
                                    Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                    self.Previos_Backend_grid_row_H1 = self.s
                                    # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                    self.s = Next_Backend_grid_col
                                    Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                    self.Previos_Backend_grid_col_H2 = self.s

                                    # self.Swap(Next_Backend_grid_col, self.Previos_Backend_grid_col_H1)
                                    self.Snail_right_splash_sprite = arcade.Sprite("Images/Right_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                                        , center_y= Next_Backend_grid_col* 74 + 35)
                                    self.Snail_right_splash_list.append(self.Snail_right_splash_sprite)

                                    self.Snail_right_sprite = arcade.Sprite("Images/Snail_right.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H2*74 + 35
                                                                                , center_y= self.Previos_Backend_grid_col_H2* 74 + 35  )          
                                    self.Snail_right_list.append(self.Snail_right_sprite)
                                    self.Collision(self.Snail_right_splash_sprite , self.Snail_right_list)
                                    break
                                            
                                #print(f"Next_Backend_grid_row= {Next_Backend_grid_row} & Next_Backend_grid_col= {Next_Backend_grid_col}")
                                #print(f"Previos_Backend_grid_row_H2= {self.Previos_Backend_grid_row_H2} & self.Previos_Backend_grid_col_H2={self.Previos_Backend_grid_row_H2}")
                                #print(f"i= {self.i}")
                                #self.i += 1
                            self.turn = "Human_Left"
                            if Next_Backend_grid_col == 9:
                                # Next_Backend_grid_col -= 1
                                self.s = self.Board[Next_Backend_grid_row][Next_Backend_grid_col] 
                                self.Board[Next_Backend_grid_row][Next_Backend_grid_col] = self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2]
                                self.Board[self.Previos_Backend_grid_row_H2][self.Previos_Backend_grid_col_H2] = self.s
                                # self.Swap(self.Board[Next_Backend_grid_row][Next_Backend_grid_col], self.Board[self.Previos_Backend_grid_row_H1][self.Previos_Backend_grid_col_H1])
                                self.s = Next_Backend_grid_row 
                                Next_Backend_grid_row = self.Previos_Backend_grid_row_H2
                                self.Previos_Backend_grid_row_H2 = self.s
                                # self.Swap(Next_Backend_grid_row, self.Previos_Backend_grid_row_H1)
                                self.s = Next_Backend_grid_col
                                Next_Backend_grid_col = self.Previos_Backend_grid_col_H2
                                self.Previos_Backend_grid_col_H2 = self.s
                                # self.Swap(Next_Backend_grid_col, self.Previos_Backend_grid_col_H1)
                                self.Snail_right_splash_sprite = arcade.Sprite("Images/Right_splash.png", scale= 0.1, center_x= Next_Backend_grid_row* 74 + 35
                                                                                        , center_y= Next_Backend_grid_col* 74 + 35)
                                self.Snail_right_splash_list.append(self.Snail_right_splash_sprite)
                                self.Snail_right_sprite = arcade.Sprite("Images/Snail_right.png", scale= 0.1, center_x= self.Previos_Backend_grid_row_H2*74 + 35
                                                                                , center_y= self.Previos_Backend_grid_col_H2* 74 + 35  )          
                                self.Snail_right_list.append(self.Snail_right_sprite)
                                self.Collision(self.Snail_right_splash_sprite , self.Snail_right_list) 
                                self.turn = "Human_Left"
                            #print(f"self.Previos_Backend_grid_row_H2= {self.Previos_Backend_grid_row_H2} & self.Previos_Backend_grid_col_H2= {self.Previos_Backend_grid_col_H2}")
            else:
                print("GameOver")
                Game_ovr_object = GameOver()
                self.window.show_view(Game_ovr_object)
        else:
            print("illegal move by Human_Right because of non-consective move.")
            self.turn = "Human_Left"

    def Swap(self, a, b):
        a , b = b , a
    
    def Collision(self, individual , list):
        enemies = arcade.check_for_collision_with_list( individual , list)
        for enemy in enemies:
            enemy.remove_from_sprite_lists()

    def isConsecutiveMoveforHumanLeft(self, x, y):
        diff_col_H1 = y - self.Previos_Backend_grid_col_H1
        diff_row_H1 = x - self.Previos_Backend_grid_row_H1
        if diff_col_H1 == -1 or diff_col_H1 == 1:
            if diff_row_H1 == 0:
                return 1 # move left(-1) or right(1) in column  and row( difference 0) remain same
        elif diff_row_H1 == -1 or diff_row_H1 == 1:
            if diff_col_H1 == 0:
                return 1 # move up and down in rows and column( difference 0 ) remains same.
        elif diff_row_H1 == 0 and diff_col_H1 == 0:
            print("Same location of Human_Left")
            return 1
        else:
            return 0

    def isConsecutiveMoveforHumanRight(self, x, y):
        diff_row_H2 = x - self.Previos_Backend_grid_row_H2
        diff_col_H2 = y - self.Previos_Backend_grid_col_H2
        if diff_col_H2 == -1 or diff_col_H2 == 1:
            if diff_row_H2 == 0:
                return 1
        elif diff_row_H2 == -1 or diff_row_H2 == 1:
            if diff_col_H2 == 0:
                return 1
        elif diff_row_H2 == 0 and diff_col_H2 == 0: 
             print("Same location of Human_Right")
             return 1
        else:
            return 0
    def minimax(self,board, depth, maxdepth, isAgentTurn):
        
        result = self.evaluate_Board() 
        if depth == maxdepth: 
            bestScore = result
            bestChild = board
            #return bestScore, bestChild
        if isAgentTurn:
            pass

    def evaluate_Board(self, board):
        Zero = self.is_zero_present(board)
        if Zero == 1:
            return 0 # Continue state
        else:
            if board.count(10) + 1 == board.count(20) + 1:
                return 50 # Draw state
            elif board.count(10) + 1 >= board.count(20) + 1:
                return 100 # Human Win
            else:
                return 200 # Bot Win
            
    def is_zero_present(self, board):
        s = np.array(board)
        check = 0 in s
        if check == 1:
            return 1
        else:
            return 0
    
class GameOver(StartGame):
    def __init__(self):
        super().__init__()
        self.Score_line = " "
    def on_show(self):
        arcade.set_background_color(arcade.color.NAVY_BLUE)
    def on_draw(self):
        arcade.start_render()
        if self.window.Left_Snail_Score == self.window.Right_Snail_Score:
            arcade.draw_text("Game Draw", Screen_width/2, Screen_height/2-200,arcade.color.YELLOW_ORANGE,font_size=50, anchor_x= "center" )
            self.Score_line = f"Human Score = {self.window.Left_Snail_Score} & Bot Score = {self.window.Right_Snail_Score}"
            arcade.draw_text(self.Score_line, Screen_width/2-50, Screen_height/2-250,arcade.color.YELLOW_ORANGE, font_size= 30, anchor_x= "center")
        elif self.window.Left_Snail_Score >= self.window.Right_Snail_Score:
            arcade.draw_text("Human Won", Screen_width/2, Screen_height/2-200,arcade.color.YELLOW_ORANGE, font_size= 50 ,anchor_x= "center")
            self.Score_line = f"Human Score = {self.window.Left_Snail_Score} & Bot Score = {self.window.Right_Snail_Score}"
            arcade.draw_text(self.Score_line, Screen_width/2-50, Screen_height/2-250,arcade.color.YELLOW_ORANGE, font_size= 30, anchor_x= "center")
        else: 
            arcade.draw_text("Bot Won", Screen_width/2, Screen_height/2-200,arcade.color.YELLOW_ORANGE, font_size= 50 ,anchor_x= "center")
            self.Score_line = f" Bot Score = {self.window.Right_Snail_Score} & Human Score = {self.window.Left_Snail_Score}"
            arcade.draw_text(self.Score_line, Screen_width/2-50, Screen_height/2-250,arcade.color.YELLOW_ORANGE, font_size= 30, anchor_x= "center")
def main():

    output_window=arcade.Window(Screen_width, Screen_height, Screen_title,  resizable= True)
    output_window.Left_Snail_Score = 1
    output_window.Right_Snail_Score = 1
    menu_screen = InstructionMenu()
    output_window.show_view(menu_screen)
    arcade.run()

if __name__ == "__main__":
    main() 
