from connect_four import Game, NONE, RED, YELLOW
from mcts_agent import MCTSAgent
from minimax_agent import MinimaxAgent
from qlearning_agent import QLearningAgent
import random
import numpy as np
import collections

human_involved = True

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

def play_wo_human(agent1, agent2):
	'''
	Default: agent 1 plays RED
	agent 2 plays YELLOW
	'''
	turn_dict = {1: RED, 2: YELLOW}
	agent_turn_dict = {RED: agent1.name, YELLOW: agent2.name}

	count_moves = 0
	winner = None

	g = Game()

	#randomize turn who starts first
	turn_ind = random.randint(1,2)
	turn = turn_dict[turn_ind]

	turn = turn_dict[1]

	print "Starting with turn = ", agent_turn_dict[turn]
	while True:
		g.printBoard()
		if turn == RED:
			print agent1.name, "'s turn"
			move = agent1.play_move()
			print move
			if move is None:
				print "DRAW GAME"
				break
			w = g.insert(move, turn)
			if w:
				winner = agent_turn_dict[w]
				print "####################WINNER: ", winner, " TOTAL MOVES: ", count_moves
				break
			agent2.play_opponent_move(move)
		else:
			print agent2.name, "'s turn"
			move = agent2.play_move()
			print move
			if move is None:
				print "DRAW GAME"
				break
			w = g.insert(move, turn)
			if w:
				winner = agent_turn_dict[w]
				print "#################WINNER: ", winner, " TOTAL MOVES: ", count_moves
				break
			agent1.play_opponent_move(move)
		count_moves += 1
		turn = YELLOW if turn == RED else RED
	return winner, count_moves


# if __name__ == "__main__":
# 	if human_involved:
# 		play_w_human()
# 	else:
# 		results = collections.defaultdict(list)
# 		for i in range(10):
# 			print "################ Game ", i
# 			agent1 = MCTSAgent()
# 			agent2 = MinimaxAgent() #assume to take turn YELLOW
# 			winner, count_moves = play_wo_human(agent1, agent2)
# 			if winner:
# 				results[winner].append(count_moves)

# 		print results
# 		print "TOTAL GAMES WON BY MCTS: ", len(results['MCTSAgent'])
# 		print "AVERAGE NO. MOVES: ", sum(results['MCTSAgent'])/ len(results['MCTSAgent'])
# 		print "TOTAL GAMES WON BY Minimax: ", len(results['MinimaxAgent'])
# 		print "AVERAGE NO. MOVES: ", sum(results['MinimaxAgent'])/ len(results['MinimaxAgent'])

