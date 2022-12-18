import numpy as np
import tkinter as tk
import time as time
import random as rand

#Global
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

MOVES = [UP, DOWN, LEFT, RIGHT]

EMPTY = 0
FOOD = 99

class Game:
    def __init__(self, size, num_snakes, players, gui = None, display = False, max_turns = 100):
        self.size = size
        self.num_snakes = num_snakes
        self.players = players
        self.gui = gui
        self.display = display
        self.max_turns = max_turns
        
        self.num_food = 4
        self.turn = 0
        self.snake_size = 3
        
        self.snakes = [[((j + 1) * self.size//(2 * self.num_snakes), self.size//2 + i) for i in range (self.snake_size)]
                       for j in range (self.num_snakes)]
        self.food = [(self.size//4, self.size//4), 
                     (3 * self.size//4, self.size//4), 
                     (self.size//4, 3 * self.size//4), 
                     (3 * self.size//4, 3 * self.size//4)]
        self.player_ids = [i for i in range (self.num_snakes)]
        
        self.board = np.zeros([self.size, self.size])
        for i in self.player_ids:
            for tup in self.snakes[i]:
                self.board[tup[0]][tup[1]] = i + 1
        for tup in self.food:
            self.board[tup[0]][tup[1]] = FOOD
            
        self.food_index = 0
        self.food_xy = [(8, 3), (9, 7), (9, 3), (8, 6), (8, 2), (0, 8), (6, 1), (5, 2), (6, 3), (1, 3), (6, 2), (1, 7), (8, 5), (9, 4), (1, 4), (3, 8), (3, 6), (8, 0), (3, 7), (7, 6), (2, 8), (0, 1), (8, 8), (0, 4), (4, 3), (7, 1), (3, 5), (1, 4), (9, 6), (3, 3), (6, 2), (1, 8), (5, 3), (1, 9), (8, 2), (6, 1), (2, 0), (9, 9), (0, 7), (7, 0), (3, 3), (8, 9), (1, 4), (9, 0), (5, 0), (9, 1), (4, 9), (5, 8), (3, 1), (4, 1), (0, 6), (9, 1), (8, 7), (5, 9), (5, 9), (4, 6), (5, 9), (1, 8), (3, 2), (1, 1), (1, 3), (2, 0), (2, 9), (5, 6), (1, 3), (9, 9), (5, 2), (9, 9), (2, 7), (6, 2), (8, 0), (8, 0), (8, 5), (5, 8), (7, 7), (9, 5), (9, 6), (8, 9), (8, 4), (3, 8), (4, 7), (3, 0), (4, 2), (4, 4), (2, 2), (7, 4), (4, 6), (5, 4), (4, 8), (8, 9), (8, 8), (8, 6), (1, 2), (7, 6), (1, 2), (7, 5), (4, 2), (0, 0), (7, 4), (9, 2), (0, 5), (8, 5), (5, 1), (4, 5), (9, 0), (7, 9), (7, 6), (6, 6), (8, 4), (7, 4), (1, 1), (4, 2), (6, 5), (9, 4), (7, 0), (3, 9), (3, 2), (7, 2), (1, 9), (5, 5), (2, 5), (1, 6), (5, 1), (7, 9), (7, 4), (4, 0), (4, 0), (4, 1), (1, 1), (2, 5), (5, 5), (9, 5), (0, 0), (7, 8), (2, 5), (9, 3), (2, 2), (8, 0), (7, 5), (1, 9), (5, 4), (8, 0), (8, 8), (7, 5), (4, 9), (6, 1), (0, 4), (9, 5), (8, 7), (2, 3), (9, 1), (6, 6), (7, 3), (9, 9), (7, 7), (7, 2), (2, 6), (2, 8), (6, 5), (8, 0), (1, 7), (1, 6), (6, 2), (4, 0), (1, 4), (2, 6), (4, 7), (8, 7), (5, 7), (5, 1), (7, 4), (2, 2), (8, 3), (6, 3), (3, 2), (6, 4), (4, 7), (2, 0), (3, 6), (1, 9), (5, 1), (8, 3), (1, 6), (9, 9), (0, 0), (1, 2), (7, 7), (9, 4), (8, 8), (8, 4), (0, 5), (9, 0), (6, 9), (4, 7), (1, 5), (1, 7), (5, 3), (4, 2), (5, 8), (7, 5)]
        
    def move(self):
        moves = []
        # move the head
        for i in self.player_ids:
            snake_i = self.snakes[i]
            move_i = self.players[i].get_move(self.board, snake_i)
            moves.append(move_i)
            new_square = (snake_i[-1][0] + move_i[0], snake_i[-1][1] + move_i[1])
            snake_i.append(new_square)
        # update tail
        for i in self.player_ids:
            head_i = self.snakes[i][-1]
            if head_i not in self.food:
                self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = EMPTY
                self.snakes[i].pop(0)
            else:
                self.food.remove(head_i)
        
        # check out of bounds
        for i in self.player_ids:
            head_i = self.snakes[i][-1]
            if head_i[0] >= self.size or head_i[1] >= self.size or head_i[0] < 0 or head_i[1] < 0:
                self.player_ids.remove(i)
            else:
                self.board[head_i[0]][head_i[1]] = i + 1
                
        # check for collisions
        for i in self.player_ids:
            head_i = self.snakes[i][-1]
            for j in range (self.num_snakes):
                if i == j:
                    if head_i in self.snakes[i][:-1]:
                        self.player_ids.remove(i)
                else:
                    if head_i in self.snakes[j]:
                        self.player_ids.remove(i)
            
            # spawn new food
            while len(self.food) < self.num_food:
                x = self.food_xy[self.food_index][0]
                y = self.food_xy[self.food_index][1]
                while self.board[x][y] != EMPTY:
                    self.food_index += 1
                    x = self.food_xy[self.food_index][0]
                    y = self.food_xy[self.food_index][1]
                self.food.append((x, y))
                self.board[x][y] = FOOD
                self.food_index += 1
            return moves
        
    def play(self, display, termination = False):
        if display:
            self.display_board()
        while True:
            if termination:
                for i in self.player_ids:
                    if len(self.snakes[0]) - self.turn/20 <=0:
                        self.player_ids.remove(i)
                        # remove return if more than 1 snakes
                        return -2
            if len(self.player_ids) == 0:
                return -1
            if self.turn >= self.max_turns:
                return 0
            moves = self.move()
            self.turn += 1
            if display:
                for move in moves:
                    if move == UP:
                        print('UP')
                    elif move == DOWN:
                        print('DOWN')
                    elif move == LEFT:
                        print('LEFT')
                    else:
                        print('RIGHT')
                self.display_board()
                if self.gui is not None:
                    self.gui.update()
                time.sleep(3)
        
    def display_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == EMPTY:
                    print('|_', end = '')
                elif self.board[i][j] == FOOD:
                    print('|#', end = '')
                else:
                    print('|' + str(int(self.board[i][j])), end = '')
            print('|')

class Gui:
    def __init__(self ,game, size):
        self.game = game
        self.game.gui = self
        self.size = size
        
        self.ratio = self.size/self.game.size
        
        self.app = tk.Tk()
        self.canvas = tk.Canvas(self.app, width = self.size, height = self.size)
        self.canvas.pack()
        
        for i in range (len(self.game.snakes)):
            color = '#' + '{0:03X}'.format((i + 1) * 500)
            snake = self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio * (snake[-1][1]), 
                                         self.ratio * (snake[-1][0]), 
                                         self.ratio * (snake[-1][1] + 1), 
                                         self.ratio * (snake[-1][0] + 1), fill = color)
            
            for j in range (len(snake) - 1):
                color = '#' + '{0:03X}'.format((i + 1) * 123)
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), 
                                             self.ratio * (snake[j][0]), 
                                             self.ratio * (snake[j][1] + 1), 
                                             self.ratio * (snake[j][0] + 1), fill = color)
            
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio * (food[1]), 
                                             self.ratio * (food[0]), 
                                             self.ratio * (food[1] + 1), 
                                             self.ratio * (food[0] + 1), fill = '#000000000')
    
    def update(self):
        self.canvas.delete('all')
        for i in range (len(self.game.snakes)):
            color = '#' + '{0:03X}'.format((i + 1) * 500)
            snake = self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio * (snake[-1][1]), 
                                         self.ratio * (snake[-1][0]), 
                                         self.ratio * (snake[-1][1] + 1), 
                                         self.ratio * (snake[-1][0] + 1), fill = color)
            
            for j in range (len(snake) - 1):
                color = '#' + '{0:03X}'.format((i + 1) * 123)
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), 
                                             self.ratio * (snake[j][0]), 
                                             self.ratio * (snake[j][1] + 1), 
                                             self.ratio * (snake[j][0] + 1), fill = color)
            
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio * (food[1]), 
                                             self.ratio * (food[0]), 
                                             self.ratio * (food[1] + 1), 
                                             self.ratio * (food[0] + 1), fill = '#000000000')
        self.canvas.pack()
        self.app.update()