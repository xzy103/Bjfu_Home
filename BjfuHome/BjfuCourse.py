# -*- coding:UTF-8 -*-
# Author: xzy103
# Ver: 1.0(190418)

import os
import ctypes
import sys
import requests
import win32api
import win32con
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable
import csv
import time

url_start = 'http://newjwxt.bjfu.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL'  # GET
url_main = 'http://newjwxt.bjfu.edu.cn/jsxsd/framework/xsMain.jsp'  # GET
url_login = 'http://newjwxt.bjfu.edu.cn/jsxsd/xk/LoginToXk'  # POST
url_classes = 'http://newjwxt.bjfu.edu.cn/jsxsd/xskb/xskb_list.do'


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
    def printGreen(self, mess, end='\n'):
        self.set_cmd_text_color(self.FOREGROUND_GREEN)
        sys.stdout.write(mess+end)
        self.resetColor()

    # red
    def printRed(self, mess, end='\n'):
        self.set_cmd_text_color(self.FOREGROUND_RED)
        sys.stdout.write(mess+end)
        self.resetColor()

    # yellow
    def printYellow(self, mess, end='\n'):
        self.set_cmd_text_color(self.FOREGROUND_YELLOW)
        sys.stdout.write(mess+end)
        self.resetColor()


# 登录教务系统
class Newjwxt(object):
    def __init__(self, username, password):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'newjwxt.bjfu.edu.cn',
            'Referer': 'http://newjwxt.bjfu.edu.cn/Logon.do?method=logon',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.get(url_start)
        self.username = username
        self.password = password

    def login(self):
        postdata = {
            'USERNAME': self.username,
            'PASSWORD': self.password
        }
        self.session.post(url_login, data=postdata)
        if self.session.get(url_main).status_code == 200:
            pc.printGreen(">>>>>登录成功!")
            return self.session
        else:
            pc.printYellow(">>>>>登录失败!")
            time.sleep(3)
            sys.exit()

    def info(self):
        r = self.session.get(url_main)
        soup = bs(r.content, "html.parser")
        basic_info = soup.find_all("div", {"class": "Nsb_top_menu_nc"})
        info = basic_info[0].text.strip()
        pc.printGreen('账号信息： '+info)

    def write(self):
        with open("course.txt", "w") as fw2:
            fw2.write(str(self.course))

    def saveclasses(self):
        r = self.session.get(url_classes)
        soup = bs(r.content, "html.parser")

        ############################################################################
        course = [[], [], [], [], [], [], [], [], []]
        self.course = course
        trs = soup.find('table', {'id': 'kbtable'}).find_all('tr')
        for t in trs[0].find_all('th'):
            course[0].append(t.string.strip('\xa0').strip())

        for i in range(1, len(trs)):
            for t in trs[i].find_all('th'):
                course[i].append(t.string.strip())
            for div in trs[i].find_all("div", {"class": "kbcontent"}):
                txt = div.text.strip('\xa0').strip()
                txt = txt.replace('---------------------', '\n')
                txt = txt.replace('(专选)', '(专选)\n')
                txt = txt.replace('(必修)', '(必修)\n')
                txt = txt.replace('(周)', '(周)\n')
                txt = txt.replace('(python)', '')
                txt = txt+'\n'
                course[i].append(txt)

        for t in trs[-1].find_all('td'):
            course[-1].append(t.string.strip(';').strip().replace(' ;', '; '))

        ############################################################################
        table = PrettyTable(course[0])
        for i in range(1, len(course)-1):
            table.add_row(course[i])
        print(table)
        print(course[-1][0], course[-1][-1], '\n')
        ############################################################################

        if os.path.isfile('course.txt') is False:
            self.write()
            pc.printGreen('>>>>>课程信息已保存')

        with open('course.txt', "r") as fr:
            content = eval(fr.read())
            win32api.SetFileAttributes('course.txt', win32con.FILE_ATTRIBUTE_NORMAL)

        if content == course:
            pc.printGreen('当前已是最新课表！')
        else:
            pc.printYellow('课表有更新！')
            for z in zip(course, content):
                if z[0] == z[-1]:
                    continue
                else:
                    for j in enumerate(zip(z[0], z[-1])):
                        if j[-1][0] != j[-1][-1]:
                            pc.printYellow(course[0][j[0]]+z[0][0])
                            pc.printYellow('更新前：', j[-1][-1].strip().replace('\n', '  '))
                            pc.printYellow('更新后：', j[-1][0].strip().replace('\n', '  '))
                            print()
            pc.printGreen('>>>>>课程信息已更新')
        self.write()
        win32api.SetFileAttributes('course.txt', win32con.FILE_ATTRIBUTE_HIDDEN)


# 获取账户信息
def get_user_info():
    if os.path.isfile('jwxtinfo') is True:
        with open('jwxtinfo', 'r') as f:
            Usn = f.readline()[:-1]
            Psw = f.readline()[:-1]
    else:
        with open('jwxtinfo', 'w') as f:
            pc.printGreen(">>>>>初次使用需初始化账号和密码")
            Usn = input('>>>>>请输入教务系统账号：')
            Psw = input('>>>>>请输入教务系统密码：')
            f.write(Usn + '\n' + Psw + '\n')
            win32api.SetFileAttributes('jwxtinfo', win32con.FILE_ATTRIBUTE_HIDDEN)
    return Usn, Psw


def main():
    global pc, UserName, PassWord
    pc = PyColor()
    pc.printGreen("北林全家桶 | 教务系统课表查询 | Ver:1.0")
    pc.printGreen(">>>>>开始运行...")
    UserName, PassWord = get_user_info()
    new = Newjwxt(UserName, PassWord)
    new.login()
    new.info()
    new.saveclasses()
    pc.printGreen(">>>>>运行结束！")
    input('>>>>>任意键继续...')
    time.sleep(1)


if __name__ == '__main__':
    pc = PyColor()
    pc.printGreen("北林全家桶 | 教务系统课表查询 | Ver:1.0")
    pc.printGreen(">>>>>开始运行...")
    UserName, PassWord = get_user_info()
    new = Newjwxt(UserName, PassWord)
    new.login()
    new.info()
    new.saveclasses()
    pc.printGreen(">>>>>运行结束！")
    input()
    sys.exit()
