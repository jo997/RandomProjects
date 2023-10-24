import tkinter as tk
import random
import queue
import heapq
from collections import defaultdict

# Constants
ROWS, COLS = 10, 10

# Function to generate a random maze with a guaranteed path
def generate_maze():
    global running_algorithm
    running_algorithm = False
    
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.25:
                button_grid[i][j]["bg"] = "black"
            else:
                button_grid[i][j]["bg"] = "white"

    # Ensure there is a free start and goal
    button_grid[0][0]["bg"] = "white"
    button_grid[ROWS-1][COLS-1]["bg"] = "white"

# Function to clear the grid
def clear_grid():
    global running_algorithm
    running_algorithm = False
    
    for i in range(ROWS):
        for j in range(COLS):
            button_grid[i][j]["bg"] = "white"

# Function for Depth-First Search
def dfs():
    global running_algorithm
    running_algorithm = True
    
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    path = []

    def dfs_helper(x, y):
        global running_algorithm
        
        if not running_algorithm:
            return False
        
        if x < 0 or x >= ROWS or y < 0 or y >= COLS or visited[x][y] or button_grid[x][y]["bg"] == "black":
            return False
        visited[x][y] = True
        path.append((x, y))
        button_grid[x][y]["bg"] = "green"
        root.update()
        root.after(100)  # Pause for 100 milliseconds 
        if x == ROWS - 1 and y == COLS - 1:
            return True  # Reached the goal
        if (dfs_helper(x + 1, y) or dfs_helper(x - 1, y) or dfs_helper(x, y + 1) or dfs_helper(x, y - 1)):
            return True  # Found a path
        path.pop()
        return False

    dfs_helper(0, 0)

    if not running_algorithm and (ROWS-1, COLS-1) not in path:
        for x, y in path:
            button_grid[x][y]["bg"] = "white"
            visited[x][y] = False

# Function for Breadth-First Search
def bfs():
    global running_algorithm
    running_algorithm = True
    
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    queue = [(0, 0)]

    while queue:
        if not running_algorithm:
            return
        
        x, y = queue.pop(0)
        if x < 0 or x >= ROWS or y < 0 or y >= COLS or visited[x][y] or button_grid[x][y]["bg"] == "black":
            continue
        visited[x][y] = True
        button_grid[x][y]["bg"] = "green"
        root.update()
        root.after(100)  # Pause for 100 milliseconds 
        if x == ROWS - 1 and y == COLS - 1:
            return True  # Reached the goal
        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))

# Function for A*
def astar():
    global running_algorithm
    running_algorithm = True
    
    def heuristic(node):
        return abs(node[0] - ROWS + 1) + abs(node[1] - COLS + 1)

    open_list = [(heuristic((0, 0)), 0, (0, 0), [(0, 0)])]
    closed_list = set()

    while open_list:
        if not running_algorithm:
            return

        _, cost, current, path = heapq.heappop(open_list)
        if current == (ROWS - 1, COLS - 1):
            for step in path:
                button_grid[step[0]][step[1]]["bg"] = "green"
                root.update()
                root.after(100)  # Pause for 100 milliseconds
            return

        closed_list.add(current)

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < ROWS and 0 <= ny < COLS and button_grid[nx][ny]["bg"] != "black" and (nx, ny) not in closed_list]

        for n in valid_neighbors:
            new_cost = cost + 1
            heapq.heappush(open_list, (new_cost + heuristic(n), new_cost, n, path + [n]))

# Function for Dijkstra's Algorithm
def dijkstra():
    pass
"""
    global running_algorithm
    running_algorithm = True
    
    def heuristic(node):
        return abs(node[0] - ROWS + 1) + abs(node[1] - COLS + 1)

    dist = {(i, j): float('inf') for i in range(ROWS) for j in range(COLS)}
    dist[(0, 0)] = 0

    while open_list:
        if not running_algorithm:
            return

        current = min((dist[node], node) for node in dist if node not in closed_set)[1]
        
        if current == (ROWS - 1, COLS - 1):
            x, y = current
            while (x, y) != (0, 0):
                button_grid[x][y]["bg"] = "green"
                x, y = came_from[(x, y)]
            root.update()
            return

        closed_set.add(current)

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < ROWS and 0 <= ny < COLS and button_grid[nx][ny]["bg"] != "black"]

        for n in valid_neighbors:
            new_cost = dist[current] + 1
            if new_cost < dist[n]:
                dist[n] = new_cost
                came_from[n] = current

                button_grid[n[0]][n[1]]["bg"] = "green"
                root.update()
                root.after(100)  # Pause for 100 milliseconds
"""
def greedy_best_first():
    global running_algorithm
    running_algorithm = True
    
    def heuristic(node):
        goal = (ROWS - 1, COLS - 1)
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    current = (0, 0)

    while True:
        if not running_algorithm:
            return

        if current == (ROWS - 1, COLS - 1):
            button_grid[current[0]][current[1]]["bg"] = "green"
            root.update()
            return

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < ROWS and 0 <= ny < COLS and button_grid[nx][ny]["bg"] != "black"]

        if not valid_neighbors:
            return

        next_node = min(valid_neighbors, key=heuristic)
        button_grid[next_node[0]][next_node[1]]["bg"] = "green"
        root.update()
        root.after(100)  # Pause for 100 milliseconds
        current = next_node

