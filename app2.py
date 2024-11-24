import pygame
import random
from queue import PriorityQueue

# Khởi tạo pygame
pygame.init()

# Cấu hình game
GRID_SIZE = 6  # Bảng 6x6
WINDOW_SIZE = 750  # Tăng kích thước cửa sổ
TILE_SIZE = WINDOW_SIZE // GRID_SIZE
FPS = 60

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 123, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = self.calculate_manhattan() + depth * 0.4  # Giảm trọng số độ sâu

    def calculate_manhattan(self):
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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("35-Puzzle Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)  # Điều chỉnh kích thước font
        self.moves_count = 0
        self.auto_solving = False
        self.solution = None
        self.solution_index = 0
        self.solving_failed = False  # Thêm biến để theo dõi trạng thái giải
        self.reset_game()

    def reset_game(self):
        self.current_state = self.create_solvable_puzzle()
        self.moves_count = 0
        self.auto_solving = False
        self.solution = None
        self.solution_index = 0
        self.solving_failed = False

    def create_solvable_puzzle(self):
        """Tạo puzzle có thể giải được"""
        goal_state = [[i + j*GRID_SIZE + 1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        goal_state[-1][-1] = 0
        
        current_state = [row[:] for row in goal_state]
        # Giảm số bước xáo trộn để dễ giải hơn
        for _ in range(25):  
            blank_i, blank_j = self.get_blank_pos_from_state(current_state)
            possible_moves = []
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                    possible_moves.append((di, dj))
            if possible_moves:
                di, dj = random.choice(possible_moves)
                new_i, new_j = blank_i + di, blank_j + dj
                current_state[blank_i][blank_j], current_state[new_i][new_j] = \
                    current_state[new_i][new_j], current_state[blank_i][blank_j]
        return current_state

    def get_blank_pos_from_state(self, state):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if state[i][j] == 0:
                    return i, j
        return None

    def get_blank_pos(self):
        return self.get_blank_pos_from_state(self.current_state)

    def move(self, direction):
        blank_i, blank_j = self.get_blank_pos()
        new_i, new_j = blank_i + direction[0], blank_j + direction[1]

        if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
            self.current_state[blank_i][blank_j], self.current_state[new_i][new_j] = \
                self.current_state[new_i][new_j], self.current_state[blank_i][blank_j]
            self.moves_count += 1
            self.solving_failed = False  # Reset trạng thái khi người chơi di chuyển
            return True
        return False

    def is_solved(self):
        numbers = list(range(1, GRID_SIZE * GRID_SIZE))
        numbers.append(0)
        goal = [numbers[i:i+GRID_SIZE] for i in range(0, GRID_SIZE * GRID_SIZE, GRID_SIZE)]
        return self.current_state == goal

    def solve_astar(self):
        initial = PuzzleState([row[:] for row in self.current_state])
        goal_state = [[i + j*GRID_SIZE + 1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        goal_state[-1][-1] = 0

        open_list = PriorityQueue()
        open_list.put(initial)
        closed_set = set()
        max_iterations = 7000  # Tăng giới hạn lặp

        iterations = 0
        while not open_list.empty() and iterations < max_iterations:
            iterations += 1
            current = open_list.get()

            if current.board == goal_state:
                path = []
                while current:
                    path.append(current.board)
                    current = current.parent
                self.solution = path[::-1]
                return True

            board_tuple = tuple(map(tuple, current.board))
            if board_tuple in closed_set:
                continue

            closed_set.add(board_tuple)
            blank_i, blank_j = self.get_blank_pos_from_state(current.board)

            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                    new_board = [row[:] for row in current.board]
                    new_board[blank_i][blank_j], new_board[new_i][new_j] = \
                        new_board[new_i][new_j], new_board[blank_i][blank_j]
                    
                    new_state = PuzzleState(new_board, current, (di, dj), current.depth + 1)
                    board_tuple = tuple(map(tuple, new_board))
                    
                    if board_tuple not in closed_set:
                        open_list.put(new_state)

        self.solving_failed = True  # Đánh dấu khi không tìm được giải pháp
        return False

    def draw_board(self):
        self.screen.fill(WHITE)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.current_state[i][j]
                if value != 0:
                    pygame.draw.rect(self.screen, BLUE,
                                   (j * TILE_SIZE, i * TILE_SIZE,
                                    TILE_SIZE - 2, TILE_SIZE - 2))
                    text = self.font.render(str(value), True, WHITE)
                    text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2,
                                                    i * TILE_SIZE + TILE_SIZE // 2))
                    self.screen.blit(text, text_rect)

        # Hiển thị thông báo
        if self.is_solved():
            win_text = self.font.render('WIN!', True, GREEN)
            text_rect = win_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            self.screen.blit(win_text, text_rect)
        elif self.solving_failed:
            fail_text = self.font.render('Try Again (R)', True, RED)
            text_rect = fail_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            self.screen.blit(fail_text, text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_SPACE and not self.auto_solving:
                        self.auto_solving = True
                        if self.solve_astar():
                            self.solution_index = 0
                        else:
                            self.auto_solving = False
                    elif not self.auto_solving:
                        if event.key == pygame.K_LEFT:
                            self.move((0, 1))
                        elif event.key == pygame.K_RIGHT:
                            self.move((0, -1))
                        elif event.key == pygame.K_UP:
                            self.move((1, 0))
                        elif event.key == pygame.K_DOWN:
                            self.move((-1, 0))

            if self.auto_solving and self.solution:
                if self.solution_index < len(self.solution):
                    self.current_state = [row[:] for row in self.solution[self.solution_index]]
                    self.solution_index += 1
                else:
                    self.auto_solving = False

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
