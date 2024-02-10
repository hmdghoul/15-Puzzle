import sys
import time
from enum import Enum
from collections import deque

class Action(Enum):
    MOVE_UP = 'Move up'
    MOVE_DOWN = 'Move down'
    MOVE_LEFT = 'Move left'
    MOVE_RIGHT = 'Move right'

class PuzzleState:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.size = len(state)
        self.parent = parent
        self.action = action
        self.empty_position = self.find_empty_position()
    
    def __eq__(self, other):
        if isinstance(other, PuzzleState) and self.state == other.state:
            return True
        return False

    def find_empty_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == '00':
                    return (i, j)

    def possible_actions(self):
        actions = []
        row, col = self.empty_position

        if row > 0:
            actions.append(Action.MOVE_UP)
        if row < self.size - 1:
            actions.append(Action.MOVE_DOWN)
        if col > 0:
            actions.append(Action.MOVE_LEFT)
        if col < self.size - 1:
            actions.append(Action.MOVE_RIGHT)

        return actions

    def perform_action(self, action):
        new_state = [row.copy() for row in self.state]
        row, col = self.empty_position

        if action == Action.MOVE_UP:
            new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
        elif action == Action.MOVE_DOWN:
            new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
        elif action == Action.MOVE_LEFT:
            new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
        elif action == Action.MOVE_RIGHT:
            new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]

        return PuzzleState(new_state, parent=self, action=action)

    def is_goal_state(self, goal_state):
        return self.state == goal_state.state

    def print_state(self):
        for row in self.state:
            print(" ".join(str(cell) for cell in row))

class QueueFrontier:
    def __init__(self):
        self.container = deque()

    def is_empty(self):
        return len(self.container) == 0
    
    def contains_state(self, state):
        return state in self.container

    def add(self, item):
        self.container.append(item)

    def remove(self):
        if not self.is_empty():
            return self.container.popleft()

def parse_state(file_path):
    try:
        with open(file_path, 'r') as file:
            puzzle_state = PuzzleState([line.strip().split() for line in file])
            return puzzle_state
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

def print_solution_path(final_state):
    path = []
    current_state = final_state

    while current_state:
        path.append(current_state)
        current_state = current_state.parent
    
    print("Solution path:")
    for step, state in enumerate(reversed(path)):
        print(f"Step {step}:")
        state.print_state()
        print("-----------")

def solve(initial_state, goal_state, frontier):
    start = time.time()
    explored_states = []
    frontier.add(initial_state)
    while not frontier.is_empty():
        current_state = frontier.remove()
        explored_states.append(current_state)

        if current_state.is_goal_state(goal_state):
            print("Goal state is found")
            print(f"Number of explored states: {len(explored_states)}")
            print(f"Time to find the goal state: {round(time.time() - start, 3)}")
            print_solution_path(current_state)
            break

        actions = current_state.possible_actions()
        for action in actions:
            new_state = current_state.perform_action(action)
            if new_state not in explored_states and not frontier.contains_state(new_state):
                frontier.add(new_state)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <initial_state> <goal_state>")
        sys.exit(1)
    
    initial_state = parse_state(sys.argv[1])
    goal_state = parse_state(sys.argv[2])

    if initial_state and goal_state:
        frontier = QueueFrontier()
        solve(initial_state, goal_state, frontier)