def jump_point_search():
    pass
    """global running_algorithm
    running_algorithm = True
    
    def heuristic(node):
        return abs(node[0] - ROWS + 1) + abs(node[1] - COLS + 1)

    def valid_successors(node, parent):
        x, y = node
        px, py = parent

        dx, dy = x - px, y - py

        if dx != 0 and dy != 0:
            return [(x, y)]
        
        successors = []

        if dx != 0:
            if button_grid[x][y-1]["bg"] != "black":
                successors.append((x, y-1))
            if button_grid[x][y+1]["bg"] != "black":
                successors.append((x, y+1))
            if button_grid[x+dx][y]["bg"] != "black":
                successors.append((x+dx, y-1))
            if button_grid[x+dx][y]["bg"] != "black":
                successors.append((x+dx, y+1))
        else:
            if button_grid[x-1][y]["bg"] != "black":
                successors.append((x-1, y))
            if button_grid[x+1][y]["bg"] != "black":
                successors.append((x+1, y))
            if button_grid[x][y+dy]["bg"] != "black":
                successors.append((x-1, y+dy))
            if button_grid[x][y+dy]["bg"] != "black":
                successors.append((x+1, y+dy))

        return successors

    def jump(node, parent):
        visited.add(node)
        x, y = node

        while True:
            if not (0 <= x < ROWS and 0 <= y < COLS) or button_grid[x][y]["bg"] == "black":
                return None

            if node == (ROWS - 1, COLS - 1):
                return node

            dx, dy = x - parent[0], y - parent[1]

            if dx != 0 and dy != 0:
                if jump((x+dx, y), node) or jump((x, y+dy), node):
                    return node
            else:
                for s in valid_successors(node, parent):
                    if s not in visited:
                        jump_node = jump(s, node)
                        if jump_node:
                            return node
                        visited.add(s)
                return None

    open_list = [(heuristic((0, 0)), 0, (0, 0), [(0, 0)])]
    closed_list = set()
    visited = set()

    while open_list:
        if not running_algorithm:
            return

        _, cost, current, path = heapq.heappop(open_list)
        if current == (ROWS - 1, COLS - 1):
            for step in path:
                button_grid[step[0]][step[1]]["bg"] = "green"
                root.update()
                root.after(100)  # Pause for 100 milliseconds
            return

        closed_list.add(current)

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < ROWS and 0 <= ny < COLS and button_grid[nx][ny]["bg"] != "black" and (nx, ny) not in closed_list]

        for n in valid_neighbors:
            new_cost = cost + 1
            jump_node = jump(n, current)
            if jump_node:
                heapq.heappush(open_list, (new_cost + heuristic(n), new_cost, jump_node, path + [jump_node]))
"""

# Function to generate initial population
def generate_population(population_size):
    population = []
    for _ in range(population_size):
        individual = [(0, 0)]  # Start at the top-left corner
        for _ in range(ROWS*COLS):
            next_move = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            new_position = (max(0, min(individual[-1][0] + next_move[0], ROWS-1)),
                            max(0, min(individual[-1][1] + next_move[1], COLS-1)))
            individual.append(new_position)
        population.append(individual)
    return population

# Function to evaluate fitness (lower value is better)
def fitness(individual):
    # Initialize variables to track the position and steps
    position = (0, 0)
    steps = 0

    # Traverse the path and calculate fitness
    for move in individual:
        steps += 1
        new_position = (max(0, min(position[0] + move[0], ROWS-1)),
                        max(0, min(position[1] + move[1], COLS-1)))

        # Check if the new position is a valid move
        if button_grid[new_position[0]][new_position[1]]["bg"] == "black":
            break

        position = new_position

    # Calculate fitness score (lower values are better)
    fitness_score = steps

    return fitness_score

