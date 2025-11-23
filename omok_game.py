# omok_game.py
import pygame
import sys
import numpy as np
import os

# AI 모듈 불러오기 (나중에 파일 만들면 자동으로 작동)
try:
    import ai_logic
except ImportError:
    ai_logic = None

# --- 설정 ---
SIZE = 15
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (219, 172, 78)

# --- 초기화 ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Omok Game (Gemini Feedback Ver.)")

# --- 효과음 설정 ---
# 파일이 없으면 비프음으로 대체하여 에러 방지
try:
    stone_sound = pygame.mixer.Sound("stone.wav")
except:
    stone_sound = None

def play_sound():
    if stone_sound:
        stone_sound.play()
    else:
        # 윈도우 비프음 (효과음 파일 없을 때 대용)
        print('\a') 

# --- 게임 로직 ---
board = np.zeros((SIZE, SIZE), dtype=int)

def draw_board():
    screen.fill(BG_COLOR)
    for i in range(SIZE):
        pygame.draw.line(screen, BLACK, (GRID_SIZE // 2, i * GRID_SIZE + GRID_SIZE // 2), 
                         (WIDTH - GRID_SIZE // 2, i * GRID_SIZE + GRID_SIZE // 2))
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE // 2), 
                         (i * GRID_SIZE + GRID_SIZE // 2, HEIGHT - GRID_SIZE // 2))
    
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y][x] == 1:
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 2)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, WHITE, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 2)

def check_win(player):
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y][x] == player:
                for dy, dx in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    count = 0
                    for k in range(5):
                        ny, nx = y + k*dy, x + k*dx
                        if 0 <= ny < SIZE and 0 <= nx < SIZE and board[ny][nx] == player:
                            count += 1
                        else:
                            break
                    if count == 5:
                        return True
    return False

# --- 메인 실행 ---
def main():
    turn = 1 # 1: 흑(나), 2: 백(AI)
    game_over = False
    
    while True:
        draw_board()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if not game_over:
                # 1. 사용자 턴 (흑돌)
                if turn == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    gx, gy = mx // GRID_SIZE, my // GRID_SIZE
                    if board[gy][gx] == 0:
                        board[gy][gx] = 1
                        play_sound() # 효과음 재생
                        if check_win(1):
                            print("흑돌 승리!")
                            game_over = True
                        turn = 2

        # 2. AI 턴 (백돌) - Gemini API
        if not game_over and turn == 2:
            pygame.display.flip()
            if ai_logic:
                print("Gemini가 생각 중입니다...")
                ay, ax = ai_logic.get_best_move(board)
                if board[ay][ax] == 0:
                    board[ay][ax] = 2
                    play_sound() # 효과음 재생
                    if check_win(2):
                        print("백돌(AI) 승리!")
                        game_over = True
                    turn = 1
            else:
                # AI 파일이 없을 경우 임시 패스
                pass

if __name__ == "__main__":
    main()