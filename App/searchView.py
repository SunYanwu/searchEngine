from flask import Blueprint, render_template, request, json
from setupIndex.setup_db import get_newsData
from App.search_fromdb import search_result

search_blue = Blueprint("search_blue",__name__)

@search_blue.route('/')
def hello ():
    return render_template('lawNews.html',error = True,page = 0)

@search_blue.route('/search/',methods=['post'])
def search():
    print('-------------------------------------')
    global scores
    global pages
    global keyword
    keyword = request.form.get('key_word')
    flag, scores = search_result(keyword)
    print(scores)
    pages = cut_page(len(scores)) +1 # 获得一共需要的分页数
    print(pages)
    docs = get_docs(scores,0,5)     #得到返回给客户端的文档集合（按相关度从大到小排列）
    print(docs)
    if not len(docs):
        print('isNone')
        return render_template('lawNews.html',error = False)
    else:
        return render_template('lawNews.html',key = keyword,page = pages,docs = docs,error = True)

def get_docs(scores,start,end):
    docs = []

    if(len(scores)<5):
        end = len(scores)
    if(end > len(scores)):
        end = len(scores)

    #获取原始新闻数据
    file = './data/newsData.data'
    with open(file, 'r', encoding='utf-8') as data:
        news = json.load(data)
    news_dic = get_newsData(news)

    for s in scores[start:end]:
        docid = s[0]   #获取docId
        newsData = news_dic[docid]  #得到docID对应的 doc文档信息
        title = newsData[0]
        snipper = str(newsData[1])[0:80] + '......'
        url = newsData[2]
        doc = {'title':title,'snipper':snipper,'url':url}
        docs.append(doc)
    return docs

def cut_page(sum_doc):
    sum_page = sum_doc/5 + 1
    sum_page = int(sum_page)
    if sum_page > 5:     #只取前五页相关的高的数据
        sum_page = 5
    return sum_page

@search_blue.route('/search/page/<page_no>/',methods = ['get'])
def search_by_page(page_no):
    page_num = int(page_no)
    start = (page_num-1) * 5
    end = start + 5
    docs = get_docs(scores,start,end)
    if not len(docs):
        print('isNone')
        return render_template('lawNews.html',error = False)
    else:
        return render_template('lawNews.html',key = keyword,page = pages,docs = docs,error = True)

if __name__ == '__main__':
    search('恋爱')