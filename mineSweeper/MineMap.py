# -*- coding: UTF-8 -*-
import random


# 地图类
class MineMap:
    def __init__(self, level):
        # 根据级别设置地图规格以及地雷数量
        if level == 1:
            self.height = 9
            self.width = 9
            self.mineNum = 10
        elif level == 2:
            self.height = 16
            self.width = 16
            self.mineNum = 40
        elif level == 3:
            self.height = 16
            self.width = 30
            self.mineNum = 99
        # 需要点开的数量
        self.findout = self.height * self.width - self.mineNum
        # 二维数组记录地图
        self.mines = [([0] * (self.width + 2)) for p in range(self.height + 2)]
        # 随机生成地雷位置
        self.createMines()
        self.creatMap()
        for m in self.mines:
            print(m)
            print('\n')

    # 随机生成地雷位置
    def createMines(self):
        count = 0
        while count < self.mineNum:
            print(count)
            # 随机生成地雷位置的行列数
            row = random.randint(1, self.height)
            col = random.randint(1, self.width)
            # 此位置没有地雷，则放一颗地雷
            if self.mines[row][col] == 0:
                self.mines[row][col] = -1
                print(self.mines[row][col])
                count += 1

    # 计算每个格子周围的地雷书，填到地图中
    def creatMap(self):
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                if self.mines[i][j] != -1:
                    self.mines[i][j] = self.getMineAround(i, j)

    # 判断此位置是否为地雷
    def isMine(self, row, col):
        if self.mines[row][col] == -1:
            return True
        return False

    # 计算此格子周围地雷数量
    def getMineAround(self, row, col):
        num = 0
        if self.mines[row - 1][col - 1] == -1:
            num += 1
        if self.mines[row - 1][col] == -1:
            num += 1
        if self.mines[row - 1][col + 1] == -1:
            num += 1
        if self.mines[row][col - 1] == -1:
            num += 1
        if self.mines[row][col + 1] == -1:
            num += 1
        if self.mines[row + 1][col - 1] == -1:
            num += 1
        if self.mines[row + 1][col] == -1:
            num += 1
        if self.mines[row + 1][col + 1] == -1:
            num += 1
        return num



