# Minimax with alpha beta pruning

import random

INF = 10000

X = 1
O = 2

class MiniBoard:

    def __init__(self):
        self.board = [3*[0] for i in range(3)]
        self.winner = 0

    def play_move(self,pos,player):
        self.board[pos[0]][pos[1]] = player
        self._calc_winner()

    def undo_move(self,pos):
        self.board[pos[0]][pos[1]] = 0
        self.winner = 0

    def get_legal_moves(self,big_pos):
        legal_moves = []
        for i in range(3):
            for j in range(3):
                if(not self.board[i][j]):
                    legal_moves.append((big_pos[0]*3+i,big_pos[1]*3+j))
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

class Board:

    def __init__(self):
        self.board = [[MiniBoard(),MiniBoard(),MiniBoard()] for i in range(3)]
        self.winner = 0
        self.move_history = []

    def play_move(self,pos,player):
        self.move_history.append(pos)
        board_pos,mini_pos = self._calc_pos(pos)
        mini_board = self.board[board_pos[0]][board_pos[1]]
        mini_board.play_move((mini_pos[0],mini_pos[1]),player)
        if(mini_board.winner):
            self._calc_winner()

    def undo_move(self):
        pos = self.move_history.pop()
        board_pos,mini_pos = self._calc_pos(pos)
        self.board[board_pos[0]][board_pos[1]].undo_move((mini_pos[0],mini_pos[1]))
        self.winner = 0

    def get_legal_moves(self):
        if(self.move_history):
            pos = self.move_history[-1]
            _,board_pos = self._calc_pos(pos)
            if(self.board[board_pos[0]][board_pos[1]].winner):
                return self._get_all_legal_moves()
            return self.board[board_pos[0]][board_pos[1]].get_legal_moves(board_pos)
        else:
            return self._get_all_legal_moves()

    def _get_all_legal_moves(self):
        all_moves = []
        for i in range(3):
            for j in range(3):
                if(not self.board[i][j].winner):
                    all_moves.extend(self.board[i][j].get_legal_moves((i,j)))
        return all_moves

    def _calc_pos(self,pos):
        x_board = pos[0]//3
        y_board = pos[1]//3

        x_mini = pos[0] % 3
        y_mini = pos[1] % 3

        return ((x_board,y_board),(x_mini,y_mini))

    def _calc_winner(self):
        for i in range(3):
            if(self.board[i][0].winner!=0 and self.board[i][0].winner==self.board[i][1].winner==self.board[i][2].winner):
                self.winner = self.board[i][0].winner
                break
            if(self.board[0][i].winner!=0 and self.board[0][i].winner==self.board[1][i].winner==self.board[2][i].winner):
                self.winner = self.board[0][i].winner
                break
        if(self.board[0][0].winner!=0 and self.board[0][0].winner==self.board[1][1].winner==self.board[2][2].winner):
            self.winner = self.board[0][0].winner
        if(self.board[2][0].winner!=0 and self.board[2][0].winner==self.board[1][1].winner==self.board[0][2].winner):
            self.winner = self.board[2][0].winner

    def __str__(self):
        string = ""
        str_map = {0 : "_",X:"X",O:"O"}
        for i in range(9):
            if(i%3==0 and i!=0):
                string += "\n"
            for j in range(9):
                board_pos , mini_pos = self._calc_pos((i,j))
                value = self.board[board_pos[0]][board_pos[1]].board[mini_pos[0]][mini_pos[1]]
                if(j%3==0 and j!=0):
                    string += " "
                string += str_map[value]
            string += "\n"
        return string

    def __repr__(self):
        string = ""
        str_map = {0 : "_",X:"X",O:"O"} 
        for i in range(3):
            for j in range(3):
                string += str_map[self.board[i][j].winner]
            string += "\n"
        return string


class Bot:

    def __init__(self,color):
        self.color = color
        self.opponent = X if color==O else O
        self.board = Board()
        self.bot_depth = 4
        self.sample_size = 10
        self.max_evaluation = 50
        {(i,j):1 for i in range(3) for j in range(3)}
        self.goals_map = {(i,j):1 for i in range(3) for j in range(3)}
        self.threat_map ={(i,j):1 for i in range(3) for j in range(3)}

    def _evaluate_state(self):
        if(self.board.winner == self.color):
            return self.max_evaluation
        elif(self.board.winner == self.opponent):
            return -self.max_evaluation
        count = 0
        for i in range(3):
            for j in range(3):
                if(self.board.board[i][j].winner == self.color):
                    count += self.goals_map[(i,j)]
                elif(self.board.board[i][j].winner == self.opponent):
                    count -= self.threat_map[(i,j)]
        return count

    def _evaluate_goals(self,last_move):
        pos,_ = self.board._calc_pos(last_move)
        mini_board = self.board.board[pos[0]][pos[1]]
        if(mini_board.winner == self.color):
            diags = (((0,0),(1,1),(2,2)),((0,2),(1,1),(2,0)))
            for i in range(3):
                self.goals_map[(pos[0],i)] += 1
                self.goals_map[(i,pos[1])] += 1
            for d in range(2):
                if pos in diags[d]:
                    for i in diags[d]:
                        self.goals_map[i] += 1

    def _evaluate_threats(self,last_move):
        pos,_ = self.board._calc_pos(last_move)
        mini_board = self.board.board[pos[0]][pos[1]]
        if(mini_board.winner == self.opponent):
            diags = (((0,0),(1,1),(2,2)),((0,2),(1,1),(2,0)))
            for i in range(3):
                self.threat_map[(pos[0],i)] += 1
                self.threat_map[(i,pos[1])] += 1
            for d in range(2):
                if pos in diags[d]:
                    for i in diags[d]:
                        self.threat_map[i] += 1


    def opponent_move(self,move):
        self.board.play_move(move,self.opponent)
        self._evaluate_threats(move)

    def get_move(self):
        _ ,move = self.max_move(self.bot_depth)
        self.board.play_move(move,self.color)
        self._evaluate_goals(move)
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
            self.board.undo_move()
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
            self.board.undo_move()
            if(tmp_eval<min_eval[0]):
                min_eval = (tmp_eval,move)
                if(min_eval==-self.max_evaluation):
                    break
        return min_eval


debug = True

if not debug:

    begin = True

    while True:

        op = [int(i) for i in input().split()]

        if(begin):
            begin = False
            if(op[0]==-1):
                bot = Bot(X)
            else:
                bot = Bot(O)
                bot.opponent_move(op)
        else:
            bot.opponent_move(op)

        action_count = int(input())
        valid_moves = []
        for i in range(action_count):
            valid_move = [int(j) for j in input().split()]
            valid_moves.append(valid_move)

        best_move = bot.get_move()

        print("{} {}".format(best_move[0],best_move[1]))