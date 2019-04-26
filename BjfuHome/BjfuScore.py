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
url_score = 'http://newjwxt.bjfu.edu.cn/jsxsd/kscj/cjcx_list'


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
        pc.printGreen('账号信息：'+info)

    def write(self):
        with open("score.txt", "w") as fw:
            fw.write(str(self.score))

    def saveclasses(self):
        r = self.session.get(url_score)
        soup = bs(r.content, "html.parser")

        score, title = [], []
        self.score = score
        trs = soup.find('table', {'id': 'dataList'}).find_all('tr')
        for th in trs[0].find_all('th'):
            title.append(th.string.strip())
        score.append(title)
        for i in range(1, len(trs)):
            ls = []
            for td in trs[i].find_all('td'):
                txt = td.text.strip().replace('Ⅰ', '1').replace('Ⅱ', '2')
                ls.append(txt)
            score.append(ls)
        table = PrettyTable(score[0])
        for i in range(1, len(score)):
            table.add_row(score[i])
        pc.printGreen('>>>>>成绩详情')
        print(table)
        print()

        grade = soup.find_all('div', {'class': 'Nsb_pw'})
        grade = grade[2].text
        grade = grade.split('在本查询时间段，')[-1].split('所得学分详情')[0]
        grade = grade.replace("\t", '').replace('\r', '').replace('、\n', '').strip()
        print(grade)
        print()
        
        t1, t2, t3 = [], [], []
        trs = soup.find_all('table', {'id': 'dataList'})[1].find_all('tr')
        for th in trs[0].find_all('th'):
            t1.append(th.string.strip())
        for th in trs[1].find_all('th'):
            t2.append(th.string.strip())
        for td in trs[-1].find_all('td'):
            t3.append(td.string.strip())
        t2[0], t2[3] = '专选总计', '公选总计'
        table2 = PrettyTable(t1[:3]+t2)
        table2.add_row(t3)
        pc.printGreen('>>>>>学分详情')
        print(table2)
        print()

        rank, title2 = [], []
        trs = soup.find_all('table', {'id': 'dataList'})[2].find_all('tr')
        for th in trs[0].find_all('th'):
            title2.append(th.string.strip())
        rank.append(title2)
        for i in range(1, len(trs)):
            ls = []
            for td in trs[i].find_all('td'):
                txt = td.text.strip()
                ls.append(txt)
            rank.append(ls)
        table3 = PrettyTable(rank[0])
        for i in range(1, len(rank)):
            table3.add_row(rank[i])
        pc.printGreen('>>>>>排名详情')
        print(table3)
        print()

        if os.path.isfile('score.txt') is False:
            self.write()
            pc.printGreen('>>>>>成绩信息已保存')
        with open('score.txt', "r") as fr:
            content = eval(fr.read())
            win32api.SetFileAttributes('score.txt', win32con.FILE_ATTRIBUTE_NORMAL)
        if content == score:
            pc.printGreen('当前是最新成绩！')
        else:
            pc.printYellow('成绩有更新！')
            table_new = PrettyTable(score[0])
            for sc in score:
                if sc not in content:
                    table_new.add_row(sc)
            pc.printYellow('>>>>>更新的成绩为：')
            pc.printYellow(str(table_new))
            pc.printGreen('>>>>>成绩信息已更新')
        self.write()
        win32api.SetFileAttributes('score.txt', win32con.FILE_ATTRIBUTE_HIDDEN)


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
    global pc
    pc = PyColor()
    pc.printGreen("北林全家桶 | 教务系统成绩查询 | Ver:1.0")
    pc.printGreen(">>>>>开始运行...")
    UserName, PassWord = get_user_info()
    new = Newjwxt(UserName, PassWord)
    new.login()
    new.info()
    new.saveclasses()
    pc.printGreen(">>>>>运行结束！")
    input('>>>>>任意键继续...')


if __name__ == '__main__':
    pc = PyColor()
    pc.printGreen("北林全家桶 | 教务系统成绩查询 | Ver:1.0")
    pc.printGreen(">>>>>开始运行...")
    UserName, PassWord = get_user_info()
    new = Newjwxt(UserName, PassWord)
    new.login()
    new.info()
    new.saveclasses()
    pc.printGreen(">>>>>运行结束！")
    input()
    sys.exit()
