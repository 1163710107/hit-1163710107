# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from mineSweeper.MineMap import MineMap


class MineSweeper:
    # 初始化创建窗口
    def __init__(self, level):
        # level表示困难级别1、2、3对应简单、普通、困难
        self.click = 0
        if level == 1:
            # height表示游戏地图有几行
            self.height = 9
            # width表示游戏地图有几列
            self.width = 9
            self.title = b'EASY'
        elif level == 2:
            self.height = 16
            self.width = 16
            self.title = b'NORMAL'
        elif level == 3:
            self.height = 16
            self.width = 30
            self.title = b'HARD'
        # haveFound表示已经点开的格子数
        self.haveFound = 0
        # 创建地图
        self.mineMap = MineMap(level)
        # 记录视图 0为初始状态，1为掀开显示周围地雷数，2为旗子标记
        self.view = [([0] * (self.width + 2)) for p in range(self.height + 2)]

        # 传递命令行参数
        glutInit(sys.argv)
        # 设置显示模式
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        # 设置窗口位置
        glutInitWindowPosition(100, 100)
        # 设置窗口大小
        glutInitWindowSize(40 * self.width, 40 * self.height)
        # 创建窗口
        glutCreateWindow(self.title)
        # 设置场景绘制函数
        glutDisplayFunc(self.Draw)
        # 调用OpenGL初始化函数
        glClearColor(0.96, 0.96, 0.96, 0.0)
        # 显示范围
        gluOrtho2D(0, 40 * self.width, 0, 40 * self.height)
        print("jianting")
        glutMouseFunc(self.mouseClick)

    # 绘制地图
    def Draw(self):
        # 清除缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.0, 0.0, 0.0)

        # 绘制地图
        for i in range(1, self.width):
            glBegin(GL_LINES)
            glVertex2f(40 * i, 0, )
            glVertex2f(40 * i, 40 * self.height)
            glEnd()

        for j in range(1, self.height):
            glBegin(GL_LINES)
            glVertex2f(0, 40 * j)
            glVertex2f(40 * self.width, 40 * j)
            glEnd()

        glTranslatef(0.0, 0.0, -1.0)
        #交换缓存
        glutSwapBuffers()

    def MainLoop(self):
        # 进入消息循环
        glutMainLoop()

    def mouseClick(self, btn, state, x, y):
        # 从鼠标坐标确定点击的行和列数
        row = int(y / 40) + 1
        col = int(x / 40) + 1
        # 鼠标监听同样存在问题，右键的按下会触发左键按下，抬起出发右键按下，
        # 直接非左键（中间、右键）的点击都执行标记操作，click作用与main相同
        if btn == GLUT_LEFT_BUTTON & state == GLUT_DOWN:
            self.click += 1
            if self.click % 2 == 0:
                print('row' + str(row) + 'col' + str(col))
                # 此格子在初始状态下可接受左键点击执行操作
                if self.view[row][col] == 0:
                    # 此格为地雷，gameover
                    if self.mineMap.isMine(row, col):
                        self.gameover()
                    # 不是地雷，掀开格子
                    else:
                        # 如果此格周围没有地雷，则拓展掀开这一片没有地雷的区域
                        if self.mineMap.mines[row][col] == 0:
                            self.multiplicate(row, col)
                        else:
                            self.view[row][col] = 1
                            self.haveFound += 1
                        # 更新视图
                        self.update()
        # 右键和中间的操作，标记或取消标记
        else:
            self.click += 1
            if self.click % 2 == 0:
                print('row' + str(row) + 'col' + str(col))
                # 此格为初始状态，标记
                if self.view[row][col] == 0:
                    self.view[row][col] = 2
                    # 更新视图
                    self.update()
                # 此格为标记状态，取消标记
                elif self.view[row][col] == 2:
                    self.view[row][col] = 0
                    # 更新视图
                    self.update()

    # 绘制游戏结束界面，显示所有地雷，good luck next time！
    def gameover(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # 遍历地图
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                # 地雷显示
                if self.mineMap.mines[i][j] == -1:
                    self.drawBoom(i, j)
                # 标记显示
                elif self.view[i][j] == 2:
                    self.drawFlag(i, j)
                # 周围地雷数显示
                elif self.view[i][j] == 1:
                    self.drawNumber(i, j)

        # 绘制地图
        glColor3f(0.0, 0.0, 0.0)
        for i in range(1, self.width):
            # 画线
            glBegin(GL_LINES)
            glVertex2f(40 * i, 0, )
            glVertex2f(40 * i, 40 * self.height)
            glEnd()

        for j in range(1, self.height):
            # 画线
            glBegin(GL_LINES)
            glVertex2f(0, 40 * j)
            glVertex2f(40 * self.width, 40 * j)
            glEnd()
        # 显示祝福语
        glColor3f(1.0, 0.8, 0.1)
        x = 20 * self.width - 160
        y = 20 * self.height
        glRasterPos2f(x, y)
        c = str('Good Luck Next Time!')
        for cc in c:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(cc))

        glutSwapBuffers()

    # 绘制炸弹 两个三角形组成
    def drawBoom(self, row, col):
        glColor3f(1.0, 0.0, 0.0)
        # 格子左上角坐标
        x0 = 40 * (col - 1)
        y0 = 40 * (self.height - row + 1)
        # 画三角形
        glBegin(GL_TRIANGLES)
        glVertex2f(x0 + 5, y0 - 27)
        glVertex2f(x0 + 35, y0 - 27)
        glVertex2f(x0 + 20, y0 - 7)
        glEnd()
        # 画三角形
        glBegin(GL_TRIANGLES)
        glVertex2f(x0 + 5, y0 - 13)
        glVertex2f(x0 + 35, y0 - 13)
        glVertex2f(x0 + 20, y0 - 33)
        glEnd()

    # 更新视图
    def update(self):
        # 清除缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # 遍历视图
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                # 画标记
                if self.view[i][j] == 2:
                    self.drawFlag(i, j)
                # 显示周围地雷数
                elif self.view[i][j] == 1:
                    self.drawNumber(i, j)
        # 点开所有非地雷格子，游戏胜利
        if self.haveFound >= self.mineMap.findout:
            glColor3f(1.0, 0.8, 0.1)
            x = 20 * self.width - 160
            y = 20 * self.height
            # 设置文字位置
            glRasterPos2f(x, y)
            # 显示祝福语
            c = str('Winner Winner! Chicken Diner!')
            for cc in c:
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(cc))

        # 绘制地图
        glColor3f(0.0, 0.0, 0.0)
        for i in range(1, self.width):
            glBegin(GL_LINES)
            glVertex2f(40 * i, 0, )
            glVertex2f(40 * i, 40 * self.height)
            glEnd()

        for j in range(1, self.height):
            glBegin(GL_LINES)
            glVertex2f(0, 40 * j)
            glVertex2f(40 * self.width, 40 * j)
            glEnd()

        glutSwapBuffers()

        print("found>>>>>" + str(self.haveFound))

    # 绘制🚩标记，一个三角形表示旗帜，一条线表示旗杆
    def drawFlag(self, row, col):
        glColor3f(1.0, 0.0, 0.0)
        # 格子左上角坐标
        x0 = 40 * (col - 1)
        y0 = 40 * ( self.height - row + 1)
        # 画三角形，旗帜
        glBegin(GL_TRIANGLES)
        glVertex2f(x0 + 10, y0 - 20)
        glVertex2f(x0 + 10, y0 - 5)
        glVertex2f(x0 + 30, y0 - 20)
        glEnd()
        # 画线，旗杆
        glBegin(GL_LINES)
        glVertex2f(x0 + 10, y0 - 20)
        glVertex2f(x0 + 10, y0 - 35)
        glEnd()

    # 画数字
    def drawNumber(self, row, col):
        # 旗子左上角坐标
        x0 = (col - 1) * 40
        y0 = self.height * 40 - (row - 1) * 40
        glColor3f(0.8, 0.8, 0.8)
        # 画一个正方形代替原来的格子，颜色比背景深，表示已经点开
        glBegin(GL_POLYGON)
        glVertex2f(x0, y0)
        glVertex2f(x0, y0 - 40)
        glVertex2f(x0 + 40, y0 - 40)
        glVertex2f(x0 + 40, y0)
        glEnd()
        glColor3f(0.18, 0.54, 0.34)
        # 设置数字的位置
        x = x0 + 17
        y = y0 - 25
        # 绘制数字
        glRasterPos2f(x, y)
        if self.mineMap.mines[row][col] != 0:
            c = str(self.mineMap.mines[row][col])
            for cc in c:
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(cc))

    # 递归拓展没有地雷的区域
    def multiplicate(self, row, col):
        # 标记视图点开
        self.view[row][col] = 1
        self.haveFound += 1
        # 遍历周围的格子
        if ((row - 1) >= 1) & ((row - 1) <= self.height) & ((col - 1) >= 1) & ((col - 1) <= self.width):
            # 如果此格子没有点开，且周围地雷书为零，进行递归后续代码相同
            if (self.view[row - 1][col - 1] == 0) & (self.mineMap.mines[row - 1][col - 1] == 0):
                self.multiplicate(row - 1, col - 1)
            # 此格子没有点开，周围有地雷，不对它进行递归，只是将他点开，后续代码相同
            elif (self.view[row - 1][col - 1] == 0) & (self.mineMap.mines[row - 1][col - 1] > 0):
                self.view[row - 1][col - 1] = 1
                self.haveFound += 1
        if ((row - 1) >= 1) & ((row - 1) <= self.height) & (col >= 1) & (col <= self.width):
            if (self.view[row - 1][col] == 0) & (self.mineMap.mines[row - 1][col] == 0):
                self.multiplicate(row - 1, col)
            elif (self.view[row - 1][col] == 0) & (self.mineMap.mines[row - 1][col] > 0):
                self.view[row - 1][col] = 1
                self.haveFound += 1
        if ((row - 1) >= 1) & ((row - 1) <= self.height) & ((col + 1) >= 1) & ((col + 1) <= self.width):
            if (self.view[row - 1][col + 1] == 0) & (self.mineMap.mines[row - 1][col + 1] == 0):
                self.multiplicate(row - 1, col + 1)
            elif (self.view[row - 1][col + 1] == 0) & (self.mineMap.mines[row - 1][col + 1] > 0):
                self.view[row - 1][col + 1] = 1
                self.haveFound += 1
        if (row >= 1) & (row <= self.height) & ((col - 1) >= 1) & ((col - 1) <= self.width):
            if (self.view[row][col - 1] == 0) & (self.mineMap.mines[row][col - 1] == 0):
                self.multiplicate(row, col - 1)
            elif (self.view[row][col - 1] == 0) & (self.mineMap.mines[row][col - 1] > 0):
                self.view[row][col - 1] = 1
                self.haveFound += 1
        if (row >= 1) & (row <= self.height) & ((col + 1) >= 1) & ((col + 1) <= self.width):
            if (self.view[row][col + 1] == 0) & (self.mineMap.mines[row][col + 1] == 0):
                self.multiplicate(row, col + 1)
            elif (self.view[row][col + 1] == 0) & (self.mineMap.mines[row][col + 1] > 0):
                self.view[row][col + 1] = 1
                self.haveFound += 1
        if ((row + 1) >= 1) & ((row + 1) <= self.height) & ((col - 1) >= 1) & ((col - 1) <= self.width):
            if (self.view[row + 1][col - 1] == 0) & (self.mineMap.mines[row + 1][col - 1] == 0):
                self.multiplicate(row + 1, col - 1)
            elif (self.view[row + 1][col - 1] == 0) & (self.mineMap.mines[row + 1][col - 1] > 0):
                self.view[row + 1][col - 1] = 1
                self.haveFound += 1
        if ((row + 1) >= 1) & ((row + 1) <= self.height) & (col >= 1) & (col <= self.width):
            if (self.view[row + 1][col] == 0) & (self.mineMap.mines[row + 1][col] == 0):
                self.multiplicate(row + 1, col)
            elif (self.view[row + 1][col] == 0) & (self.mineMap.mines[row + 1][col] > 0):
                self.view[row + 1][col] = 1
                self.haveFound += 1
        if ((row + 1) >= 1) & ((row + 1) <= self.height) & ((col + 1) >= 1) & ((col + 1) <= self.width):
            if (self.view[row + 1][col + 1] == 0) & (self.mineMap.mines[row + 1][col + 1] == 0):
                self.multiplicate(row + 1, col + 1)
            elif (self.view[row + 1][col + 1] == 0) & (self.mineMap.mines[row + 1][col + 1] > 0):
                self.view[row + 1][col + 1] = 1
                self.haveFound += 1





