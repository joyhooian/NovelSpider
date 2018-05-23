from tkinter import *
from tkinter.filedialog import askdirectory
import requests
import re
from bs4 import BeautifulSoup
from tkinter import messagebox

class Url:
    def __init__(self, url):
        self.url = url
        self.host = 'null'
        self.tid = 0
        self.authorid = 0
        self.page = 1
        urlList = self.url.split('&')
        for each in urlList:
            if each.find('allcp')>=0:
               self.host = each
               if each.find('http')<0:
                   self.host = "http://" + self.host
            elif each.find('tid')>=0:
                self.tid = int(re.sub("\D", "", each))
            elif each.find('authorid')>=0:
                self.authorid = int(re.sub("\D", "", each))

def pathSelect():
    pathStr = askdirectory()
    path.set(pathStr)

def topMessageCreate(msg, title):
    top = Toplevel()
    top.title(title)
    message = Message(top, text = msg)
    message.pack()

def start():
    if urlEntry.get() == "":
        messagebox.showerror(u'错误！', u'网址不能为空！')
        return
    if dirEntry.get() == "":
        messagebox.showerror(u'错误！', u'路径不能为空！')
        return
    if fileEntry.get() == "":
        messagebox.showerror(u'错误！', u'文件名不能为空！')
        return
    url = Url(str(urlEntry.get()))
    if url.host != 'null':
        if url.tid != 0:
            if url.authorid != 0:
                url.url = url.host + '&tid=' + str(url.tid) + '&page=' + str(url.page) + '&authorid=' + str(url.authorid)
            else:
                response = requests.get(url.url)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(str(response.text), 'html.parser')
                authorList = soup.select('.authi')
                author = BeautifulSoup(str(authorList[0]), 'html.parser')
                url.authorid = int(re.sub("\D", "", str(author.find_all(name='a')[1].get('href')).split('&')[3]))
                url.url = url.host + '&tid=' + str(url.tid) + '&page=' + str(url.page) + '&authorid=' + str(url.authorid)
        else:
            topMessageCreate(u'网址输入有误！2', u'错误！')
            return
    else:
        topMessageCreate(u'网址输入有误！1', u'错误！')
        return
    fileName = str(dirEntry.get()) + '\\' + str(fileEntry.get())
    messagebox.showinfo(u'提示', u'正在下载，请稍后...')
    response = requests.get(url.url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(str(response.text), 'html.parser')
    try:
        pageList = soup.find(class_ = 'pgs mtm mbm cl').select('.pg')[0].find_all(name = 'a')
        pageLenth = len(pageList)
        maxPage = int(re.sub("\D", "", pageList[pageLenth-2].text))
    except IndexError:
        maxPage = 1
    f = open(str(fileName) + ".txt", 'a', encoding='utf-8')
    chap = 1
    while maxPage - url.page >= 0:
        url.url = url.host + '&tid=' + str(url.tid) + '&page=' + str(url.page) + '&authorid=' + str(url.authorid)
        response = requests.get(url.url)
        soup = BeautifulSoup(str(response.text), 'html.parser')
        articleList = soup.select('.t_f')
        length = len(articleList)
        cnt = 0
        while cnt<length:
            article = articleList[cnt].text
            f.write(article)
            cnt = cnt+1
            chap = chap + 1
        url.page = url.page + 1
    f.close
    messagebox.showinfo(u'提示', u'下载完成！')

root = Tk()
frame = Frame(root)
path = StringVar()

root.title(u'小说下载器')
frame.pack(anchor = CENTER, padx = 10, pady = 10)
Label(frame, text = u'小说网址：').grid(row = 0, column = 0, pady = 5)
Label(frame, text = u'文件位置：').grid(row = 1, column  = 0, pady = 5)
Label(frame, text = u'文件名称：').grid(row = 2, column = 0, pady = 5)
urlEntry = Entry(frame)
dirEntry = Entry(frame, textvariable = path)
fileEntry = Entry(frame)
urlEntry.grid(row = 0, column = 1, columnspan = 3, sticky = W, ipadx = 35, pady = 5, ipady = 3)
dirEntry.grid(row = 1, column = 1, columnspan = 2, sticky = W, pady = 5, ipady = 3)
fileEntry.grid(row = 2, column = 1, columnspan = 2, sticky = W, pady = 5, ipady = 3)
Button(frame, text = u'选择路径', command = pathSelect).grid(row = 1, column = 3,sticky = E, pady = 5)
Button(frame, text = u'开始下载', command = start).grid(row = 2, column = 3, sticky = E, pady = 5)
mainloop()
