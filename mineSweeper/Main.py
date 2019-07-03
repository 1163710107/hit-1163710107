# _*_ coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from mineSweeper.MineSweeper import MineSweeper

class OpenGLWindow:
    # 初始化

    def __init__(self, title=b'MineSweeper'):
        self.click = 0
        # 传递命令行参数
        glutInit(sys.argv)
        # 设置显示模式
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        # 设置窗口大小
        glutInitWindowSize(200, 130)
        # 设置窗口位置
        glutInitWindowPosition(500, 250)
        # 创建窗口
        self.window = glutCreateWindow(title)
        # 设置场景绘制函数
        glutDisplayFunc(self.Draw)
        # 调用OpenGL初始化函数
        glClearColor(0.0, 0.0, 0.0, 0.0)

        #添加鼠标监听
        glutMouseFunc(self.mouseClick)

    # 绘制场景
    def Draw(self):
        # 清除屏幕和深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # 移动位置
        glTranslatef(0.0, 0.0, -1.0)
        # 设置颜色为绿色
        glColor3f(0.0, 1.0, 0.0)
        # 定位文字
        glRasterPos2f(-0.15, 0.5)
        # 绘制文字
        self.DrawText('EASY')
        # 定位文字
        glRasterPos2f(-0.15, 0)
        # 绘制文字
        self.DrawText('NORMAL')
        # 定位文字
        glRasterPos2f(-0.15, -0.5)
        # 绘制文字
        self.DrawText('HARD')
        # 交换缓存
        glutSwapBuffers()


    # 绘制文字函数
    def DrawText(self, string):
        # 循环处理字符串
        for c in string:
            # 输出文字
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))

    # 监听鼠标点击事件
    def mouseClick(self, btn, state, x, y):
        # 这里的鼠标监听存在一些问题，左键在按下和抬起得到的参数都为左键、按下
        # 因此一次点击会触发两次事件，所以添加了click记录点击次数，二的倍数时触发
        if btn == GLUT_LEFT_BUTTON & state == GLUT_DOWN:
            self.click += 1
            if self.click %2 == 0:
                # 根据鼠标纵坐标确定选取模式（简单、普通、困难）
                print("x>>>>" + str(x) + "y>>>" + str(y))
                if y < 45:
                    game = MineSweeper(1)
                    game.MainLoop()
                elif y < 85:
                    game = MineSweeper(2)
                    game.MainLoop()
                else:
                    game = MineSweeper(3)
                    game.MainLoop()



    def MainLoop(self):
        # 进入消息循环
        glutMainLoop()


# 创建窗口
window = OpenGLWindow()
# 进入消息循环
window.MainLoop()