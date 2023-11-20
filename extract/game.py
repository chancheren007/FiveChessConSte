# -*- coding : UTF-8 -*-

import pygame, sys
from pygame.locals import *

from computer import *
import datetime

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'


class five_chess():
    KAN = (255, 255, 255)
    DARK = (0, 0, 0)
    BACKGROUNDCOLOR = (255, 255, 255)
    BLACK = (255, 255, 255)
    BLUE = (0, 0, 255)
    CELL = 40
    PIECEWIDTH = 36
    PIECEHEIGHT = 36
    BOARDX = 2
    BOARDY = 2
    FPS = 40

    def __init__(self):
        self.board = self.init_board()
        self.move_numbers = [[0 for _ in range(15)] for _ in range(15)]
        self.turn = 'player'
        self.move_count = 0
        with open('res/res.txt', 'w') as f:
            pass
        self.run()

    def init_board(self):
        # None is 0, player is 1, computer is 2
        return [[0] * 15 for i in range(15)]

    def get_valid_move(self):
        ret = []
        for i in range(15):
            for j in range(15):
                if self.board[i][j] == 0:
                    ret.append((i, j))
        return ret

    def five(self):
        # 左上，上，右上，左，右，左下，下，右下
        way = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for i in range(15):
            for j in range(15):
                if self.board[i][j] != 0:
                    get = self.board[i][j]

                    for w in way:
                        now = (i, j)
                        count = 1

                        while True:
                            if (now[0] + w[0] not in range(15)) or (now[1] + w[1] not in range(15)):
                                break

                            now = (now[0] + w[0], now[1] + w[1])

                            if self.board[now[0]][now[1]] != get:
                                break
                            else:
                                count += 1

                                if count == 5:
                                    return get
        return False

    def valid_input(self, pos):
        if pos[0] not in range(15) or pos[1] not in range(15):
            return False
        if self.board[pos[0]][pos[1]] != 0:
            return False
        return True

    def get_computer_pos(self):
        return get_pos(self.board)
    
    def render_move_number(self, windowSurface, move_number, rectDst, piece):
        basicFont = pygame.font.SysFont('Courier New', 20, bold=True, italic=True)
        text = basicFont.render(str(move_number), True, self.DARK if piece == 2 else self.KAN)
        textRect = text.get_rect()
        textRect.center = rectDst.center
        windowSurface.blit(text, textRect)

    def check_mouse_on(self, rect, windowSurface):
        point_x, point_y = pygame.mouse.get_pos()
        w, h = rect.width, rect.height

        x, y = windowSurface.get_rect().centerx, windowSurface.get_rect().centery + 75

        in_x = abs(point_x - x) < (w / 2)
        in_y = abs(point_y - y) < (h / 2)

        return in_x and in_y

    def run(self):
        # 初始化
        pygame.init()
        mainClock = pygame.time.Clock()

        # 加载图片
        icon = pygame.image.load('pic/cheese.png')

        boardImage = pygame.image.load('pic/board.jpg')
        boardRect = boardImage.get_rect()
        blackImage = pygame.image.load('pic/black.png')
        blackRect = blackImage.get_rect()
        whiteImage = pygame.image.load('pic/white.png')
        whiteRect = whiteImage.get_rect()
        restartImage_up = pygame.image.load('pic/restart_up.png')
        rsupRect = restartImage_up.get_rect()
        restartImage_down = pygame.image.load('pic/restart_down.png')
        rsdnRect = restartImage_down.get_rect()

        basicFont = pygame.font.SysFont('arial', 40)

        # 设置窗口
        # windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))
        # pygame.display.set_icon(icon)
        # pygame.display.set_caption('Covert Information Extraction by h_key')

        pygame.display.set_mode((800, 600), pygame.NOFRAME | pygame.SCALED | pygame.RESIZABLE)

        # Set the window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

        # Set the window size
        windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height), pygame.NOFRAME)

        gameOver = False

        # 游戏主循环
        while True:

            windowSurface.fill(self.BACKGROUNDCOLOR)
            windowSurface.blit(boardImage, boardRect, boardRect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if gameOver == False and self.turn == 'player' and event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    col = int((x - self.BOARDX) / self.CELL)
                    row = int((y - self.BOARDY) / self.CELL)
                    pos = (col, row)

                    if self.valid_input(pos):
                        self.board[pos[0]][pos[1]] = 1
                        self.move_count += 1
                        self.move_numbers[pos[0]][pos[1]] = self.move_count

                        if self.five() or not self.get_valid_move():
                            gameOver = True
                        else:
                            self.turn = 'computer'

            if gameOver == False and event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                col = int((x - self.BOARDX) / self.CELL)
                row = int((y - self.BOARDY) / self.CELL)
                pos = (col, row)
                i = 0

                if self.valid_input(pos):
                    if self.turn == 'player':
                        self.board[pos[0]][pos[1]] = 1
                    else:
                        computer_move = self.get_computer_pos()
                        for tar, soc in computer_move:
                            i += 1
                            if pos == tar and soc < 100000:
                                try:
                                    print(f"[{blue}{datetime.datetime.now().strftime('%H:%M:%S')}{end}] [{green}INFO{end}] {str(bianma()[i-1])}")
                                    with open('res/res.txt', 'a') as f:
                                        f.write(str(bianma()[i - 1]))
                                except:
                                    print(f"[{blue}{datetime.datetime.now().strftime('%H:%M:%S')}{end}] [{red}WARNING{end}] empty")
                        self.board[pos[0]][pos[1]] = 2
                    self.move_count += 1
                    self.move_numbers[pos[0]][pos[1]] = self.move_count

                    if self.five() or not self.get_valid_move():
                        gameOver = True
                    else:
                        self.turn = 'computer' if self.turn == 'player' else 'player'

            for x in range(15):
                for y in range(15):
                    rectDst = pygame.Rect(self.BOARDX + x * self.CELL, self.BOARDY + y * self.CELL, self.PIECEWIDTH,
                                          self.PIECEHEIGHT)
                    if self.board[x][y] == 1:
                        windowSurface.blit(blackImage, rectDst, blackRect)
                        self.render_move_number(windowSurface, self.move_numbers[x][y], rectDst, 1)
                    elif self.board[x][y] == 2:
                        windowSurface.blit(whiteImage, rectDst, whiteRect)
                        self.render_move_number(windowSurface, self.move_numbers[x][y], rectDst, 2)

            if gameOver:
                res = self.five()
                if res:
                    result = "You Win" if res == 1 else "You Lose"

                else:
                    result = "In A Draw"

                text = basicFont.render(result, True, self.BLACK, self.BLUE)
                textRect = text.get_rect()
                textRect.centerx = windowSurface.get_rect().centerx
                textRect.centery = windowSurface.get_rect().centery

                restart = pygame.Rect(textRect.centerx - 100, textRect.centery + 50, 200, 50)
                back = False
                while True:
                    if back: break

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.check_mouse_on(rsupRect,
                                                                                                       windowSurface):
                            self.board = self.init_board()
                            self.turn = 'player'
                            gameOver = False
                            back = True

                    for x in range(15):
                        for y in range(15):
                            rectDst = pygame.Rect(self.BOARDX + x * self.CELL, self.BOARDY + y * self.CELL,
                                                  self.PIECEWIDTH, self.PIECEHEIGHT)
                            if self.board[x][y] == 1:
                                windowSurface.blit(blackImage, rectDst, blackRect)
                                self.render_move_number(windowSurface, self.move_numbers[x][y], rectDst, 1)
                            elif self.board[x][y] == 2:
                                windowSurface.blit(whiteImage, rectDst, whiteRect)
                                self.render_move_number(windowSurface, self.move_numbers[x][y], rectDst, 2)

                    windowSurface.blit(text, textRect)

                    if self.check_mouse_on(rsupRect, windowSurface):
                        windowSurface.blit(restartImage_up, restart, rsupRect)
                    else:
                        windowSurface.blit(restartImage_down, restart, rsdnRect)

                    pygame.display.update()
                    mainClock.tick(self.FPS)

            pygame.display.update()
            mainClock.tick(self.FPS)


game = five_chess()
game.run()
