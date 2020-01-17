import jieba
import os
import sqlite3
import time
import pandas as pd
import tkinter as tk
import threading
import tkinter.filedialog as tkfd
import sys
from collections import defaultdict

class FindKeyWords():
    def __Log(self,msg):
        logf=open('data/log.txt','a',encoding='utf8')
        logf.write(time.strftime('%Y-%m-%d %H:%M')+': '+msg+'\n')
        logf.close()

    def __Loadkeywords(self):
        self.keywordsdict=defaultdict(int)
        try:
            conn=sqlite3.connect('fkw.db')  #连接数据库，如果没有，则新建
            query=conn.cursor()
            res=query.execute('select * from keywords')
            for kw in res:
                self.keywordsdict[kw[0]]=1
        except:
            self.__Log(sys.exc_info[0])

    def __init__(self):
        self.__Loadkeywords()
        self.keywords_finded=[]
        self.keywords_jiebafinded=[]

    def Read_describe_by_excel(self,fpath):
        df=pd.read_excel(fpath,sheet_name=0)
        df.fillna('',inplace=True)  #替换NAN数据
        self.describes=df.iloc[:,4:6].values.tolist()

    def Find(self): #直接遍历匹配关键词
        try:
            for row in self.describes:
                tempkeyw=set()
                for col in row:
                    for kw in self.keywordsdict.keys():
                        if col.find(kw)>-1:
                            tempkeyw.add(kw)
                self.keywords_finded.append(list(tempkeyw))
        except:
            self.__Log(sys.exc_info[0])

    def jiebafind(self):
        jieba.load_userdict('keywords.txt')
        for row in self.describes:
            tempkw=set()
            tempnotkw=set()
            for col in row:
                seg_list=jieba.cut(col,cut_all=False)
                for segword in seg_list:
                    segword=segword.strip()
                    if segword in self.keywordsdict:
                        tempkw.add(segword)
                    else:
                        tempnotkw.add(segword)
            self.keywords_jiebafinded.append([list(tempkw),list(tempnotkw)])
    
    def jiebaout(self):
        outf=open('data/out.txt','w',encoding='utf8')
        for lkw in self.keywords_jiebafinded:
            #outf.write('，'.join(lkw[0])+','+','.join(lkw[1])+'\n')
            outf.write('|'.join(lkw[0])+'\n')

        outf.close()

        outfnot=open('data/outfnot.txt','w',encoding='utf8')
        for lkw in self.keywords_jiebafinded:
            #outf.write('，'.join(lkw[0])+','+','.join(lkw[1])+'\n')
            outfnot.write('|'.join(lkw[1])+'\n')

        outfnot.close()


class Gui():
    def __init__(self):
        self.main=tk.Tk()
        self.main.title("findkeywords")
        self.main.geometry('{}x{}'.format(500, 260))
        self.btcheck=tk.Button(self.main, text='find', command=self.__loadfile)
        self.btcheck.pack(pady=10, side='top')
        self.text1 = tk.Text(self.main)
        self.text1.pack()


    def __find(self,fpath):
        fkw=FindKeyWords()
        fkw.Read_describe_by_excel(fpath)
        fkw.jiebafind()
        fkw.jiebaout()
        self.text1.insert(tk.END, '完成')
        pass
    
    def __loadfile(self):
        fpath=tk.filedialog.askopenfilename()
        if fpath!='':
            p=threading.Thread(target=self.__find(fpath))
            p.start()

if __name__ == "__main__":
    #fkw=FindKeyWords()
    #fkw.Read_describe_by_excel('data/样例.xlsx')
    form1=Gui()
    form1.main.mainloop() 

    pass