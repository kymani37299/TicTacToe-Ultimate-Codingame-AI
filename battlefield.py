from full_minimax import Bot as Bot1 , Board
from random import shuffle,choice

class RandomBot(Bot1):
	def get_move(self):
		move = choice(self.board.get_legal_moves())
		self.board.play_move(move,self.color)
		return move

X = 1
O = 2

def play_game(p1,p2):
	# Preparation
	board = Board()
	p1.color = X
	p1.opponent = O
	p1.board = Board()
	p2.color = X
	p2.opponent = O
	p2.board = Board()
	curr_player = p1
	while not board.winner and board.get_legal_moves():
		if(board.move_history):
			curr_player.opponent_move(board.move_history[-1])
		board.play_move(curr_player.get_move(),curr_player.color)
		curr_player = p1 if curr_player==p2 else p2
	return board.winner

def contest(bot1,bot2,rounds):
	bots = [[bot1[0],bot1[1],0],[bot2[0],bot2[1],0]]
	for i in range(rounds):
		shuffle(bots)
		winner = play_game(bots[0][0],bots[1][0])
		if(winner!=0):
			bots[winner-1][2] += 1
			

	print("Score( {} - {} ): {} - {} , {} ties".format(bots[0][1],bots[1][1],bots[0][2],bots[1][2],rounds-bots[0][2]-bots[1][2]))

b1 = (Bot1(X),"New bot")
b2 = (RandomBot(O),"RandomBot")
contest(b1,b2,100)