import random
import pygame
from settings import Settings

settings = Settings()

def get_random_position():
    # [{x:0,y:0},{x:0,y:100}]
    grap_y = random.randint(0,int(settings.screen_height*0.5-settings.grap_size))
    grap_y += int(settings.grap_size*0.2)
    position = [
        {'x':settings.screen_width+10,'y':grap_y-settings.pipe_height},
        {'x':settings.screen_width+10,'y':grap_y+settings.grap_size},
    ]
    return position

def check_collide(bird, pipe_group):
    # 碰到地面
    if bird.rect.y + bird.image.get_height() >= settings.base_y - 1:
        return True

    # 碰撞管道
    if pygame.sprite.spritecollide(bird, pipe_group,dokill=False,collided=pygame.sprite.collide_mask):
        return True

    return False