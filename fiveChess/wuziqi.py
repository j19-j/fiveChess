from pygame.locals import *
import pygame.gfxdraw
import traceback
import sys
from Checkerboard import Checkerboard#检查
from AI import AI#电脑下棋
from In_package import *#全局变量
from prepare import Prepare#需要准备的函数，比如画棋盘，画棋子，棋盘的提示信息

#人人对战
def person():
    fwidth, fheight = font2.size('黑子获胜')
    checkerboard = Checkerboard(Line_Points)
    pre = Prepare()
    cur_runner = WHITE_CHESSMAN  # 玩家一
    winner = None
    # 设置黑白双方初始连子为0
    black_win_count = 0
    white_win_count = 0
    AI_x = 0
    AI_y = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:  # 检测鼠标落下
                if winner is None:  # 检测是否有一方胜出
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        click_point = pre.get_clickpoint(mouse_pos)
                        if click_point:
                            AI_x, AI_y = click_point[0], click_point[
                                1]  # prevent 'NoneType' object is not subscriptable
                        if click_point is not None:  # 检测鼠标是否在棋盘内点击 #玩家1
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(cur_runner, click_point)
                                if winner is None:  # 再次判断是否有胜出
                                    # 每下一次检测一次
                                    cur_runner = pre.get_next(cur_runner)  # 换成玩家2下棋
                                    if click_point is not None:  # 检测鼠标是否在棋盘内点击
                                        if checkerboard.can_drop(click_point):  # 落子
                                            winner = checkerboard.drop(cur_runner, click_point)
                                            if winner is not None:  # 再次检测是否有胜出
                                                white_win_count += 1
                                            cur_runner = pre.get_next(cur_runner)
                                else:
                                    black_win_count += 1
                x, y = event.pos[0], event.pos[1]
                if 610 < x < 800 and 333 < y < 360:  # 点击重新开始
                    person()
                elif 600 < x < 800 and 400 < y < 500:  # 点击‘回到主界面’
                    enter_the_game()
                # elif 630 < x < 800 and 270 < y < 500:  # 点击‘悔棋’
                #     print('悔棋')
        pre.draw_checkerboard(screen)  # 画棋盘
        pre.draw_all(checkerboard, AI_x, AI_y)  # 画棋盘上的棋子
        pre.remind_chess(cur_runner)

        pre.draw_left_info_every(screen, font1)
        if winner:
            pre.print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2,
                           winner.Name + '获胜',
                           RED_COLOR)
        pygame.display.flip()


