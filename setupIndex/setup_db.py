import re

import jieba
import pymysql
from flask import json
from App import models

def create_posting_db(postings_list):
    con = pymysql.connect(host='localhost',port=3306,user='root',password='153418',db='news_db')
    cursor = con.cursor()

    cursor.execute('''drop table if exists newsdata''')
    cursor.execute('''create table newsdata (keyword varchar (32) primary key ,df INTEGER ,docs TEXT)''')

    for key,value in postings_list.items():
        doc_list = '\n'.join(map(str,value[1]))
        # print(key)
        t = (key,value[0],doc_list)
        # print(t)
        cursor.execute("insert into newsdata values(%s, %s, %s)", t)
    con.commit()
    con.close()

def doc_cut_list():   #构建词库
    postings_list = {}
    file = '../data/newsData.data'
    with open(file,'r',encoding='utf-8') as data:
        news = json.load(data)
    news_dic = get_newsData(news)
    avg_l = 0
    for a in news_dic:
        news = news_dic[a]
        cut_item = jieba.cut_for_search(news[1])
        cut_new = str.split(','.join(cut_item),',')
        # print(cut_new)
        ld,cut_clean = cut_clean_list(cut_new)
        avg_l = avg_l + ld
        for key,value in cut_clean.items():
            doc = models.Doc(a,value,ld)
            if key in postings_list:
                postings_list[key][0] = postings_list[key][0] + 1
                postings_list[key][1].append(doc)
            else:
                postings_list[key] = [1, [doc]]
    avg_l = avg_l/len(news_dic)
    print(len(news_dic))
    print(avg_l)
    # for k in postings_list:
    #     print(k)
    #     print(postings_list[k])
    create_posting_db(postings_list)

def cut_clean_list(seg_list):
    cut_clean = {}
    n = 0
    file = open('../data/stop_word.txt', 'r', encoding='utf-8')
    stopword = set(file.read().split('\n'))
    for i in seg_list:
        i = i.strip().lower()
        if (i != '' and not isNumber(i) and i not in stopword):
            n = n + 1
            if i in cut_clean:
                cut_clean[i] = cut_clean[i] + 1
            else:
                cut_clean[i] = 1
    return n,cut_clean

def get_newsData(data):
    i=0
    global news_dic
    news_dic = {}
    for a in data:
        news_dic[i] = a
        i = i + 1
    return news_dic

def isNumber(s):
    p1 = re.compile(r'[0-9]+')
    p2 = re.compile(r'[a-zA-Z]+')
    result1 = p1.match(s)
    result2 = p2.match(s)
    if result1 or result2:
        return True
    else:
        return False



if __name__ == '__main__':
   doc_cut_list()