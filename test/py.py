import pygame
from pygame.locals import *
import sys

pygame.init()

screen = pygame.display.set_mode((800,600))
# 用于保证主循环运行的变量
#runnning = True

# 主循环！
while True:
    # for 循环遍历事件队列
    for event in pygame.event.get():
        # 检测 KEYDOWN 事件: KEYDOWN 是 pygame.locals 中定义的常量，pygame.locals文件开始已经导入
        if event.type == KEYDOWN:
            key_input = pygame.key.get_pressed()
            # 如果按下 Esc 那么主循环终止
            if key_input[K_ESCAPE]:
                #running = False
                sys.exit()
         # 检测 QUIT : 如果 QUIT, 终止主循环
        elif event.type == QUIT:
            sys.exit()