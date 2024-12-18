import sys
import pygame

from settings import Settings
from util import get_random_position,check_collide

class Game():
    def __init__(self):
        pygame.init()
        self.FPS = pygame.time.Clock()
        self.screen = pygame.display.set_mode((settings.screen_width,settings.screen_height))
        # 加载地面图片
        self.background = pygame.image.load('assets/sprites/background-day.png')
        # 加载欢迎语
        self.message = pygame.image.load('assets/sprites/message.png')
        # 加载地面
        self.playground = pygame.image.load('assets/sprites/base.png')
        # 加载数字图片
        self.numbers = (
            pygame.image.load('assets/sprites/0.png'),
            pygame.image.load('assets/sprites/1.png'),
            pygame.image.load('assets/sprites/2.png'),
            pygame.image.load('assets/sprites/3.png'),
            pygame.image.load('assets/sprites/4.png'),
            pygame.image.load('assets/sprites/5.png'),
            pygame.image.load('assets/sprites/6.png'),
            pygame.image.load('assets/sprites/7.png'),
            pygame.image.load('assets/sprites/8.png'),
            pygame.image.load('assets/sprites/9.png')
        )
        # 加载游戏结束图片
        self.gameover = pygame.image.load('assets/sprites/gameover.png')
        # 加载声音文件
        if sys.platform == 'win':
            extents = 'wav'
        else:
            extents = 'ogg'
        self.sounds = {
            'die': pygame.mixer.Sound(f'assets/audio/die.{extents}'),
            'hit': pygame.mixer.Sound(f'assets/audio/hit.{extents}'),
            'point': pygame.mixer.Sound(f'assets/audio/point.{extents}'),
            'wing': pygame.mixer.Sound(f'assets/audio/wing.{extents}'),
        }


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.show_welcome() # 显示欢迎页面
            score,bird,pipe_group = self.main_game()    # 进入游戏
            self.show_gameover(score, bird, pipe_group)

    def show_score(self,score):
        # 17 [1,7]
        digits = [int(x) for x in list(str(score))]
        total_width = 0
        for item in digits:
            total_width += self.numbers[item].get_width()
        number_x = (settings.screen_width - total_width) * 0.5
        number_y = settings.screen_height * 0.1
        # 显示图片
        for item in digits:
            self.screen.blit(self.numbers[item],(number_x,number_y))
            number_x += self.numbers[item].get_width()



    def main_game(self):
        bird = Bird()
        # 创建第1组管道
        pipe1 = [Pipe(direct='upper'),Pipe(direct='lower')]
        positions1 = get_random_position()
        for pipe,position in zip(pipe1,positions1):
            pipe.rect.x = position['x']
            pipe.rect.y = position['y']

        # 创建第2组管道
        pipe2 = [Pipe(direct='upper'),Pipe(direct='lower')]
        positions2 = get_random_position()
        for pipe,position in zip(pipe2,positions2):
            pipe.rect.x = positions1[0]['x'] + settings.screen_width*0.5
            pipe.rect.y = position['y']
        # 创建管道列表
        pipes = [pipe1,pipe2]

        # 创建精灵组
        pipe_group = pygame.sprite.Group()
        pipe_group.add(pipes)

        # 初始化分数
        score = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # 按下向上箭头，小鸟上移
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.sounds['wing'].play()
                    bird.speed = bird.jump
                    if bird.rect.y < 0:
                        bird.rect.y = 0
            # 碰撞检测
            collide = check_collide(bird,pipe_group)
            if collide:
                self.sounds['hit'].play()
                self.sounds['die'].play()
                return score,bird,pipe_group
            # 小鸟移动
            bird.update()
            # 移动管道
            pipe_group.update()

            # 计算得分
            if pipes[0][0].rect.x + settings.pipe_width < bird.rect.x < pipes[0][0].rect.x + settings.pipe_width + 5:
                score += 1
                self.sounds['point'].play()


            # 创建新管道
            if 0< pipes[0][0].rect.x <5:
                new_pipe = [Pipe(direct='upper'), Pipe(direct='lower')]
                new_positions = get_random_position()
                for pipe, position in zip(new_pipe, new_positions):
                    pipe.rect.x = position['x']
                    pipe.rect.y = position['y']
                # 加入到管道列表
                pipes.append(new_pipe)
                # 加入到精灵组
                pipe_group.add(new_pipe)

            # 移除管道
            if pipes[0][0].rect.x < - settings.pipe_width:
                # 移出精灵组settings.grap_size
                pipe_group.remove(pipes[0])
                # 移出管道列表
                pipes.pop(0)


            # 显示背景
            self.screen.blit(self.background, (0, 0))
            # 绘制管道
            pipe_group.draw(self.screen)
            # 显示分数
            self.show_score(score)
            # 显示地面
            self.screen.blit(self.playground,(settings.base_x,settings.base_y))

            # 显示小鸟
            self.screen.blit(bird.image,(bird.rect.x,bird.rect.y))
            pygame.display.update()
            self.FPS.tick(30)


    def show_welcome(self):
        base_x = 0
        base_gap = self.playground.get_width() - settings.screen_width
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # 按下空格键，退出循环
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.sounds['wing'].play()
                    return

            # 设置欢迎语坐标
            message_x = int((settings.screen_width - self.message.get_width())/2)
            message_y = settings.screen_height * 0.2
            # 设置地面坐标
            base_x = -((-base_x + 4) % base_gap)
            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.message,(message_x,message_y))
            self.screen.blit(self.playground,(base_x,settings.base_y))

            pygame.display.update()

    def show_gameover(self,score,bird,pipe_group):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # 按下空格键，退出循环
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            # 小鸟降落
            bird.update()
            # 显示背景
            self.screen.blit(self.background, (0, 0))
            # 绘制管道
            pipe_group.draw(self.screen)
            # 显示分数
            self.show_score(score)
            # 显示地面
            self.screen.blit(self.playground, (settings.base_x, settings.base_y))
            # 显示小鸟
            self.screen.blit(bird.image,(bird.rect.x,bird.rect.y))
            # 显示gameover
            self.screen.blit(self.gameover,(50,180))

            pygame.display.update()
            self.FPS.tick(30)



class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 加载小鸟图片
        self.image = pygame.image.load('assets/sprites/bluebird-midflap.png')
        self.rect = self.image.get_rect()

        self.jump = -9 # 按下按键，小鸟跳跃高度
        self.acceleration = 1 # 重力加速度
        self.max_speed = 10   # 下降的最大速度
        self.speed = 0 # 当前小鸟的速度
        self.rect.x = settings.screen_width * 0.2
        self.rect.y = 0

    def update(self):
        # 速度变化
        if self.speed < self.max_speed:
            self.speed += self.acceleration

        self.rect.y += min(self.speed,settings.base_y - self.image.get_height() - self.rect.y)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,direct='upper'):
        super().__init__()
        # 创建上管道或者下管道
        if direct == 'lower':
            self.image = pygame.image.load('assets/sprites/pipe-green.png')
        else:
            self.image = pygame.transform.flip(pygame.image.load('assets/sprites/pipe-green.png'),False,True)
        self.rect = self.image.get_rect()
        self.speed = -4  # 向左移动速度

    def update(self):
        self.rect.x += self.speed


if __name__ == "__main__":
    settings = Settings()
    game = Game()
    game.run()
