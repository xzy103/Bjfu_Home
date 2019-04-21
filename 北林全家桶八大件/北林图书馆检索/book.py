# -*- coding:UTF-8 -*-
# Author: xzy103
# Ver: 1.0(190418)

import ctypes
import sys
import os
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
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


def search():
    url = 'http://222.28.112.187:8080/opac/openlink.php?title={}&onlylendable={}&displaypg=1000'.format(word, only)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        lis = soup.ol.find_all('li')
    except:
        pc.printYellow('本馆没有您检索的图书')
        input('>>>>>任意键继续...')
        return None
    global books
    books = [['标题', '状态', '页面链接', '作者', '出版社']]
    for li in lis:
        title = li.h3.a.text.strip()
        lendable = li.p.span.text.strip().replace(' ', '').replace('\n', '').replace('\r', '')
        bookurl = li.h3.a['href']
        temp = lendable.split('\t')
        author = li.p.text.replace(' ', '').replace('\n', '').replace('\r', '')
        author = author.replace(temp[0], '').replace(temp[-1], '')[:-5]
        author = author.strip().split('\t')
        books.append([title, lendable, bookurl, author[0], author[-1]])
    result = ''
    for book in books[1:]:
        status = '[可\xa0\xa0借]' if int(book[1].split('可借复本：')[-1]) else '[不可借]'
        if tit == 'yes':
            content = '-'*80+'\n'+book[0]+'\n'+status+'\t'+book[3]+'\n'+book[-1]
        else:
            content = status+'\t'+book[0]
        result += content + '\n'
    return result


def position(turl):
    r = requests.get(turl)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    local = soup.find_all('tr', {'align': "left"})
    loc_urls = []
    for tr in local:
        a = tr.find_all('a')
        if a:
            loc_urls.append(a[0]['href'])
    areas = []
    for loc in loc_urls:
        r = requests.get(loc)
        soup = BeautifulSoup(r.text, "html.parser")
        area = soup.find_all('script')[2].text.split('=')[3].split('|')[-1].split('"')[0].strip()
        if area:
            areas.append(area)
    return '\n'.join(set(areas)) if areas else '当前图书未上架 无法定位！'


def details():
    pc.printGreen('>>>>>该图书详情信息')
    burl = 'http://222.28.112.187:8080/opac/'+books[n][2]
    r = requests.get(burl)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html, "lxml")

    dls = soup.find('div', {'id': 'item_detail'}).find_all('dl')
    attrs = [['属性名', '属性']]
    for dl in dls:
        if dl.dt.string and dl.dd.text:
            new = dl.dd.text if len(dl.dd.text) < 30 else dl.dd.text.replace('，', '，\n').replace('。', '。\n').replace('.', '.\n').replace(';', ';\n')
            attrs.append([str(dl.dt.string), str(new)])
    table = PrettyTable(attrs[0])
    for attr in attrs[1:]:
        table.add_row(attr)
    table.align = 'l'
    print(table)

    local = soup.find_all('tr', {'align': "left"})
    locals = []
    for tr in local:
        it = tr.text.strip().replace('\n', '').split()
        it[-1] = it[-1][:-2]
        locals.append(it)

    for i in range(len(locals)):
        if len(locals[0]) != len(locals[i]):
            locals[i].insert(2, '-')

    table2 = PrettyTable(locals[0])
    for lc in locals[1:]:
        table2.add_row(lc)
    table2.align = 'l'
    pc.printGreen('>>>>>该图书馆藏信息')
    print(table2)

    pc.printGreen('>>>>>该图书所在位置')
    print(position(burl))


def data():
    try:
        data_url = 'http://222.28.112.167/datashow/index_a.php'
        r = requests.get(data_url)
        soup = BeautifulSoup(r.text, "html.parser")
        data_temp = soup.find('div', {'class': 'div_dataleft'})
        datas = data_temp.find_all('tr')
        rows = []
        for tr in datas:
            row = []
            td = tr.find_all('td')
            for t in td:
                row.append(t.text)
            rows.append(row)
        print('截至到今天', time.strftime("%H:%M:%S"))
        print('北林图书馆入馆数据')
        pt = PrettyTable(rows[1])
        pt.add_row(rows[2])
        pt.add_row(rows[-1])
        print(pt)
    except:
        pc.printYellow('获取当前数据失败，可能是因为您未使用校园网。')
        pc.printYellow('这并不影响您接下来的使用')


def model():
    print('1 [全部结果+详情]模式', '2 [全部结果+标题]模式', '3 [可借结果+标题]模式(推荐)', '4 [可借结果+详情]模式', sep='\n')
    select = input('请输入对应模式序号：')
    global only, tit
    only = 'yes' if select in ['3', '4'] else 'no'  # 全部结果or可借
    tit = 'yes' if select in ['1', '4'] else 'no'  # 标题or详情


if __name__ == '__main__':
    pc = PyColor()
    pc.printGreen("北林全家桶 | 北林图书馆信息查询 | Ver:1.0")
    pc.printGreen(">>>>>获取当前数据...")
    data()
    pc.printGreen('\n{:-^80}\n'.format('检索模式'))
    model()
    while True:
        word = input('请输入检索关键词：')
        pc.printGreen('>>>>>正在检索...')
        resultxt = search()
        while resultxt:
            os.system('cls')
            pc.printGreen('>>>>>检索结果')
            print(resultxt)

            pc.printGreen('\n序号->该图书详情\nx   ->退出程序\nm   ->重新选择检索模式\nr   ->重新开始检索')
            n = input('请输入对应提示：')
            if n == 'x':
                pc.printGreen('>>>>>程序结束...')
                time.sleep(2)
                sys.exit()
            elif n == 'm':
                model()
                resultxt = search()
                continue
            elif n == 'r':
                os.system('cls')
                break
            else:
                try:
                    n = int(n)
                except:
                    pc.printRed('您的输入非法！')
                    break
                details()

            pc.printGreen('\n回车->返回检索结果界面\nx   ->退出程序\nm   ->重新选择检索模式\nr   ->重新开始检索')
            flag = input('请输入对应提示：')
            if flag == 'x':
                pc.printGreen('>>>>>程序结束...')
                time.sleep(2)
                sys.exit()
            elif flag == 'm':
                model()
                resultxt = search()
                continue
            elif flag == 'r':
                os.system('cls')
                break

