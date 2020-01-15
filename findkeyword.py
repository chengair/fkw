import jieba
import os
import sqlite3
import time
import pandas as pd
import tkinter as tk
import tkinter.filedialog as tkfd
import sys
from collections import defaultdict

class FindKeyWords():
    def __Log(self,msg):
        logf=open('log.txt','a')
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



if __name__ == "__main__":
    fkw=FindKeyWords()
    fkw.Read_describe_by_excel('data/样例.xlsx')
    fkw.Find()
    for k in fkw.keywords_finded:
        print(k)
    pass