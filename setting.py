class Settings():
    def __init__(self):
        # 設置窗口
        self.screen_width = 288
        self.screen_height = 512
        # 設置地面
        self.base_x = 0
        self.base_y = self.screen_height * 0.8
        # 設置管道
        self.pipe_height = 320
        self.pipe_width = 52
        self.grap_size = 100 # 管道間的距離
