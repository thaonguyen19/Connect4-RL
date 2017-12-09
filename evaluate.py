from connect_four import Game, NONE, RED, YELLOW
from play import play_wo_human
from naive_agent import NaiveAgent
from minimax_agent import MinimaxAgent
from mcts_agent import MCTSAgent
from qlearning_agent import QLearningAgent
import collections
import copy

def test_agents(agent1, agent2, n_trials=200):
	print "################################################################"
	results = collections.defaultdict(list)
	times = collections.defaultdict(list)
	for i in range(n_trials):
		print "########## Game ", i
		a1 = copy.deepcopy(agent1)
		a2 = copy.deepcopy(agent2)
		if i < n_trials/2:
			winner, count_moves, trial_times = play_wo_human(a1, a2, 1)
		else:
			winner, count_moves, trial_times = play_wo_human(a1, a2, 2)
		if winner:
			results[winner].append(count_moves)
			times[a1.name].append(trial_times[a1.name])
			times[a2.name].append(trial_times[a2.name])

	total_moves = sum(results[a1.name]) + sum(results[a2.name])
	print results
	print "TOTAL GAMES WON BY ", a1.name, ": ", len(results[a1.name])
	if len(results[a1.name]) != 0:
		print "AVERAGE NO. MOVES: ", sum(results[a1.name]) / len(results[a1.name])
	print "AVERAGE TIME PER MOVE: ", sum(times[a1.name]) / total_moves
	print "TOTAL GAMES WON BY ", a2.name, ": ", len(results[a2.name])
	if len(results[a2.name]) != 0:
		print "AVERAGE NO. MOVES: ", sum(results[a2.name])/ len(results[a2.name])
	print "AVERAGE TIME PER MOVE: ", sum(times[a2.name]) / total_moves
	print "################################################################"


if __name__ == "__main__":
	# test_agents(NaiveAgent(), MCTSAgent())
	# test_agents(NaiveAgent(), QLearningAgent())
	# test_agents(MCTSAgent(), MinimaxAgent(depth=3))
	# test_agents(QLearningAgent("q_values"), MinimaxAgent(depth=3))
	test_agents(MCTSAgent(), QLearningAgent("q_values"))
