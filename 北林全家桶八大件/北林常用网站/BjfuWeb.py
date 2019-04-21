# -*- coding:UTF-8 -*-
# Author: xzy103
# Ver: 1.0(190418)

import os
import ctypes
import sys


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


pc = PyColor()
pc.printGreen("北林全家桶 | 北林常用网站集合 | Ver:1.0")
pc.printGreen(">>>>>>开始运行...")
pc.printYellow("提示：如果网页无法打开，可能是因为没有使用校园网。")
webs = [
    ['北林官方主页', 'http://www.bjfu.edu.cn/'],
    ['北林教务处', 'http://jwc.bjfu.edu.cn/'],
    ['教务系统', 'http://newjwxt.bjfu.edu.cn/'],
    ['教学平台', 'http://202.204.121.133/meol/index.do'],
    ['北林VPN', 'https://vpn.bjfu.edu.cn/'],
    ['网络计费系统', 'http://202.204.122.1/'],
    ['数字北林', 'http://cas.bjfu.edu.cn/cas/login'],
    ['二课堂认证', 'http://qq.bjfu.edu.cn/XueSheng/All_Activities.aspx'],
    ['北林图书馆', 'http://lib.bjfu.edu.cn/'],
    ['北林经管院', 'http://em.bjfu.edu.cn/'],
    ['校历查询', 'http://v6.bjfu.edu.cn/dcp/dcp/apps/bjfu/calendar/html/bjfuCalendar.html'],
    ['北林邮箱', 'http://mail.bjfu.edu.cn'],
    ['北林MOOC', 'https://www.icourse163.org/university/BJFU#/c'],
    ['北林学生处', 'http://xsc.bjfu.edu.cn/'],
    ['阳光长跑系统', 'http://bjfu.sunnysport.org.cn/']
]

for web in range(len(webs)):
    print(f'{web:2}', webs[web][0], sep=' | ')

while True:
    n = eval(input("\n请输入对应的序号查看："))
    if (not isinstance(n, int)) or (n > len(webs)-1):
        pc.printRed("您的输入有误，请重新输入！")
        continue
    name = webs[n][0]
    url = webs[n][-1]
    new_name = name+'.url'

    with open(name, "w") as fweb:
        fweb.write("[InternetShortcut]\n"+'URL='+url)

    os.rename(name, new_name)
    os.system(new_name)
    os.remove(new_name)
    pc.printGreen(f"已为您打开{name}！")
