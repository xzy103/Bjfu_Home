# -*- coding:UTF-8 -*-
# Author: xzy103
# Ver: 1.0(190416)

from selenium import webdriver
from time import sleep
import os
import win32api
import win32con
import sys
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


# 读取csv文件中的邮箱信息
def read_csv():
    lrs = []
    fr = open("MailInfo.csv", "r")
    for line in fr:
        line = line.replace("\n", "")
        lrs.append(line.split(","))
    fr.close()
    return lrs


# 将邮箱信息写入邮箱
def write_csv():
    fw = open("MailInfo.csv", "a")  # w为创建写，a为追加写
    name = input(">>>请输入邮箱名称：")
    usn_raw = input(">>>请输入完整邮箱账号：")
    psw = input(">>>请输入邮箱密码：")
    usn = usn_raw[:-8]
    if usn_raw.endswith('@163.com'):
        mail_type = 'http://mail.163.com'
    elif usn_raw.endswith('@126.com'):
        mail_type = 'http://mail.126.com'
    else:
        pc.printRed(">>>>>>仅支持126和163邮箱！")
        sleep(3)
        sys.exit()
    lw = []
    lw.extend([name, usn, psw, mail_type])
    fw.write(",".join(lw) + "\n")  # ",".join(lw)为生成一个新字符串，由","分隔列表lw中的元素组成
    win32api.SetFileAttributes('MailInfo.csv', win32con.FILE_ATTRIBUTE_HIDDEN)
    fw.close()


# 录入邮箱信息
def write_in():
    pc.printGreen(">>>>>>请录入邮箱信息")
    while True:
        write_csv()
        f = input("回车继续录入，输入0结束录入：")
        if f == '0':
            break
    pc.printGreen(">>>>>>信息录入结束")


# 启动浏览器
def chrome(usn, psw, url):
    # 启动浏览器
    global browser
    try:
        browser = webdriver.Chrome()
    except:
        pc.printRed("您的设备未安装chrome浏览器或未安装chromedriver.")
        pc.printYellow("将为您打开配置教程 :)")
        sleep(2)
        f = open("config", "w")
        f.write("[InternetShortcut]\n")
        f.write("URL=https://github.com/xzy103/login_126_163_mail/blob/master/config.md")
        f.close()
        os.rename("config", "config.url")
        os.system("config.url")
        os.remove("config.url")
        input()
        sys.exit()
    browser.get(url)
    browser.maximize_window()
    sleep(2)

    # 输入账号密码并登录
    browser.switch_to.frame(0)
    browser.find_element_by_name("email").send_keys(usn)
    browser.find_element_by_name("password").send_keys(psw)
    browser.find_element_by_id("dologin").click()
    pc.printGreen(">>>>>>登陆成功！")


if __name__ == '__main__':
    pc = PyColor()
    pc.printGreen("北林全家桶 | 登录126/163邮箱 | Ver:1.0")
    pc.printGreen(">>>>>>开始运行...")
    if os.path.isfile('MailInfo.csv') is False:
        with open("MailInfo.csv", "w") as fi:
            fi.write(",".join(['新增公邮或其他公邮']) + "\n")
        write_in()

    lr = read_csv()
    for i in range(len(lr)):
        print(i, lr[i][0])

    while True:
        num = eval(input("请输入需要登陆的公邮序号:"))
        if num == 0:
            write_in()
            pc.printYellow("请重新运行本程序！")
            sleep(3)
            break
        elif num <= len(lr):
            info = lr[num]
            Usn, Psw, Url = info[1], info[2], info[3]
            try:
                chrome(Usn, Psw, Url)
            except:
                pc.printRed("登陆失败！可能的原因为：网络信号差、浏览器已升级、中途手动操作浏览器等")
                sleep(3)
                sys.exit()
        else:
            pc.printRed(">>>>>>您的输入有误！")
            sleep(3)
            sys.exit()
