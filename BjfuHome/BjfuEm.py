# -*- coding:UTF-8 -*-
# Author: xzy103
# Ver: 1.0(190416)

import requests
from bs4 import BeautifulSoup
import os
import win32api
import win32con
import ctypes
import sys
import time


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


def main():
    global pc
    pc = PyColor()
    pc.printGreen("北林全家桶 | 获取经管院最新通知 | Ver:1.0")
    pc.printGreen(">>>>>>开始运行...")
    if os.path.isfile('EmInfo') is False:
        f = open("EmInfo", "w")
        f.close()
        win32api.SetFileAttributes('EmInfo', win32con.FILE_ATTRIBUTE_HIDDEN)

    with open("EmInfo", "r") as fr:
        lr = fr.readlines()

    url = 'http://em.bjfu.edu.cn/sytzgg/'
    r = requests.get(url)
    r.encoding = 'gbk'
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find_all('ul')[3]
    spans = ul.find_all("span")
    lis = ul.find_all("li")

    ls = []
    print("序号\t", "发布时间\t", "标题")
    for i in range(len(lis)):
        if lis[i].a.string+'\n' in lr:
            new = '   '
        else:
            new = 'new'
            with open('EmInfo', 'a') as fw:
                fw.write(lis[i].a.string + '\n')
        print(f"{i:<5}", spans[i].string, new, lis[i].a.string)
        ls.append(url+lis[i].a['href'])

    print("-1     结束程序")
    while True:
        n = int(input("\n请输入对应数字："))
        if n == -1:
            pc.printGreen('>>>>>>运行结束')
            time.sleep(1)
            break
        pc.printGreen("正在为您打开网页...")
        time.sleep(1)
        with open("href", "w") as f:
            f.write(f"[InternetShortcut]\nURL={ls[n]}")

        os.rename("href", "href.url")
        os.system("href.url")
        os.remove("href.url")

