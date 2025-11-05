import heapq
import itertools

class PuzzleState:
    def __init__(self, board, empty_pos, cost=0, moves="", parent=None):
        self.board = board
        self.empty_pos = empty_pos
        self.cost = cost #f(x) = g(x) + h(x)
        self.moves = moves #string which represents the sequence of moves taken to reach the state 
        self.parent = parent #reference to the parent state, used to trace back the solution path
        self.g = len(moves)  #path cost (g(x))

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.board])


def misplaced_tiles_heuristic(board, goal):
    """Heuristic: number of misplaced tiles (excluding the empty space)"""
    return sum(
        1 for i in range(3) for j in range(3) if board[i][j] != 0 and board[i][j] != goal[i][j]
    )


def is_solvable(board):
    """Check if a board configuration is solvable(number of inversions has to be even)"""
    flat_board = list(itertools.chain(*board))
    inversions = sum(
        1 for i in range(len(flat_board)) for j in range(i + 1, len(flat_board))
        if flat_board[i] > flat_board[j] != 0
    )
    return inversions % 2 == 0


def a_star_8_puzzle(start, goal, heuristic_function):
    """Solves the 8-puzzle problem using A* search"""
    if not is_solvable(start): #check if the puzzle is silvable for not entering into an infinite loop
        return "Unsolvable puzzle.", 0, "",0

    goal_positions = {val: (i, j) for i, row in enumerate(goal) for j, val in enumerate(row)}
    start_flat = list(itertools.chain(*start))#we use it to flatten the board
    empty_pos = divmod(start_flat.index(0), 3) #finds the position in the board of the empty space

    heap = []
    visited = set()#we create a set for storing the visited states
    initial = PuzzleState(start, empty_pos, heuristic_function(start, goal), "") #initialize the initial state of the puzzle
    heapq.heappush(heap, (initial.cost, initial))#use heapq to always expand the node with the lowest f(x)

    moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}#different possible moves for the empty space
    states_generated = 0 #initialization of the states generated count

    while heap:
        _, current = heapq.heappop(heap) #extracts the current state with the lowest f(x) from the priority queue
        visited.add(tuple(itertools.chain(*current.board))) #add the current state of the board to the set of visited ones

        #check if the goal state is reached
        if current.board == goal: #if it is true we reconstruct the path of the solution by using the parent pointers
            path = []
            move_sequence = current.moves  #sequence of moves to reach the goal
            while current: #create the solution path 
                path.append(current.board)
                current = current.parent
            
            return list(reversed(path)), states_generated, move_sequence, len(move_sequence) 
            #the path is reversed because when we find the goal state we go back through the parent pointers, so we have to reverse it
            

        for move, (dx, dy) in moves.items(): #for each valid move we are going to create a new board configuration
            x, y = current.empty_pos
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3: #check if the new position of the empty space is inside the board
                new_board = [row[:] for row in current.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                new_flat = tuple(itertools.chain(*new_board)) #flatten the new board

                if new_flat not in visited: #check if we already visit the current state
                    visited.add(new_flat) #we mark the current state as visited
                    h = heuristic_function(new_board, goal)
                    new_cost = current.g + 1 + h  #f(x) = g(x) + h(x)
                    new_state = PuzzleState(
                        new_board, (nx, ny), new_cost, current.moves + move, current
                    )
                    heapq.heappush(heap, (new_cost, new_state)) #as the new state is not visited we push it into the priority queue
                    states_generated += 1 #increment the count for the different states generated

    return "No solution found.", states_generated, "", 0


#start state
start = [
    [3, 1, 2],
    [4, 7, 5],
    [6, 8, 0],
]

#goal state
goal = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
]

#solution for UCS (h=0)
solution_ucs, states_generated_ucs, moves_ucs, move_count_ucs = a_star_8_puzzle(start, goal, lambda x, y: 0)
#printing the start and goal states
print(f"Start state")
for row in start:
        print(" ".join(map(str, row)))
print()
print(f"Goal state")
for row in goal:
        print(" ".join(map(str, row)))
print()

print("UCS Solution:")
if solution_ucs == "No solution found.":
    print(f"No solution found.")
elif solution_ucs == "Unsolvable puzzle.":
    print(f"Unosolvable puzzle")
else:
    for step in solution_ucs:
        print("\n".join(" ".join(map(str, row)) for row in step), "\n")
print(f"States generated: {states_generated_ucs}\n")
print(f"Sequence of moves: {moves_ucs}")
print(f"Number of moves: {move_count_ucs}\n")

#solution using A* algorithm with misplaced tiles heuristic
solution_misplaced, states_generated_misplaced, moves_misplaced, move_count_misplaced = a_star_8_puzzle(start, goal, misplaced_tiles_heuristic)
print("A* with Misplaced Tiles Heuristic Solution:")
if solution_misplaced == "No solution found.":
    print(f"No solution found.")
elif solution_misplaced == "Unsolvable puzzle.":
    print(f"Unosolvable puzzle")
else:
    for step in solution_misplaced:
        print("\n".join(" ".join(map(str, row)) for row in step), "\n")
print(f"States generated: {states_generated_misplaced}")
print(f"Sequence of moves: {moves_misplaced}")
print(f"Number of moves: {move_count_misplaced}")