# coding=utf-8
import io
from Tkinter import *
from PIL import Image,ImageTk
import sys
import webbrowser
import re
import urllib2
import chardet
from BeautifulSoup import BeautifulSoup

try:
  # Python2
  from urllib2 import urlopen
except ImportError:
  # Python3
  from urllib.request import urlopen

def resize(w, h, w_box, h_box, pil_image):
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2
  f2 = 1.0*h_box/h
  factor = min([f1, f2])
  width = int(w*factor)
  height = int(h*factor)
  return pil_image.resize((width, height), Image.ANTIALIAS)
def brief_url_img(url):
  image_bytes = urlopen(url).read()
  # internal data file
  data_stream = io.BytesIO(image_bytes)
  # open as a PIL image object
  pil_image = Image.open(file = '0.jpg')
  pil_image_resized = resize(w, h, w_box, h_box, pil_image)
  return pil_image_resized
def openurl(url):
  webbrowser.open_new_tab(url)
url0 = 'http://www.baidu.com'
url = [url0,url0,url0,url0,url0,url0,url0,url0,url0]
picurl = [url0,url0,url0,url0,url0,url0,url0,url0,url0]


filename='1.jpg'
w_win = 500
h_win = 500
root=Tk()
root.title('今日科大')
root.geometry('500x500')
w_box=100
h_box=100
img0 = ImageTk.PhotoImage(file = '0.jpg')
img = [img0,img0,img0,img0,img0,img0,img0,img0,img0]
box0 = Label(root,image=img0,width=w_box,height=h_box)
box = [box0,box0,box0,box0,box0,box0,box0,box0,box0]
title0 = Button(root,text='title0',command=openurl)
title = [title0,title0,title0,title0,title0,title0,title0,title0,title0]
tit0 = 'title0'
tit = [tit0,tit0,tit0,tit0,tit0,tit0,tit0,tit0,tit0]
def search(key_word):
    global x
    search_url='http://news.sogou.com/news?ie=utf8&p=40230447&interV=kKIOkrELjboMmLkEkLoTkKIMkLELjb8TkKIMkrELjboImLkEk74TkKILmrELjbgRmLkEkLY=_485898072&query=%E4%B8%AD%E7%A7%91%E5%A4%A7&'
    req=urllib2.urlopen(search_url.replace('key_word',key_word))
    real_visited=0
    html=req.read()
    soup=BeautifulSoup(html)
    #print soup
    content  = soup.findAll(name="a",attrs={"href":True,"data-click":True,"target":True}) #resultset object
    num = len(content)
    #print num
    for i in range(9):
        #先解析出来所有新闻的标题、来源、时间、url
        p_str= content[2*i] #if no result then nontype object
        tit[i]=p_str.renderContents()
        tit[i]=tit[i].decode('utf-8', 'ignore')#need it
        tit[i]= re.sub("<[^>]+>","",tit[i])
        print(tit[i])
        url[i]=str(p_str.get("href"))
        print(url[i])
        #存放顺利抓取的url，对比
        img[i]=getimg(url[i])
        w, h = img[i].size
        img[i]=resize(w,h, w_box, h_box,img[i])
def getimg(url):
    wmax=0
    hmax=0
    pos=0
    req=urllib2.urlopen(url)
    real_visited=0
    html=req.read()
    soup=BeautifulSoup(html)
    #print soup
    content  = soup.findAll(name="img") #resultset object
    print(content)
    num = len(content)
    #print num
    for i in range(num-1):
      url_img=str(content[i].get("src"))
      #print url_img[0]
      if (url_img[0]!='h'):
        continue
      print(url_img)
      image_bytes = urlopen(url_img).read()
      # internal data file
      data_stream = io.BytesIO(image_bytes)
      # open as a PIL image object
      pil_image = Image.open(data_stream)
      # get the size of the image
      w, h = pil_image.size
      #print w,h
      if (w*h>wmax*hmax):
        wmax=w
        hmax=h
        pos=i
    url_img=str(content[pos].get("src"))
    #print url_img
    image_bytes = urlopen(url_img).read()
    # internal data file
    data_stream = io.BytesIO(image_bytes)
    # open as a PIL image object
    pil_image = Image.open(data_stream)
    return pil_image
#search("中科大")
for r in range(3):
  for c in range(3):
    
    img0 = Image.open('%s.jpg'%(r*3+c))
    w,h = img0.size
    pil_image_resized = resize(w, h, w_box, h_box, img0)
    img[r*3+c] = ImageTk.PhotoImage(pil_image_resized)
    img[r*3+c] = ImageTk.PhotoImage(file = '%s.jpg'%(r*3+c))
    box[r*3+c] = Label(root,image=img[r*3+c],width=w_box,height=h_box)
    box[r*3+c].pack()
    box[r*3+c].place(x=50+c*150,y=50+r*150)
    title[r*3+c] = Button(root,text=tit[r*3+c],command = lambda:openurl(url[r*3+c]))
    title[r*3+c].pack()
    title[r*3+c].place(x=50+c*150,y=r*150+150)
    #openurl(url[r*3+c])
mainloop()
