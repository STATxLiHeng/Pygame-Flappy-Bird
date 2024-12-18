import pygame
import sys

# 初始化
pygame.init()


size = width,height = 480,460
# 绘制窗口
screen = pygame.display.set_mode(size)
color = (0,0,0)

# 加载图片
ball = pygame.image.load('intro_ball.gif')

# 获取图形的矩形
ball_rect = ball.get_rect()
speed = [2,2]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # 移动小球
    ball_rect = ball_rect.move(speed)
    # 碰撞检测
    if ball_rect.left <=0 or ball_rect.right >= width:
        speed[0] = - speed[0]
    if ball_rect.top <=0 or ball_rect.bottom >= height:
        speed[1] = - speed[1]

    # 填充背景
    screen.fill(color)
    # 显示图片
    screen.blit(ball,ball_rect)

    # 显示窗口
    pygame.display.flip()