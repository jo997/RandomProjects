import random
import time

# Tic-Tac-Toe game
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def available_moves(self):
        return [i for i, v in enumerate(self.board) if v == ' ']

    def make_move(self, move):
        if self.board[move] == ' ':
            self.board[move] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def is_winner(self, player):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for line in lines:
            if all(self.board[i] == player for i in line):
                return True
        return False

    def is_draw(self):
        return ' ' not in self.board

    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()

    def print_board(self):
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("--|---|--")
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("--|---|--")
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")


# Genetic Algorithm
class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []

        for _ in range(population_size):
            genes = [random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8']) for _ in range(9)]
            self.population.append({'genes': genes, 'fitness': 0})

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, 7)
        child_genes = parent1['genes'][:crossover_point] + parent2['genes'][crossover_point:]
        return {'genes': child_genes, 'fitness': 0}

    def mutate(self, child_genes):
        for i in range(9):
            if random.random() < self.mutation_rate:
                child_genes[i] = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8'])
        return child_genes

    def calculate_fitness(self, player, opponent):
        return player['fitness'] - opponent['fitness']

    def evolve(self):
        new_population = []

        # Sort population by fitness
        self.population.sort(key=lambda x: x['fitness'], reverse=True)

        # Elitism: Keep the best individual
        new_population.append(self.population[0])

        while len(new_population) < self.population_size:
            parent1 = random.choice(self.population[:5])  # Choose from the top 5 individuals
            parent2 = random.choice(self.population[:5])

            child = self.crossover(parent1, parent2)
            child['genes'] = self.mutate(child['genes'])
            new_population.append(child)

        self.population = new_population


# Visualization
def visualize_game(game):
    print("\nCurrent Board:")
    game.print_board()


# Function for human player to make a move
def human_player_move(game):
    print("Enter your move (0-8): ")
    move = int(input())
    if move not in game.available_moves():
        print("Invalid move. Please try again.")
        human_player_move(game)
    else:
        game.make_move(move)


def evaluate_agent_against_human(agent, generations, game):
    for generation in range(generations):
        for individual in agent.population:
            game = TicTacToe()
            for move in individual['genes']:
                game.make_move(int(move))
                if game.is_game_over():
                    break

            if game.is_winner('X'):
                individual['fitness'] += 1
            elif game.is_draw():
                individual['fitness'] += 0.5

        agent.evolve()
        print(f"\nGeneration {generation + 1} complete.\n")

    best_agent = max(agent.population, key=lambda x: x['fitness'])
    return best_agent


def main():
    population_size = 50
    mutation_rate = 0.5
    generations = 25

    algorithm = GeneticAlgorithm(population_size, mutation_rate)

    # Training the agent
    for generation in range(generations):
        for individual in algorithm.population:
            game = TicTacToe()
            for move in individual['genes']:
                game.make_move(int(move))
                if game.is_game_over():
                    break

            if game.is_winner('X'):
                individual['fitness'] += 1
            elif game.is_draw():
                individual['fitness'] += 0.5

            visualize_game(game)
            time.sleep(0.01)

        algorithm.evolve()
        print(f"\nGeneration {generation + 1} complete.\n")

    # Evaluate agent against human player
    best_agent = evaluate_agent_against_human(algorithm, generations, TicTacToe())

    # Play against the best agent
    while True:
        game = TicTacToe()
        visualize_game(game)
        while not game.is_game_over():
            human_player_move(game)
            if game.is_game_over():
                break
            agent_move = int(best_agent['genes'].pop(0))
            game.make_move(agent_move)
            visualize_game(game)
        if game.is_winner('X'):
            print("You win!")
        elif game.is_winner('O'):
            print("Agent wins!")
        else:
            print("It's a draw!")

        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
