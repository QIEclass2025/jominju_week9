
import pygame
import sys
import json
import urllib.request

# --- 상수 정의 ---
SCREEN_WIDTH = 760
SCREEN_HEIGHT = 760
BOARD_SIZE = 18
CELL_SIZE = SCREEN_WIDTH // (BOARD_SIZE + 2)
BOARD_OFFSET = CELL_SIZE

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (205, 133, 63)
BUTTON_BG = (220, 220, 220)
GAMEOVER_BG = (60, 70, 90)
SHADOW = (100, 100, 100)
HIGHLIGHT = (230, 230, 230)

# --- API 및 명언 관련 함수 ---
def get_advice():
    try:
        with urllib.request.urlopen("https://api.adviceslip.com/advice", timeout=5) as url:
            data = json.loads(url.read().decode())
            return data['slip']['advice']
    except Exception:
        return "Play your best move."

# --- 게임 초기화 ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("오목 게임")

try:
    advice_font = pygame.font.SysFont('malgungothic', 16)
    korean_font = pygame.font.SysFont('malgungothic', 18)
except pygame.error:
    advice_font = pygame.font.Font(None, 18)
    korean_font = pygame.font.Font(None, 20)

font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)

# --- 게임 변수 및 명언 ---
advice_text = get_advice()
board = [[0 for _ in range(BOARD_SIZE + 1)] for _ in range(BOARD_SIZE + 1)]
turn = "black"
game_over = False
winner = None
restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)

# --- 그리기 및 게임 로직 함수 ---
def reset_game():
    global board, turn, game_over, winner, advice_text
    board = [[0 for _ in range(BOARD_SIZE + 1)] for _ in range(BOARD_SIZE + 1)]
    turn = "black"
    game_over = False
    winner = None
    advice_text = get_advice()

def draw_text_wrapped(surface, text, font, color, rect):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y = rect.top
    for line in lines:
        line_surface = font.render(line.strip(), True, color)
        # 각 줄을 가운데 정렬하기 위한 코드
        line_rect = line_surface.get_rect(centerx=rect.centerx, top=y)
        surface.blit(line_surface, line_rect)
        y += font.get_height()

def draw_grid():
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET, BOARD_OFFSET + i * CELL_SIZE), (SCREEN_WIDTH - BOARD_OFFSET, BOARD_OFFSET + i * CELL_SIZE), 1)
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET + i * CELL_SIZE, BOARD_OFFSET), (BOARD_OFFSET + i * CELL_SIZE, SCREEN_HEIGHT - BOARD_OFFSET), 1)
    
    star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
    for r, c in star_points:
        pygame.draw.circle(screen, BLACK, (BOARD_OFFSET + c * CELL_SIZE, BOARD_OFFSET + r * CELL_SIZE), 5)

def draw_stones():
    for r in range(BOARD_SIZE + 1):
        for c in range(BOARD_SIZE + 1):
            if board[r][c] != 0:
                center_pos = (BOARD_OFFSET + c * CELL_SIZE, BOARD_OFFSET + r * CELL_SIZE)
                radius = CELL_SIZE // 2 - 2
                shadow_pos = (center_pos[0] + 2, center_pos[1] + 2)
                pygame.draw.circle(screen, SHADOW, shadow_pos, radius)
                stone_color = BLACK if board[r][c] == 1 else WHITE
                pygame.draw.circle(screen, stone_color, center_pos, radius)

def check_win(row, col):
    stone_color = board[row][col]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 5): 
            r, c = row + dr*i, col + dc*i
            if 0 <= r <= BOARD_SIZE and 0 <= c <= BOARD_SIZE and board[r][c] == stone_color: count += 1
            else: break
        for i in range(1, 5):
            r, c = row - dr*i, col - dc*i
            if 0 <= r <= BOARD_SIZE and 0 <= c <= BOARD_SIZE and board[r][c] == stone_color: count += 1
            else: break
        if count >= 5: return True
    return False

def display_end_game_elements(winner_color):
    message = f"{winner_color.upper()} WINS!"
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(text, text_rect)
    
    pygame.draw.line(screen, HIGHLIGHT, restart_button_rect.topleft, restart_button_rect.topright, 2)
    pygame.draw.line(screen, HIGHLIGHT, restart_button_rect.topleft, restart_button_rect.bottomleft, 2)
    pygame.draw.line(screen, SHADOW, restart_button_rect.bottomleft, restart_button_rect.bottomright, 2)
    pygame.draw.line(screen, SHADOW, restart_button_rect.topright, restart_button_rect.bottomright, 2)
    pygame.draw.rect(screen, BUTTON_BG, restart_button_rect.inflate(-4, -4))
    restart_text = button_font.render("Restart", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)

    korean_label = korean_font.render("오늘의 명언:", True, WHITE)
    korean_label_rect = korean_label.get_rect(center=(SCREEN_WIDTH // 2, restart_button_rect.bottom + 50))
    screen.blit(korean_label, korean_label_rect)
    advice_rect = pygame.Rect(50, korean_label_rect.bottom + 10, SCREEN_WIDTH - 100, SCREEN_HEIGHT - korean_label_rect.bottom - 20)
    draw_text_wrapped(screen, advice_text, advice_font, WHITE, advice_rect)

# --- 메인 게임 루프 ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if game_over:
                if restart_button_rect.collidepoint(mouseX, mouseY): reset_game()
            else:
                row = round((mouseY - BOARD_OFFSET) / CELL_SIZE)
                col = round((mouseX - BOARD_OFFSET) / CELL_SIZE)
                if 0 <= row <= BOARD_SIZE and 0 <= col <= BOARD_SIZE and board[row][col] == 0:
                    board[row][col] = 1 if turn == "black" else 2
                    if check_win(row, col): 
                        winner = turn
                        game_over = True
                    turn = "white" if turn == "black" else "black"

    if game_over:
        screen.fill(GAMEOVER_BG)
        display_end_game_elements(winner)
    else:
        screen.fill(BROWN)
        draw_grid()
        draw_stones()

    pygame.display.flip()
