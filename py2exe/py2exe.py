import sys
import os
import time
import ctypes
from easygui import fileopenbox


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


pc = PyColor()
pc.printGreen('>>>>>>打包程序开始运行...')

pc.printGreen('请选择图标文件...')
ico = fileopenbox("请选择图标文件", default='*.ico')
if ico:
    pc.printGreen('图标文件所在路径为：'+ico)
else:
    pc.printYellow('您未选择图标文件，将使用默认图标。')
    ico = ''
pc.printGreen('请选择待打包的python文件...')
py = fileopenbox("请选择python文件", default='*.py')
if py:
    pc.printGreen('python文件所在路径为：'+py)
    path = '\\'.join(py.split('\\')[:-1])
    pc.printGreen('打包程序执行路径为：' + path)
    name = py.split('\\')[-1].split('.')[0]
else:
    pc.printRed('您未选择python文件，程序将终止！')
    time.sleep(3)
    sys.exit()

with open(path+'\\py2exe', "w") as fcmd:
    cmd = f'pyinstaller -F {py}' if ico == '' else f'pyinstaller -i {ico} -F {py}'
    fcmd.write('@echo off'+'\n')
    fcmd.write(f'cd {path}'+'\n')
    fcmd.write(cmd+'\n')
    fcmd.write('move ' + path + '\\dist\\' + name + '.exe ' + path + '\n')
    fcmd.write("rd/s/q build"+'\n')
    fcmd.write('del/f/a/q '+name+'.spec' + '\n')
    fcmd.write('rd/s/q dist'+'\n')
    fcmd.write('rd/s/q __pycache__' + '\n')
    fcmd.write('del/f/a/q '+path+'\\py2exe.bat')
os.rename(path+'\\py2exe', path+'\\py2exe.bat')
t0 = time.time()
pc.printGreen('>>>>>>开始打包...')
os.system(path+'\\py2exe.bat')
pc.printGreen('>>>>>>打包结束！')
pc.printGreen(f'本次打包耗时{round(time.time()-t0, 2)}s.')
time.sleep(2)
sys.exit()
