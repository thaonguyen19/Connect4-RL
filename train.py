def main():
	agent = load()
	agent.train()
	agent.save()

if __name__ == "__main__":
	main()