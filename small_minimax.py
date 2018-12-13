import random
import os

clear = lambda: os.system('cls')

INF = 10000

X = 1
O = 2

class Board:

    def __init__(self):
        self.board = [3*[0] for i in range(3)]
        self.winner = 0

    def play_move(self,pos,player):
        self.board[pos[0]][pos[1]] = player
        self._calc_winner()

    def undo_move(self,pos):
        self.board[pos[0]][pos[1]] = 0
        self.winner = 0

    def get_legal_moves(self):
        legal_moves = []
        for i in range(3):
            for j in range(3):
                if(not self.board[i][j]):
                    legal_moves.append((i,j))
        return legal_moves

    def _calc_winner(self):
        if not self.winner:
            for i in range(3):
                if(self.board[i][0]!=0 and self.board[i][0]==self.board[i][1]==self.board[i][2]):
                    self.winner = self.board[i][0]
                    break
                if(self.board[0][i]!=0 and self.board[0][i]==self.board[1][i]==self.board[2][i]):
                    self.winner = self.board[0][i]
                    break
            if(self.board[0][0]!=0 and self.board[0][0]==self.board[1][1]==self.board[2][2]):
                self.winner = self.board[0][0]
            if(self.board[2][0]!=0 and self.board[2][0]==self.board[1][1]==self.board[0][2]):
                self.winner = self.board[2][0]

    def __str__(self):
        string = ""
        str_map = {0 : "_",X:"X",O:"O"} 
        for i in range(3):
            for j in range(3):
                string += str_map[self.board[i][j]]
            string += "\n"
        return string

class Bot:

    def __init__(self,color):
        self.color = color
        self.opponent = X if color==O else O
        self.board = Board()
        self.bot_depth = 9
        self.max_evaluation = 1
        self.sample_size = 10

    def _evaluate_state(self):
        if(self.board.winner == self.color):
            return self.max_evaluation
        elif(self.board.winner == self.opponent):
            return -self.max_evaluation
        return 0


    def opponent_move(self,move):
        self.board.play_move(move,self.opponent)

    def get_move(self):
        eval ,move = self.max_move(self.bot_depth)
        print(eval)
        self.board.play_move(move,self.color)
        return move

    def max_move(self,depth):
        evaluation = self._evaluate_state()
        if(abs(evaluation)==self.max_evaluation or depth < 1):
            return (evaluation,None)
        max_eval = (-INF,None)
        valid_moves = self.board.get_legal_moves()
        if not valid_moves:
            return (evaluation,None)
        if(len(valid_moves)>self.sample_size):
            valid_moves = random.sample(valid_moves,self.sample_size)
        random.shuffle(valid_moves)
        for move in valid_moves:
            self.board.play_move(move,self.color)
            tmp_eval,_ = self.min_move(depth-1)
            self.board.undo_move(move)
            if(tmp_eval>max_eval[0]):
                max_eval = (tmp_eval,move)
                if(max_eval == self.max_evaluation):
                    break
        return max_eval

    def min_move(self,depth):
        evaluation = self._evaluate_state()
        if(abs(evaluation)== self.max_evaluation or depth < 1):
            return (evaluation,None)
        min_eval = (INF,None)
        valid_moves = self.board.get_legal_moves()
        if not valid_moves:
            return (evaluation,None)
        if(len(valid_moves)>self.sample_size):
            valid_moves = random.sample(valid_moves,self.sample_size)
        random.shuffle(valid_moves)
        for move in valid_moves:
            self.board.play_move(move,self.opponent)
            tmp_eval,_ = self.max_move(depth-1)
            self.board.undo_move(move)
            if(tmp_eval<min_eval[0]):
                min_eval = (tmp_eval,move)
                if(min_eval==-self.max_evaluation):
                    break
        return min_eval

my_turn = True
bot = Bot(O if my_turn else X)

while not bot.board.winner and bot.board.get_legal_moves():
    if(my_turn):
        print(str(bot.board))
        x,y = [int(i) for i in input().split()]
        bot.opponent_move((x,y))
        clear()
    else:
        bot.get_move()
    my_turn = not my_turn
