from flask import Flask, render_template, jsonify, request
from queue import PriorityQueue
import time
import random

app = Flask(__name__)

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = self.calculate_manhattan() + depth * 0.4

    def calculate_manhattan(self):
        GRID_SIZE = 6
        distance = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                if value != 0:
                    x_goal = (value - 1) // GRID_SIZE
                    y_goal = (value - 1) % GRID_SIZE
                    distance += abs(x_goal - i) + abs(y_goal - j)
        return distance

    def __lt__(self, other):
        return self.cost < other.cost

def create_solvable_puzzle():
    GRID_SIZE = 6
    # Tạo trạng thái đích
    board = [[i + j*GRID_SIZE + 1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    board[-1][-1] = 0

    # Thực hiện các bước di chuyển ngẫu nhiên hợp lệ
    moves = 30  # Giảm số bước để puzzle dễ giải hơn
    last_move = None
    
    for _ in range(moves):
        blank_i, blank_j = get_blank_pos(board)
        possible_moves = []
        
        # Kiểm tra 4 hướng di chuyển
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                # Tránh di chuyển ngược lại
                if last_move and (di, dj) != (-last_move[0], -last_move[1]):
                    possible_moves.append((di, dj))
                elif not last_move:
                    possible_moves.append((di, dj))
        
        if possible_moves:
            move = random.choice(possible_moves)
            new_i, new_j = blank_i + move[0], blank_j + move[1]
            # Thực hiện di chuyển
            board[blank_i][blank_j], board[new_i][new_j] = board[new_i][new_j], board[blank_i][blank_j]
            last_move = move
    
    return board

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-puzzle', methods=['GET'])
def new_puzzle():
    puzzle = create_solvable_puzzle()
    return jsonify({'puzzle': puzzle})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    board = data['board']
    start_time = time.time()
    solution = solve_astar(board)
    solve_time = time.time() - start_time
    return jsonify({
        'solution': solution,
        'solve_time': round(solve_time, 2),
        'steps': len(solution) if solution else 0
    })

def solve_astar(board):
    GRID_SIZE = 6
    initial = PuzzleState(board)
    goal_state = [[i + j*GRID_SIZE + 1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    goal_state[-1][-1] = 0

    open_list = PriorityQueue()
    open_list.put(initial)
    closed_set = set()
    max_iterations = 7000
    
    # Thêm dictionary để theo dõi chi phí tốt nhất cho mỗi trạng thái
    best_costs = {tuple(map(tuple, board)): initial.cost}

    iterations = 0
    while not open_list.empty() and iterations < max_iterations:
        iterations += 1
        current = open_list.get()

        if current.board == goal_state:
            path = []
            while current:
                path.append(current.board)
                current = current.parent
            return path[::-1]

        board_tuple = tuple(map(tuple, current.board))
        if board_tuple in closed_set:
            continue

        closed_set.add(board_tuple)
        blank_i, blank_j = get_blank_pos(current.board)

        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                new_board = [row[:] for row in current.board]
                new_board[blank_i][blank_j], new_board[new_i][new_j] = \
                    new_board[new_i][new_j], new_board[blank_i][blank_j]
                
                new_state = PuzzleState(new_board, current, (di, dj), current.depth + 1)
                board_tuple = tuple(map(tuple, new_board))
                
                # Chỉ thêm vào open_list nếu đây là đường đi tốt hơn
                if board_tuple not in best_costs or new_state.cost < best_costs[board_tuple]:
                    best_costs[board_tuple] = new_state.cost
                    open_list.put(new_state)

    return None

def get_blank_pos(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/check-solvable', methods=['POST'])
def check_solvable():
    data = request.get_json()
    board = data['board']
    # Kiểm tra xem puzzle có thể giải được không
    solution = solve_astar(board)
    return jsonify({
        'solvable': solution is not None
    })

if __name__ == '__main__':
    app.run(debug=False)
