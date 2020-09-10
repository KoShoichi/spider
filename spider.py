# coding = utf-8

from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import xlwt
import sqlite3


# step1: scrape the website
# step2: analyze data one by one
# step3: save data

def main():
    baseurl  = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = ".\\doubanmovietop250.xls"
    #saveData(savepath)
    #askURL(baseurl)

#step 1 and 2
def getData(baseurl):
    datalist = []
    for i in range(0,10):    #get page number in 10 times
        url = baseurl + str(i*25)
        html = askURL(url)   #save original data get from web

    # 2. analyze one by one

    return datalist

#get content from dedicated url
def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_6) AppleWebKit / 537.36(KHTML, like Gecko) Chrome/ 85.0 .4183 .83 Safari / 537.36"
    }
                #agent, inform we are a browser but not a python program

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html



#step 3
def saveData(savepath):
    print("nothing\n")


if __name__ == "__main__":
    main()


