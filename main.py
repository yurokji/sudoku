import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYDOWN, K_r, K_s
from sudoku import *


su = Sudoku()
su.generate()

# 파이게임을 이용하여 게임 시작
cell_width = 100
w, h = cell_width * su.size, cell_width * su.size
print(w, h)
pygame.init()
clock = pygame.time.Clock()
SURFACE = pygame.display.set_mode((w,h))


# 보드 이미지
board_img = pygame.image.load("./images/board.png")
board_img = pygame.transform.scale(board_img, (w,h))

# 백그라운드 이미지
back_img = pygame.image.load("./images/back.png")
back_img = pygame.transform.scale(back_img, (w,h))

# 숫자 이미지(유저 클릭가능)
num_imgs = []
for i in range(0, su.size + 1):
    img = pygame.image.load(f"./images/{str(i)}.png")
    num_imgs.append(pygame.transform.scale(img, (cell_width, cell_width)))
    
# 고정된 숫자 이미지(유저 클릭 불가능)
num_fixed_imgs = []
for i in range(0, su.size + 1):
    if i==NOT_FILLED:
        img = pygame.image.load(f"./images/{str(i)}.png")
    else:        
        img = pygame.image.load(f"./images/{str(i)}f.png")
    num_fixed_imgs.append(pygame.transform.scale(img, (cell_width, cell_width)))

# 게임 클리어 출력 메시지를 위한 텍스트 렌더링 준비
font = pygame.font.SysFont('nanumgothicbold',40)  
text = font.render("정답을 맞추셨습니다",True,(255,0,0))  

        
running = True
isClear = False
pressed = False
clicked = False
# 마우스를 클릭하면 0에서 9~0~9까지 차례대로 변하도록 한다
user_number = 0
# 파이게임 루프
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            # r키를 누르면 스도쿠 초기화
            if event.key == K_r:
                su.generate()
            # s키를 누르면 스도쿠 문제 컴퓨터가 풀어줌
            elif event.key == K_s:
                su.solve()
        # 마우스 버튼을 눌렀을 때
        elif event.type == MOUSEBUTTONDOWN:
            pressed = True
            clicked = False
        # 마우스 버튼을 떼었을 때
        elif event.type == MOUSEBUTTONUP:
            # 만약 마우스 버튼을 눌렀다 뗀 것이라면
            if pressed:
                # 마우스의 위치를 가져온다
                pos_x, pos_y = pygame.mouse.get_pos()
                pressed = False
                clicked = False
            # 마우스의 위치가 화면의 10픽셀 안쪽인지 확인한다
            if pos_x > 10 and pos_x < w - 10 and \
                pos_y > 10 and pos_y < h - 10:
                    # 만약 화면 안쪽이라면
                    # 누른 마우스 좌표를 i,j셀 위치로 환산한다
                    j_q = int(pos_x / cell_width)
                    i_q = int(pos_y / cell_width)
                    # 그 위치가 유저가 변환 가능한 셀인지 확인한다
                    if (i_q, j_q) in su.user_places:
                        # 가능하다면 현재 number를 유저에게 제시한다
                        su.grid[i_q][j_q] = user_number
                        # 같은 셀을 또 다시 클릭할 경우
                        # 숫자가 1이 올라가도록 한다
                        user_number += 1
                        # 숫자가 10이 되었을 경우 다시 1로 바꾸어준다
                        if user_number > 9:
                            user_number = 1
                        # 이미 클릭이 완료된 곳으로 지정한다
                        clicked = True
        
        
        
    #클릭되었다면 스도쿠를 조사하여 게임이 클리어되었는지 살핀다
    if clicked:
        if not isClear:
            # 우선 스도쿠가 모두 채워졌는지 조사한다
            if su.isAllFilled():
                # 그리고 나서 게임이 클리어되었는지 살핀다
                if su.isSolved():
                    isClear = True

            
                
    
    # 그림을 그려주자...드디어ㅜㅠㅠㅜㅜ
    SURFACE.fill((255,255,255))
    
    for i in range(su.size):
        for j in range(su.size):
            # 고정된 위치는 고정된 위치의 스프라이트 이미지로 나타내주자
            if (i,j) in su.fixed_places:
                SURFACE.blit(num_fixed_imgs[su.grid[i][j]], (j * cell_width, i * cell_width))
            # 유저가 클릭하여 변경할 수 있는 위치의 스프라이트 이미지를 그린다
            else:
                SURFACE.blit(num_imgs[su.grid[i][j]], (j * cell_width, i * cell_width))
    
    # 모든 셀의 가장자리를 그려준다
    for i in range(su.size):
        for j in range(su.size):
            rect = (i * cell_width, j * cell_width, cell_width, cell_width)
            pygame.draw.rect(SURFACE, (0,0,0), rect, 2)
    
    # 모든 블록의 가장자리를 두껍게 그려준다
    for i in range(3):
        for j in range(3):
            rect = (i * cell_width * 3, j * cell_width * 3, cell_width * 3, cell_width * 3)
            pygame.draw.rect(SURFACE, (0,0,0), rect, 5)
    
    # 게임이 클리어되었다면 메시지를 표시한다
    if isClear:
        SURFACE.blit(text,(400,w//2 - 100 ))
        pygame.display.update()
        # 3초를 기다린다
        pygame.time.wait(2000)
        isClear = False
        # 게임의 레벨을 올려준다
        su.difficulty += 4
        # 게임을 재시작한다
        su.generate()
            
    
    pygame.display.update()
    clock.tick(60)
            
            
        
                                
                        
                
    