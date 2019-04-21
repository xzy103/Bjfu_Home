# -*- coding: utf-8 -*-
# author: xzy103
# ver: 1.0(190421)

import BjfuCourse
import BjfuEm
import BjfuFtp
import BjfuLib
import BjfuMail
import BjfuScore
import BjfuWeb
import BjfuWifi
from prettytable import PrettyTable
import time
import sys
import os
import ctypes


# 命令行输出文字颜色
class PyColor(object):
    def __init__(self):
        self.STD_INPUT_HANDLE = -10
        self.STD_OUTPUT_HANDLE = -11
        self.STD_ERROR_HANDLE = -12

        # Windows CMD命令行 字体颜色定义 text colors
        self.FOREGROUND_GREEN = 0x0a  # green.
        self.FOREGROUND_RED = 0x0c  # red.
        self.FOREGROUND_BLUE = 0x09  # blue.
        self.FOREGROUND_YELLOW = 0x0e  # yellow.

        # get handle
        self.std_out_handle = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)

    def set_cmd_text_color(self, color):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_out_handle, color)
        return Bool

    # reset white
    def resetColor(self):
        self.set_cmd_text_color(self.FOREGROUND_RED | self.FOREGROUND_GREEN | self.FOREGROUND_BLUE)

    # green
    def printGreen(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_GREEN)
        sys.stdout.write(mess+'\n')
        self.resetColor()

    # red
    def printRed(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_RED)
        sys.stdout.write(mess+'\n')
        self.resetColor()

    # yellow
    def printYellow(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_YELLOW)
        sys.stdout.write(mess+'\n')
        self.resetColor()


lst = [
    ['1', '查询课表'],
    ['2', '获取经管院通知'],
    ['3', '北林常用FTP'],
    ['4', '北林图书馆检索'],
    ['5', '126/163邮箱登录'],
    ['6', '查询最新成绩'],
    ['7', '北林常用网站'],
    ['8', '一键登录校园网'],
    ['0', '退出程序']
]
pc = PyColor()
table = PrettyTable(['序号', '功能'])
for it in lst:
    table.add_row(it)
table.align = 'l'

while True:
    os.system('cls')
    pc.printGreen('>>>>>>北林全家桶 | 合集版')
    print(table)
    mode = input('请输入对应序号：')
    os.system('cls')

    if mode == '0':
        pc.printYellow('>>>>>即将退出程序')
        time.sleep(1)
        sys.exit()
    elif mode == '1':
        pc.printGreen('{:-^80}'.format(lst[0][-1]))
        time.sleep(1)
        BjfuCourse.main()
    elif mode == '2':
        pc.printGreen('{:-^80}'.format(lst[1][-1]))
        time.sleep(1)
        BjfuEm.main()
    elif mode == '3':
        pc.printGreen('{:-^80}'.format(lst[2][-1]))
        time.sleep(1)
        BjfuFtp.main()
    elif mode == '4':
        pc.printGreen('{:-^80}'.format(lst[3][-1]))
        time.sleep(1)
        BjfuLib.main()
    elif mode == '5':
        pc.printGreen('{:-^80}'.format(lst[4][-1]))
        time.sleep(1)
        BjfuMail.main()
    elif mode == '6':
        pc.printGreen('{:-^80}'.format(lst[5][-1]))
        time.sleep(1)
        BjfuScore.main()
    elif mode == '7':
        pc.printGreen('{:-^80}'.format(lst[6][-1]))
        time.sleep(1)
        BjfuWeb.main()
    elif mode == '8':
        pc.printGreen('{:-^80}'.format(lst[7][-1]))
        time.sleep(1)
        BjfuWifi.main()
    else:
        pc.printRed('非法输入！')
        print('>>>>>请重新输入...')
        time.sleep(2)
