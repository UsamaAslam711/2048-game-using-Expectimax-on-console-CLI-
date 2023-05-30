
        a1 = get_available_from_zeros(self.grid)

        for x in dirs:
            if not a1[x]:
                board_clone = self.clone()

                if board_clone.move(x, True):
                    available_moves.append(x)

            else:
                available_moves.append(x)

        return available_moves

    def get_cell_value(self, pos):
        return self.grid[pos[0]][pos[1]]

import math
import time
import numpy as np

UP, DOWN, LEFT, RIGHT = range(4)

class Expectimax():

    def get_move(self, board):
        best_move, _ = self.maximize(board)
        return best_move


    #degerlendirme fonksiyonu
    def evaluationFunction(self, board, n_empty): 
        grid = board.grid

        empty_w = 50000  # bos karelerin saglayacagi fayda degeri
        loss_w = 2  # kareler arasindaki farkin verecegi zarar degerinin alıncagi üstel deger
        utility = 0 #fayda
        loss = 0 #zarar

        p_grid = np.sum(np.power(grid, 2)) # grid 4*4luk bir matrix. Hepsinin ikinci kuvveti alınıp toplanıyor.
        s_grid = np.sqrt(grid) # gridin kök alınmış hali
        # kök alınmış matrisin yan yana olan satır ve sütunlarının farklarının mutlak değerleri toplanıyor
        loss  = -np.sum(np.abs(s_grid[::,0] - s_grid[::,1])) -np.sum(np.abs(s_grid[::,1] - s_grid[::,2])) - np.sum(np.abs(s_grid[::,2] - s_grid[::,3]))
        loss  += -np.sum(np.abs(s_grid[0,::] - s_grid[1,::])) -np.sum(np.abs(s_grid[1,::] - s_grid[2,::])) -np.sum(np.abs(s_grid[2,::] - s_grid[3,::]))
        #negatif bir sayı oluşur

        loss_u = loss ** loss_w # kareler arasindaki farkin verecegi toplam zarar degeri
        empty_u = n_empty * empty_w  # bos karelerin verecegi toplam utility degeri 
        p_grid_u = p_grid
        utility += (p_grid + empty_u + loss_u)
        #utility toplami icin bos karelerin faydasi, smoothness degerlerinin verdigi zarar ve matrixin 
        #değerlerinin buyuklugu toplanir.

        return (utility, empty_u, loss_u, p_grid_u)


    # subtreelerden gelen degerlerin en buyugunun secildiği fonksiyon
    def maximize(self, board, depth = 0):
        moves = board.get_available_moves() #yapilabilecek hamleler alinir
        moves_boards = []

        for m in moves:
            m_board = board.clone() # o anki hamle uygulanırsa olusacak boardu olusturacagiz
            m_board.move(m) # move fonksiyonu ile olusturuyoruz
            moves_boards.append((m, m_board)) # tüm hamlelerin boardlarının tutuldugu listeye ekliyoruz

        best_utility = (float('-inf'),0,0,0) # tüm utilityler arasında en iyi olani tutulacak
        best_direction = None

        for mb in moves_boards:
            utility = self.chance(mb[1], depth + 1) # her hamlenin tahtasinin chance degeri hesaplanir

            if utility[0] >= best_utility[0]: # bu degerlerin en buyugu secilir
                best_utility = utility
                best_direction = mb[0]

        return best_direction, best_utility # en iyi hamle donulur


    # bir sonraki elde yapılabilecek hamlelerin optimal olmadigi kabul edilir ve her subtreenin ortalamasi alinir.
    def chance(self, board, depth = 0):
        empty_cells = board.get_available_cells() # bos hucreler listesi
        noOfEmpty = len(empty_cells) # bos hucre sayisi

        #if n_empty >= 7 and depth >= 5:
        #    return self.eval_board(board, n_empty)

        if noOfEmpty >= 6 and depth >= 3:  # bos hucre sayisi 6dan buyukse ve derinlik 3ten buyukse 
            return self.evaluationFunction(board, noOfEmpty) # utility degerlerini dondur
        if 6 > noOfEmpty >= 0 and depth >= 5:  # bos hucre sayisi 6-0 arasindaysa ve derinlik 5ten buyukse
            return self.evaluationFunction(board, noOfEmpty) # utility degerlerini dondur

        # bos hucre sayisi arttıkca derinlik artıyor. Bunun sebebi oyunun zorlasmasıdır. Bir diger sebebi ise 
        # oyun kolayken buyuk bir derinlik vermenin sureyi uzatacak olmasidir. Bu yüzden zorlastikca derinlik artıyor.

        if noOfEmpty == 0:
            _, utility = self.maximize(board, depth + 1)  #yon ignore edilir
            return utility

        possible_tiles = []
        # her el yeni bir sayi tahtaya eklenir
        chanceOf2 = (.95 * (1 / noOfEmpty))  # random olarak 2 gelme olasiligi daha cok
        chanceOf4 = (.05 * (1 / noOfEmpty))  # random olarak 4 gelme olasiligi daha az
        
        for empty_cell in empty_cells:
            possible_tiles.append((empty_cell, 2, chanceOf2))
            possible_tiles.append((empty_cell, 4, chanceOf4))

        totalUtility = [0, 0, 0, 0]

        for t in possible_tiles:
            t_board = board.clone()
            t_board.insert_tile(t[0], t[1])  # 4 ya da 2 eklenir
            _, utility = self.maximize(t_board, depth + 1)

            for i in range(4):
                totalUtility[i] += utility[i] * t[2]

        return tuple(totalUtility)



