import pygame
import sys
import random
import time

# --- 설정값 (일부러 이상하게 설정) ---
BOARD_SIZE = 19
CELL_SIZE = 40
MARGIN = 40
# 창 크기도 애매하게 안 맞음
WINDOW_SIZE = CELL_SIZE * (BOARD_SIZE - 1) + (MARGIN * 2) + 13 

# 눈이 아픈 색상 팔레트
COLOR_BG = (255, 0, 255)      # 핫핑크 배경
COLOR_GRID = (0, 255, 0)      # 형광 초록 선
COLOR_BLACK = (50, 50, 50)    # 완전 검정도 아님
COLOR_WHITE = (255, 255, 200) # 누런 흰색

# 상태 상수
EMPTY = 0
BLACK = 1
WHITE = 2

class GlitchyBaduk:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("왜 이러는지 모르겠는 바둑")
        self.clock = pygame.time.Clock()
        
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = BLACK
        self.running = True

    def draw_shaky_board(self):
        # 배경을 매 프레임마다 미세하게 깜빡이게 함
        if random.random() < 0.1:
            self.screen.fill((255, 50, 255))
        else:
            self.screen.fill(COLOR_BG)
        
        # 격자 그리기 (선의 시작과 끝이 계속 흔들림)
        for i in range(BOARD_SIZE):
            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-2, 2)
            
            # 가로줄
            start_pos = (MARGIN + shake_x, MARGIN + i * CELL_SIZE + shake_y)
            end_pos = (WINDOW_SIZE - MARGIN - shake_x, MARGIN + i * CELL_SIZE - shake_y)
            pygame.draw.line(self.screen, COLOR_GRID, start_pos, end_pos, 2)
            
            # 세로줄
            start_pos = (MARGIN + i * CELL_SIZE - shake_y, MARGIN + shake_x)
            end_pos = (MARGIN + i * CELL_SIZE + shake_y, WINDOW_SIZE - MARGIN - shake_x)
            pygame.draw.line(self.screen, COLOR_GRID, start_pos, end_pos, 2)

    def draw_weird_stones(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.board[y][x] != EMPTY:
                    # 돌 위치도 제멋대로 흔들림
                    offset_x = random.randint(-3, 3)
                    offset_y = random.randint(-3, 3)
                    
                    center_x = MARGIN + x * CELL_SIZE + offset_x
                    center_y = MARGIN + y * CELL_SIZE + offset_y
                    
                    color = COLOR_BLACK if self.board[y][x] == BLACK else COLOR_WHITE
                    
                    # 10% 확률로 돌 모양이 사각형으로 바뀜
                    if random.random() < 0.1:
                        rect = (center_x - 15, center_y - 15, 30, 30)
                        pygame.draw.rect(self.screen, color, rect)
                    else:
                        # 찌그러진 원 그리기
                        pygame.draw.ellipse(self.screen, color, 
                                            (center_x - 18, center_y - 15, 36, 30))

    def try_place_stone_glitchy(self, x, y):
        # 30% 확률로 클릭 씹힘 (입력 무시)
        if random.random() < 0.3:
            print("렉 걸림: 클릭 무시됨")
            return

        # 10% 확률로 엉뚱한 곳(옆 칸)에 두어짐
        if random.random() < 0.1:
            x = max(0, min(BOARD_SIZE-1, x + random.choice([-1, 1])))
            y = max(0, min(BOARD_SIZE-1, y + random.choice([-1, 1])))
            print(f"미끄러짐! ({x}, {y})에 두어졌습니다.")

        # 이미 돌이 있어도 그냥 겹쳐서 둠 (규칙 파괴)
        # 5% 확률로 내 턴인데 상대방 돌 색깔로 두어짐
        stone_color = self.turn
        if random.random() < 0.05:
            stone_color = WHITE if self.turn == BLACK else BLACK
            print("트롤링: 상대방 색으로 두었습니다.")

        self.board[y][x] = stone_color

        # 따내기 규칙? 그런 거 없음. 그냥 턴만 넘김.
        # 가끔 턴도 안 넘어가고 두 번 두게 해줌 (버그 구현)
        if random.random() > 0.1:
            self.turn = WHITE if self.turn == BLACK else BLACK

    def run(self):
        while self.running:
            # 강제로 프레임 드랍 유발 (버벅거림)
            if random.random() < 0.05:
                time.sleep(0.1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    # 좌표 계산도 대충 함 (반올림 안하고 내림 처리 등)
                    grid_x = int((mx - MARGIN + 10) / CELL_SIZE)
                    grid_y = int((my - MARGIN + 10) / CELL_SIZE)

                    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                        self.try_place_stone_glitchy(grid_x, grid_y)

            self.draw_shaky_board()
            self.draw_weird_stones()
            
            # 타이틀 바가 계속 이상한 말로 바뀜
            if random.random() < 0.02:
                captions = ["바둑?", "오목 아님", "System Error", "Lag...", "Python Baduk"]
                pygame.display.set_caption(random.choice(captions))
            
            pygame.display.flip()
            self.clock.tick(30) # 30프레임 제한이지만 위에서 sleep 걸어서 의미 없음

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GlitchyBaduk()
    game.run()
