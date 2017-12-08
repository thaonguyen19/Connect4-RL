from connect_four import Game, NONE, RED, YELLOW
from mcts_agent import MCTSAgent
from minimax_agent import MinimaxAgent
from qlearning_agent import QLearningAgent
import random

human_involved = False

def play_w_human():
	g = Game()
	# agent = MinimaxAgent() #MCTSAgent()
	agent = QLearningAgent('q_values')
	turn = RED

	while True:
		g.printBoard()
		if turn == RED:
			row = input('{}\'s turn: '.format('Red' if turn == RED else 'Yellow'))
			w = g.insert(int(row), turn)
			agent.play_opponent_move(int(row))
		else:
			move = agent.play_move()
			w = g.insert(move, turn)
		if w:
			print "WINNER: ", w
			break
		turn = YELLOW if turn == RED else RED

def play_wo_human(agent1, agent2, names):
	'''
	Default: agent 1 plays RED
	agent 2 plays YELLOW
	'''
	max_n_moves = []
	results = []
	turn_dict = {1: RED, 2: YELLOW}
	agent_turn_dict = {RED: names[agent1], YELLOW: names[agent2]}

	for i in range(5):
		print "################ Game ", i
		count_moves = 0
		#randomize turn who starts first
		turn_ind = random.randint(1,2)
		g = Game()
		turn = turn_dict[turn_ind]
		print "Starting with turn = ", agent_turn_dict[turn]
		while True:
			g.printBoard()
			if turn == RED:
				print names[agent1], "'s turn"
				move = agent1.play_move()
				print move
				if move is None:
					print "DRAW GAME"
					break
				w = g.insert(move, turn)
				if w:
					results.append(agent_turn_dict[w])
					max_n_moves.append(count_moves)
					print "WINNER: ", agent_turn_dict[w], " TOTAL MOVES: ", count_moves
					break
			else:
				print names[agent2], "'s turn"
				move = agent2.play_move()
				print move
				if move is None:
					print "DRAW GAME"
					break
				w = g.insert(move, turn)
				if w:
					print "WINNER: ", w
					results.append(agent_turn_dict[w])
					max_n_moves.append(count_moves)
					print "WINNER: ", agent_turn_dict[w], " TOTAL MOVES: ", count_moves
					break
			count_moves += 1
			turn = YELLOW if turn == RED else RED

	assert len(results) == len(max_n_moves)
	return results, max_n_moves

if __name__ == "__main__":
	if human_involved:
		play_w_human()
	else:
		agent1 = MCTSAgent()
		agent2 = MinimaxAgent() #assume to take turn YELLOW
		names = {agent1: 'MCTS Agent', agent2: 'Minimax Agent'}
		play_wo_human(agent1, agent2, names)