# Function to select parents for reproduction
def selection(population, num_parents):
    parents = []
    for _ in range(num_parents):
        parent = random.choice(population)
        parents.append(parent)
    return parents

# Function to perform crossover
def crossover(parents):
    child = []
    for i in range(len(parents[0])):
        if random.random() < 0.7:
            child.append(parents[0][i])
        else:
            child.append(parents[1][i])
    return child

# Function to perform mutation
def mutation(child):
    for i in range(1, len(child)-1):  # Avoid modifying start and end positions
        if random.random() < 0.7:  # Adjust mutation rate as needed
            next_move = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            new_position = (max(0, min(child[i-1][0] + next_move[0], ROWS-1)),
                            max(0, min(child[i-1][1] + next_move[1], COLS-1)))
            child[i] = new_position
    return child


def mutate_and_start_new_generation():
    global running_algorithm
    running_algorithm = True

    # Perform mutation
    parents = selection(population, 2)
    child = crossover(parents)
    child = mutation(child)

    population.append(child)

    # Update generation label
    generation_label.config(text=f"Generation: {generation}")

    # Schedule the next mutation and new generation after 10 seconds
    root.after(10000, mutate_and_start_new_generation)

# Function to run the genetic algorithm
def genetic_algorithm():
    global running_algorithm
    running_algorithm = True

    population_size = 500
    num_generations = 500

    population = generate_population(population_size)

    for generation in range(num_generations):
        if not running_algorithm:
            return

        for individual in population:
            for position in individual:
                button_grid[position[0]][position[1]]["bg"] = "white"

            for position in individual:
                button_grid[position[0]][position[1]]["bg"] = "green"
                root.update()
                root.after(100)  # Pause for 100 milliseconds

            fitness_score = fitness(individual)
            if fitness_score == 0:
                return

        parents = selection(population, 2)
        child = crossover(parents)
        child = mutation(child)

        population.append(child)
        
        # Update generation label
        generation_label.config(text=f"Generation: {generation}")
        population = generate_population(population_size)
        mutate_and_start_new_generation()  # Start the mutation process


# Create main window
root = tk.Tk()
root.title("Maze Solver")


# Create grid of buttons
button_grid = [[tk.Button(root, width=2, height=1, bg="white") for _ in range(COLS)] for _ in range(ROWS)]

# Place buttons in the grid
for i in range(ROWS):
    for j in range(COLS):
        button_grid[i][j].grid(row=i, column=j)

# Generate maze button
generate_maze_button = tk.Button(root, text="Generate Maze", command=generate_maze)
generate_maze_button.grid(row=ROWS+1, column=0, columnspan=COLS)

# DFS button
dfs_button = tk.Button(root, text="DFS", command=dfs)
dfs_button.grid(row=ROWS+2, column=0, columnspan=COLS)

# BFS button
bfs_button = tk.Button(root, text="BFS", command=bfs)
bfs_button.grid(row=ROWS+3, column=0, columnspan=COLS)

# A* button
astar_button = tk.Button(root, text="A*", command=astar)
astar_button.grid(row=ROWS+4, column=0, columnspan=COLS)

# Dijkstra's button
dijkstra_button = tk.Button(root, text="Dijkstra's", command=dijkstra)
dijkstra_button.grid(row=ROWS+5, column=0, columnspan=COLS)

# Greedy Best-First button
greedy_best_first_button = tk.Button(root, text="Greedy Best-First", command=greedy_best_first)
greedy_best_first_button.grid(row=ROWS+6, column=0, columnspan=COLS)

# Jump Point Search button (placeholder)
jps_button = tk.Button(root, text="Jump Point Search", command=jump_point_search)
jps_button.grid(row=ROWS+7, column=0, columnspan=COLS)

# Genetic Algorithm button
genetic_algorithm_button = tk.Button(root, text="Genetic Algorithm", command=genetic_algorithm)
genetic_algorithm_button.grid(row=ROWS+9, column=0, columnspan=COLS)

# Generation
generation_label = tk.Label(root, text="Generation: 0")
generation_label.grid(row=ROWS+11, column=0, columnspan=COLS)

# Reset button
reset_button = tk.Button(root, text="Reset", command=clear_grid)
reset_button.grid(row=ROWS+10, column=0, columnspan=COLS)

# Global flag for running algorithm
running_algorithm = False

# Run the GUI event loop
root.mainloop()
