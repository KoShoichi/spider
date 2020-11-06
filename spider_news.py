# _*_ coding: utf-8 _*_
import feedparser
import requests
from newspaper import Article
from newspaper import Config

#to standard code
def code_parse(buf):
    buf = str(buf.encode("utf-8"))
    buf = buf[2:]
    buf = buf.replace("'","").replace("\\x","%")
    return buf

#get article
def parse_article(url):
    try:
        headers = {
            "User-Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_6) AppleWebKit / 537.36(KHTML, like Gecko) Chrome/ 85.0 .4183 .83 Safari / 537.36"}
        config = Config()
        config.headers = headers
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return "None"

def get_title(q):
    basic_url = "https://news.google.com/rss/search?q=default&hl=ja&gl=JP&ceid=JP:ja"
    url = basic_url.replace("default",q)
    d = feedparser.parse(url)
    titlelist = []
    for i in d.entries:
        titlelist.append(i["title"])
    return titlelist

def get_link(q):
    basic_url = "https://news.google.com/rss/search?q=default&hl=ja&gl=JP&ceid=JP:ja"
    url = basic_url.replace("default",q)
    d = feedparser.parse(url)
    linklist = []
    for i in d.entries:
        linklist.append(i["link"])
    return linklist

def read_company_news(filename):
    clist = [[None for i in range(2)]for j in range(2500)]
    i = 0
    with open(filename,"r",encoding="utf-8") as f:
        for line in f:
            temp = line.split()
            clist[i][0] = temp[0]
            clist[i][1] = temp[1]
            i += 1
    return clist

def output_table4(company_name,stock_code,startid):
    title = get_title(code_parse(company_name))
    link = get_link(code_parse(company_name))

    with open("table4.csv","a",encoding="utf_8_sig") as f:
        for i in range(10): #here number like 10 means 10 news for each company
            article = parse_article(link[i])
            print(startid,title[i].replace(",",""),link[i].replace(",",""),article.replace("\n","").replace(",","").strip(),company_name,stock_code,sep=",",file=f)
            startid += 1

if __name__ ==  "__main__":
    clist = read_company_news("companylist_news.txt")
    table4_colunm = ["newsid","title","link","article","companyname","stockcode"]
    size_colunm = len(table4_colunm)

    with open("table4.csv","w",encoding="utf_8_sig") as f:
        for i in range(size_colunm-1):
            print(table4_colunm[i],end=",",file=f)
        print(table4_colunm[size_colunm-1],file=f)

    sid = 1 #news id start from 1
    for i in range(6): #here number like 6 means 6 companies
        output_table4(clist[i][1],clist[i][0],sid)
        sid += 10