from random import randint, seed

dirs = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

class CLIRunner:
    def __init__(self):
        self.board = GameBoard()
        self.ai = AI()

        self.init_game()
        self.print_board()

        self.run_game()

        self.over = False

    def init_game(self):
        self.insert_random_tile()
        self.insert_random_tile()

    def run_game(self):
        while True:
            move = self.ai.get_move(self.board)
            self.board.move(move)
            print(dirs[move])
            self.print_board()
            self.insert_random_tile()
            self.print_board()

            if len(self.board.get_available_moves()) == 0:
                print("GAME OVER (max tile): " + str(self.board.get_max_tile()))
                break

    def print_board(self):
        for i in range(4):
            for j in range(4):
                continou
            

    def insert_random_tile(self):
        if randint(0,99) < 100 * 0.9:
            value = 2
        else:
            value = 4

        cells = self.board.get_available_cells()
        pos = cells[randint(0, len(cells) - 1)] if cells else None

        if pos is None:
            return None
        else:
            self.board.insert_tile(pos, value)
            return pos

if __name__ == '__main__':
    CLIRunner = CLIRunner()

from tkinter import Frame, Label, CENTER
from random import randint
import time



SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.grid_cells = []

        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.AI = AI()

        self.run_game()
        self.mainloop()

    def run_game(self):
        while True:
            self.board.move(self.AI.get_move(self.board))
            self.update_grid_cells()
            self.add_random_tile()
            self.update_grid_cells()

            if len(self.board.get_available_moves()) == 0:
                self.game_over_display()
                break

            self.update()
        
    def game_over_display(self):
        for i in range(4):
            for j in range(4):
                self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)

        self.grid_cells[1][1].configure(text="TOP",bg=BACKGROUND_COLOR_CELL_EMPTY)
        self.grid_cells[1][2].configure(text="4 TILES:",bg=BACKGROUND_COLOR_CELL_EMPTY)
        top_4 = list(map(int, reversed(sorted(list(self.board.grid.flatten())))))
        self.grid_cells[2][0].configure(text=str(top_4[0]), bg=BACKGROUND_COLOR_DICT[2048], fg=CELL_COLOR_DICT[2048])
        self.grid_cells[2][1].configure(text=str(top_4[1]), bg=BACKGROUND_COLOR_DICT[2048], fg=CELL_COLOR_DICT[2048])
        self.grid_cells[2][2].configure(text=str(top_4[2]), bg=BACKGROUND_COLOR_DICT[2048], fg=CELL_COLOR_DICT[2048])
        self.grid_cells[2][3].configure(text=str(top_4[3]), bg=BACKGROUND_COLOR_DICT[2048], fg=CELL_COLOR_DICT[2048])
        self.update()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()

        for i in range(GRID_LEN):
            grid_row = []

            for j in range(GRID_LEN):

                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

