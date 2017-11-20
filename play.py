from connect_four import Game, NONE, RED, YELLOW
from mcts_agent import MCTSAgent

g = Game()
agent = MCTSAgent()
turn = RED
while True:
	g.printBoard()
	if turn == RED:
		row = input('{}\'s turn: '.format('Red' if turn == RED else 'Yellow'))
		g.insert(int(row), turn)
		agent.play_opponent_move(int(row))
	else:
		move = agent.play_move()
		g.insert(move, turn)
	turn = YELLOW if turn == RED else RED