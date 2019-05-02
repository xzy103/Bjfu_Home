# Bjfu_Home
北林全家桶 / 北林八大件  

## 功能
>1.126or163公邮登录  
>2.北林常用网站登录  
>3.北林图书馆检索  
>4.北林常用ftp下载  
>5.一键登录校园网  
>6.教务系统查成绩  
>7.教务系统查课表  
>8.获取经管院最新通知  

## 结构说明
`BjfuHomeRun.py`是打包版的主文件，集成了全家桶八大功能，依赖`BjfuHomeRun文件夹`下的各个子功能.py文件;  
`BjfuHome文件夹`中的`icos文件夹`存放的是各子功能对应的图标文件，用于打包;  
`BjfuHome文件夹`中的`py2exe文件夹`存放的是用于将`.py文件`打包成`.exe文件`的python脚本;  
也可以使用[pyinstaller](https://github.com/pyinstaller/pyinstaller)库自行打包;  

>命令行下安装`pip install --user pyinstaller`  
>打包方法  
>在命令行下cd到.py和.ico文件所在的文件夹  
>使用命令`pyinstaller -i xxx.ico -F xxx.py`  
>如果没有cd，使用绝对路径即可，也可以不使用图标文件直接打包  

## 依赖的第三方库
[requests](https://github.com/pyinstaller/pyinstaller)  
[pywifi](https://github.com/awkman/pywifi)  
[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)  
[prettytable](https://pypi.org/project/PrettyTable/)  
[pywin32](https://pypi.org/project/pywin32/)

## 关于作者
BJFU非计算机专业的一只野生猿，欢迎与我交流Python。(๑¯∀¯๑)  