def enter_per_com():  # 进入人机对战界面，可以选择谁先
    screen.fill(Checkerboard_Color)
    pre = Prepare()
    # _draw_left_info_begin(screen, font1)  #初始界面
    Background = pygame.image.load("人机对战.png").convert_alpha()  # 图片填充
    screen.blit(Background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            # 点击x则关闭窗口
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # 点击窗口里面类容则完成相应指令
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    pre.draw_checkerboard(screen)  # 画棋盘
                    pygame.display.flip()  # 刷新屏幕显示出来
                    # 如果点击‘我方先手’
                    if 210 < x < 500 and 270 < y < 360:
                        person_computer("me")
                        print("我方先手")

                    # 点击‘电脑先手’
                    elif 210 < x < 500 and 370 < y < 460:
                        person_computer("com")
                        print("电脑先手")

        clock.tick(60)


def person_computer(first):  # 人机对战

    fwidth, fheight = font2.size('黑子获胜')
    checkerboard = Checkerboard(Line_Points)
    computer = AI(Line_Points, BLACK_CHESSMAN)  # 实例化一个对象
    pre = Prepare()
    black_win_count = 0
    AI_x = 0
    AI_y = 0
    winner = None
    cur_runner = WHITE_CHESSMAN  # 电脑下玩之后，到我方下棋
    # 设置黑白双方初始连子为0
    white_win_count = 0
    while True:
        """
        默认白子优先
        """
        if first == "com":
            # 电脑落子是让电脑在5-13之间随机选一个位置（这里在中间部分）
            AI_point = computer.randDrop()  # 电脑落子
            print("hellouuu", AI_point)
            AI_x = AI_point[0]
            AI_y = AI_point[1]
            winner = checkerboard.drop(cur_runner, AI_point)
            if winner is not None:
                white_win_count += 1
            cur_runner = pre.get_next(cur_runner)
            first = "other"
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:  # 检测鼠标落下
                    if winner is None:  # 检测是否有一方胜出
                        """
                        pygame.mouse.get_pressed()  表示左键和右键被按下(左键、中键、右键)
                        (True, False, False)
                        """
                        pressed_array = pygame.mouse.get_pressed()
                        if pressed_array[0]:  # 按下左键
                            mouse_pos = pygame.mouse.get_pos()  # 获取点击位置

                            click_point = pre.get_clickpoint(mouse_pos)  # 物理->逻辑  根据鼠标点击位置，返回游戏区坐标
                            if click_point is not None:  # 检测鼠标是否在棋盘内点击
                                if checkerboard.can_drop(click_point):  # 玩家落子
                                    # flag = 0
                                    # 这个是点击标记的，电脑下棋并不是靠点击啊！！！
                                    # mouse_x,mouse_y = mouse_pos[0],mouse_pos[1]
                                    winner = checkerboard.drop(cur_runner, click_point)
                                    if winner is None:  # 再次判断是否有胜出
                                        # 一个循环内检测两次，意思就是人出一次检测一下，电脑出一次检测一下。
                                        cur_runner = pre.get_next(cur_runner)
                                        computer.get_opponent_drop(click_point)  # 电脑获得人落子位置
                                        AI_point = computer.AI_drop()  # 电脑落子

                                        # 逻辑->物理， 并且是电脑落子才标记，人落子就不用标记
                                        AI_x, AI_y = AI_point[0], AI_point[1]

                                        winner = checkerboard.drop(cur_runner, AI_point)
                                        if winner is not None:
                                            white_win_count += 1
                                        cur_runner = pre.get_next(cur_runner)
                                    else:
                                        black_win_count += 1
                    x, y = event.pos[0], event.pos[1]
                    if 610 < x < 800 and 333 < y < 360:  # 点击重新开始，需要回到刚开始选择是哪方先手
                        enter_per_com()
                    elif 600 < x < 800 and 400 < y < 500:  # 点击‘回到主界面’
                        enter_the_game()
        pre.draw_checkerboard(screen)  # 画棋盘
        pre.draw_all(checkerboard, AI_x, AI_y)  # 画棋盘上的棋子
        pre.draw_left_info_computer(screen, font1, first)
        if winner:
            pygame.draw.line(screen, RED_COLOR, checkerboard.ls[0], checkerboard.ls[1], 5)  # 画线段
            # pygame.gfxdraw.aacircle(screen, 26 + 30 * i, 26 + 30 * j, radius, BLACK_COLOR)
            pre.print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2,
                           winner.Name + '获胜',
                           RED_COLOR)

        pygame.display.flip()

def enter_the_game():
        pre = Prepare()
        screen.fill(Checkerboard_Color)
        # _draw_left_info_begin(screen, font1)  #初始界面
        Background = pygame.image.load("new_backgroud_begin.jpg").convert_alpha()  # 图片填充
        screen.blit(Background, (0, 0))
        pygame.display.flip()
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                # 点击x则关闭窗口
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # 点击窗口里面类容则完成相应指令
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos[0], event.pos[1]
                        pre.draw_checkerboard(screen)  # 画棋盘
                        pygame.display.flip()  # 刷新屏幕显示出来
                        # 如果点击‘人机对战’
                        if 210 < x < 500 and 270 < y < 360:
                            # 取消阻止
                            running = True
                            # 播放音效
                            # button_sound.play(0)
                            # 重新开始
                            enter_per_com()
                            # person_person()
                            print("人机对战")

                        # 点击‘人人对战’
                        elif 210 < x < 500 and 370 < y < 460:
                            person()
                            print("人人对战")

            clock.tick(60)

def main():
    try:
        enter_the_game()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
if __name__ == "__main__":
    main()



