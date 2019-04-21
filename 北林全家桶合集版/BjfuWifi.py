# -*- coding: utf-8 -*-
# author: xzy103
# ver: 1.1(190418)

import requests
import time
import pywifi
import sys
import bs4
import ctypes
import os
import win32api
import win32con
from retry import retry


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


# 查询账户信息模块
class BJFUINFO(object):
    def __init__(self, *args):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '87',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '202.204.122.1',
            'Origin': 'http://202.204.122.1',
            'Referer': 'http://202.204.122.1/index.jsp',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(headers)

        # get ip
        s = bs4.BeautifulSoup(self.session.get(url).content, 'html.parser')
        self.ip = s.find("input", {"name": "ip"})["value"]
        self.url2 = url2+self.ip+'&action=connect'

        if len(sys.argv) > 1:
            self.username = sys.argv[1]
            self.password = sys.argv[2]
        else:
            self.username = args[0]
            self.password = args[1]

    @retry(tries=3, delay=1)
    def login(self):
        postdata = {
            'username': self.username,
            'password': self.password,
            'ip': self.ip,
            'action': 'admin'
        }
        self.session.post(url1, data=postdata)

    @retry(tries=3, delay=1)
    def disconnect(self):
        self.session.get(url3+self.userid+'&ip='+self.ip+'&type=2')

    @retry(tries=3, delay=1)
    def connect(self):
        # get userid
        userid = ''
        r = self.session.get(self.url2)
        idinfo = r.text.find("userid=")
        for i in range(7, 13):
            userid = userid+r.text[int(idinfo)+i]
        self.userid = userid

        # build the url
        self.url3 = url3+self.userid+'&ip='+self.ip+'&type=2'
        self.session.get(self.url3)

    @retry(tries=3, delay=1)
    def info(self):
        soup = bs4.BeautifulSoup(self.session.get(self.url3).content, "html.parser")
        information = soup.find_all("td", {"class": "left_bt2"})
        info_m = soup.find_all("td", {"class": "form_td_middle"})
        tfree = info_m[4].text.strip()  # 总的免费流量
        free = info_m[6].text.strip()  # 总的基础流量
        tbase = info_m[8].text.strip()
        base = info_m[10].text.strip()
        ttotal = float(tfree.split()[0])+float(tbase.split()[0])
        total = float(free.split()[0])+float(base.split()[0])
        persent = str(round(100*total/ttotal, 2)) + '%'

        print(information[0].text.strip())
        print("用户类型：", info_m[0].text.strip())
        print("账户余额：", info_m[2].text.strip())
        print("剩余免费流量：", free)
        print("剩余基础流量：", base)
        print("总流量剩余：", persent)


# 连接bjfu wifi
def connect_bjfu(ifaces):
    pcolor.printGreen(">>>>>正在尝试连接bjfu wifi...")
    profile = pywifi.Profile()  # 配置文件
    profile.ssid = "bjfu-wifi"  # wifi名称
    profile.auth = pywifi.const.AUTH_ALG_OPEN  # 需要密码
    profile.akm.append(pywifi.const.AKM_TYPE_NONE)  # 加密类型
    profile.cipher = pywifi.const.CIPHER_TYPE_NONE  # 加密单元
    ifaces.connect(profile)  # 连接
    time.sleep(1)  # 尝试1秒能否成功连接
    if ifaces.status() == pywifi.const.IFACE_CONNECTED:
        pcolor.printGreen(">>>>>连接成功！")
    else:
        pcolor.printRed(">>>>>bjfu wifi连接失败！")
        time.sleep(2)
        sys.exit()


# 检测bjfu wifi连接状态
def is_bjfu_connected():
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    if ifaces.status() == pywifi.const.IFACE_CONNECTED:
        pcolor.printGreen(">>>>>已连接bjfu wifi!")
    else:
        pcolor.printYellow(">>>>>未连接bjfu wifi，尝试连接...")
        connect_bjfu(ifaces)


