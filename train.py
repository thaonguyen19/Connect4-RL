import os
import pickle

from qlearning_agent import QLearningAgent

NUM_GAMES = 100
FILE = "q_values"

def main():
	agent = QLearningAgent()
	if os.path.isfile(FILE):
		with open(FILE, 'r') as f:
			agent.Q = pickle.load(f)
	for i in range(NUM_GAMES):
		print(i)
		agent.train()
	with open(FILE, 'w') as f:
		agent.save(f)

if __name__ == "__main__":
	main()