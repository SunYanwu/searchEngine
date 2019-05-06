import math
import operator
import re

import jieba
import pymysql

def search_result(keyword):
    BM25_scores = {}
    cut_item = jieba.cut_for_search(keyword)
    n,clean_dic = cut_clean(cut_item)
    for term in clean_dic.keys():
        print(term)
        r = search_from_db(term)
        if r is None:
            continue
        df = r[1]
        N = 4330
        avg_l = 229.799
        k1 = 1.5
        b = 0.75
        w = math.log2((N - df + 0.5 )/(df + 0.5))
        doc_list = r[2].split('\n')
        for doc in doc_list:
            docId,tf,ld = doc.split('\t')
            docId = int(docId)
            tf = int(tf)
            ld = int(ld)
            s = ((k1+1)*w*tf)/(tf+k1*(1-b+b*ld/avg_l))
            if docId in BM25_scores:
                BM25_scores[docId] = BM25_scores[docId] + s
            else:
                BM25_scores[docId] = s
    BM25_scores = sorted(BM25_scores.items(),key=operator.itemgetter(1))
    BM25_scores.reverse()
    if BM25_scores is None:
        return 0,[]
    else:
        return 1,BM25_scores

def cut_clean(seg_list):
    cut_clean = {}
    n = 0
    file = open('./data/stop_word.txt', 'r', encoding='utf-8')
    stopword = set(file.read().split('\n'))
    for i in seg_list:
        i = i.strip().lower()
        if (i != '' and not isNumber(i) and i not in stopword):
            n = n + 1
            if i in cut_clean:
                cut_clean[i] = cut_clean[i] + 1
            else:
                cut_clean[i] = 1
    return n, cut_clean

def isNumber(s):
    p1 = re.compile(r'[0-9]+')
    p2 = re.compile(r'[a-zA-Z]+')
    result1 = p1.match(s)
    result2 = p2.match(s)
    if result1 or result2:
        return True
    else:
        return False

def search_from_db(term):
    con = pymysql.connect(host='localhost', port=3306, user='root', password='153418', db='newstest')
    c = con.cursor()
    c.execute(' select * from newdata where keyword = %s',term)
    return(c.fetchone())

if __name__ == '__main__':
    search_result('闯红灯')