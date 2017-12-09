from connect_four import Game, NONE, RED, YELLOW
from play import play_wo_human
from naive_agent import NaiveAgent
from minimax_agent import MinimaxAgent
from mcts_agent import MCTSAgent
from qlearning_agent import QLearningAgent
import collections
import copy

def test_agents(agent1, agent2, n_trials=100):
	results = collections.defaultdict(list)
	for i in range(n_trials):
		print "################ Game ", i
		a1 = copy.deepcopy(agent1)
		a2 = copy.deepcopy(agent2)
		if i < n_trials/2:
			winner, count_moves = play_wo_human(a1, a2)
		else:
			winner, count_moves = play_wo_human(a2, a1)
		if winner:
			results[winner].append(count_moves)

	print results
	print "TOTAL GAMES WON BY ", a1.name, ": ", len(results[a1.name])
	if len(results[a1.name]) != 0:
		print "AVERAGE NO. MOVES: ", sum(results[a1.name]) / len(results[a1.name])
	print "TOTAL GAMES WON BY ", a2.name, ": ", len(results[a2.name])
	if len(results[a2.name]) != 0:
		print "AVERAGE NO. MOVES: ", sum(results[a2.name])/ len(results[a2.name])


if __name__ == "__main__":
	test_agents(NaiveAgent(), MCTSAgent())
	test_agents(MinimaxAgent(depth=2), MCTSAgent())
	test_agents(MinimaxAgent(depth=2), QLearningAgent("q_values"))
	test_agents(MCTSAgent(), QLearningAgent("q_values"))