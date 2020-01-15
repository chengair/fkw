import jieba
import os
import sqlite3
import time
import sys
from collections import defaultdict

class FindKeyWords():
    def __Log(self,msg):
        logf=open('log.txt','a')
        logf.write(time.strftime('%Y-%m-%d %H:%M')+msg+'\n')
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
        super().__init__()
        self.__Loadkeywords()



if __name__ == "__main__":
    fkw=FindKeyWords()
    pass