# 验证是否可以上网
@retry(tries=5, delay=1)
def check():
    r = requests.get("https://www.baidu.com")
    r.raise_for_status()
    pcolor.printGreen(">>>>>恭喜您已成功连接并登录bjfu wifi!")


# 登录bjfu
def login_bjfu():
    result_list = get_url.split('&')  # get_url在is_bjfu_login函数中被定义为全局变量
    ps = []  # ps -> [p1, p2, p3, switch_url]
    for item in result_list:
        p = item.split('=')
        ps.append(p[-1])

    put_url = f'{ps[-1]}?p1=3&p2={ps[1]}&p3={ps[2]}'
    post_data = {
        'p1': '3',
        'p2': ps[1],
        'p3': ps[2],
        'p4': '0',
        'p5': UserName,
        'p6': PassWord,
        'p7': '0',
        'PtUser': UserName,
        'PtPwd': PassWord,
        'PtButton': 'logon'
    }
    requests.post(put_url, data=post_data)
    pcolor.printGreen(">>>>>表单信息提交成功，正在验证...")
    try:
        check()
    except:
        pcolor.printRed(">>>>>登录失败，请手动登录！")
        time.sleep(2)
        sys.exit()


# 检测bjfu登录状态
def is_bjfu_login():
    url = 'http://202.204.122.1/index.jsp'
    result = requests.get(url)
    global get_url
    get_url = result.url
    if get_url == url:
        pcolor.printGreen(">>>>>当前您已登录bjfu，无需重复登录...")
    else:
        pcolor.printYellow(">>>>>当前您未登录bjfu，尝试登录...")
        login_bjfu()


# 获取bjfu账户信息
def get_account_info():
    global url, url1, url2, url3
    url = 'http://202.204.122.1/index.jsp'
    url1 = 'http://202.204.122.1/checkLogin.jsp'
    url2 = 'http://202.204.122.1/user/index.jsp?ip='
    url3 = 'http://202.204.122.1/user/network/connect_action.jsp?userid='
    bjfu = BJFUINFO(UserName, PassWord)
    try:
        bjfu.login()
        bjfu.connect()
        bjfu.info()
    except:
        pass


# 获取账户信息
def get_user_info():
    if os.path.isfile('userinfo') is True:
        with open('userinfo', 'r') as f:
            Usn = f.readline()[:-1]
            Psw = f.readline()[:-1]
    else:
        with open('userinfo', 'w') as f:
            pcolor.printGreen(">>>>>初次使用需初始化账号和密码！")
            Usn = input('>>>>>请输入bjfu校园网账号：')
            Psw = input('>>>>>请输入bjfu校园网密码：')
            f.write(Usn + '\n' + Psw + '\n')
            win32api.SetFileAttributes('userinfo', win32con.FILE_ATTRIBUTE_HIDDEN)
    return Usn, Psw


def main():
    global pcolor, UserName, PassWord
    pcolor = PyColor()
    UserName, PassWord = get_user_info()
    t0 = time.time()

    pcolor.printGreen(">>>>>北林全家桶 | bjfu wifi一键登录 | Ver:1.1")
    pcolor.printGreen(">>>>>开始运行...")
    is_bjfu_connected()  # 是否连接bjfu wifi
    is_bjfu_login()  # 是否登录bjfu
    get_account_info()  # 获取账户信息
    pcolor.printGreen(">>>>>结束运行！")

    pcolor.printGreen("本次运行用时：{:.2f}s".format(time.time()-t0))
    input('>>>>>任意键继续...')


if __name__ == '__main__':
    pcolor = PyColor()
    UserName, PassWord = get_user_info()
    t0 = time.time()

    pcolor.printGreen(">>>>>北林全家桶 | bjfu wifi一键登录 | Ver:1.1")
    pcolor.printGreen(">>>>>开始运行...")
    is_bjfu_connected()  # 是否连接bjfu wifi
    is_bjfu_login()  # 是否登录bjfu
    get_account_info()  # 获取账户信息
    pcolor.printGreen(">>>>>结束运行！")

    pcolor.printGreen("本次运行用时：{:.2f}s".format(time.time()-t0))
    input()
    sys.exit()
