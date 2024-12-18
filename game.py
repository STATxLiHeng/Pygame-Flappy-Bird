import pygame
import sys
from setting import Settings
from util import get_random_position, check_collide

class Game():
    def __init__(self):

        pygame.init()
        self.FPS = pygame.time.Clock()
        self.screen = pygame.display.set_mode((settings.screen_width,settings.screen_height))
        # 加載地面
        self.background = pygame.image.load('assets/sprites/background-day.png')
        # 加載歡迎
        self.message = pygame.image.load('assets/sprites/message.png')
        # 加載地面
        self.playground = pygame.image.load('assets/sprites/base.png')
        # 加載數字
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
            pygame.image.load('assets/sprites/9.png'),
        )
        # 加載遊戲結束
        self.gameover = pygame.image.load('assets/sprites/gameover.png')
        # 加載聲音文件
        if sys.platform == 'win':
            extents = 'wav'
        else:
            extents = 'ogg'
        self.sounds = {
                        "die" : pygame.mixer.Sound(f'assets/audio/die.{extents}'),
                        "hit" : pygame.mixer.Sound(f'assets/audio/hit.{extents}'),
                        "point": pygame.mixer.Sound(f'assets/audio/point.{extents}'),
                        "wing": pygame.mixer.Sound(f'assets/audio/wing.{extents}')
                       }


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.show_welcome() # 顯示歡迎頁面
            score,bird,pipe_group=self.main_game() # 進入遊戲
            self.show_game_over(score, bird, pipe_group)


    def show_score(self,score):
        digits = [int(x) for x in list(str(score))]
        total_width = 0
        for item in digits:
            total_width += self.numbers[item].get_width()
        number_x = (settings.screen_width - total_width) *0.5
        number_y =  settings.screen_height * 0.1

        # 顯示圖片
        for item in digits:
            self.screen.blit(self.numbers[item],(number_x,number_y))
            number_x += self.numbers[item].get_width()


    def main_game(self):
        bird = Bird()

        # 創建第一組管道
        pipe1 = [Pipe(direct='upper'),Pipe(direct='lower')]
        positions1 = get_random_position()
        for pipe, position in zip(pipe1,positions1):
            pipe.rect.x = position['x']
            pipe.rect.y = position['y']
        # 創建第二組管道
        pipe2 = [Pipe(direct='upper'), Pipe(direct='lower')]
        positions2 = get_random_position()
        for pipe, position in zip(pipe2, positions2):
            pipe.rect.x = positions1[0]['x'] + settings.screen_width*0.5
            pipe.rect.y = position['y']
        # 創建管道列表
        pipes = [pipe1,pipe2]

        pipe_group = pygame.sprite.Group() #創建精靈組
        pipe_group.add(pipes)

        # 初始化分數
        score = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # 按下按鍵小鳥上移
                if event.type ==pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.sounds['wing'].play()
                    bird.speed = bird.jump
                    if bird.rect.y < 0:
                        bird.rect.y = 0
            # 碰撞檢測
            collide = check_collide(bird,pipe_group)
            if collide:
                self.sounds['hit'].play()
                self.sounds['die'].play()
                return score,bird,pipe_group

            # 小鳥移動
            bird.update()
            # 移動管道
            pipe_group.update()

            # 計算得分
            if pipes[0][0].rect.x + settings.pipe_width< bird.rect.x < pipes[0][0].rect.x + settings.pipe_width + 5:
                score += 1
                self.sounds['point'].play()


            # 創建新的管道
            if 0< pipes[0][0].rect.x<5:
                new_pipe = [Pipe(direct='upper'), Pipe(direct='lower')]
                new_positions = get_random_position()
                for pipe, position in zip(new_pipe, new_positions):
                    pipe.rect.x = position['x']
                    pipe.rect.y = position['y']
                # 加入到管道列表
                pipes.append(new_pipe)
                # 加到精靈組
                pipe_group.add(new_pipe)
            # 移除管道
            if pipes[0][0].rect.x < - settings.pipe_width:
                    # 移除精靈組
                pipe_group.remove(pipes[0])
                pipes.pop(0)
            # 繪製背景
            self.screen.blit(self.background, (0,0))
            # 繪製管道
            pipe_group.draw(self.screen)
            # 顯示得分
            self.show_score(score)
            # 繪製地面
            self.screen.blit(self.playground,(settings.base_x,settings.base_y))
            #顯示小鳥
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
                    # 按下空格退出循環

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.sounds['wing'].play()
                    return

            message_x = int((settings.screen_width - self.message.get_width())/2)
            message_y = int((settings.screen_height - self.message.get_height())/2)
            base_x = -((-base_x + 1) % base_gap)

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.message, (message_x, message_y))
            self.screen.blit(self.playground, (settings.base_x,settings.base_y))
            pygame.display.update()

    def show_game_over(self,score,bird,pipe_group):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    # 按下空格退出循環
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            # 小鳥降落
            bird.update()
            # 顯示背景
            self.screen.blit(self.background,(0,0))
            # 繪製管道
            pipe_group.draw(self.screen)
            # 顯示得分
            self.show_score(score)
            # 顯示地面
            self.screen.blit(self.playground,(settings.base_x,settings.base_y))
            # 顯示gameover
            self.screen.blit(self.gameover,(50,180))
            # 顯示小鳥
            self.screen.blit(bird.image, (bird.rect.x, bird.rect.y))
            pygame.display.update()
            self.FPS.tick(30)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 加載圖片
        self.image = pygame.image.load("assets/sprites/bluebird-midflap.png")
        self.rect = self.image.get_rect()
        self.jump = -9 # 跳躍高度
        self.acceleration = 1 # 重力加速度
        self.max_speed = 10 # 下降最大速度
        self.speed = 0 # 當前速度
        self.rect.x = settings.screen_width * 0.2
        self.rect.y = settings.screen_height * 0.5

    def update(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration

        self.rect.y += min(self.speed,settings.base_y - self.image.get_height()-self.rect.y)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, direct = 'upper'):
        super().__init__()
        if direct == 'lower':
            self.image = pygame.image.load('assets/sprites/pipe-green.png')
        else:
            self.image = pygame.transform.flip(pygame.image.load('assets/sprites/pipe-green.png'),False,True)
        self.rect = self.image.get_rect()
        self.speed = -4
    def update(self):
        self.rect.x += self.speed


if __name__ == "__main__":
    settings = Settings()
    game = Game()
    game.run()