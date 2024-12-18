import sys

import pygame
import sys

# 初始化
pygame.init()

clock = pygame.time.Clock()
#繪製窗口
size = width,height = 480,460
screen = pygame.display.set_mode(size)
color = (0,0,0)

# 加載圖片
ball = pygame.image.load('intro_ball.gif')
# 獲取圖像矩形
ball_rect = ball.get_rect()
speed = [1,1]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # 移動小球
    ball_rect = ball_rect.move(speed)
    # 邊緣檢測
    if ball_rect.left <=0 or ball_rect.right >= width:
        speed[0] = -speed[0]
    if ball_rect.top <= 0 or ball_rect.bottom >= height:
        speed[1] = -speed[1]
    # 填充背景
    screen.fill(color)
    # 顯示圖片
    screen.blit(ball,ball_rect)
    # 展示窗口
    pygame.display.flip()
    clock.tick(240)
