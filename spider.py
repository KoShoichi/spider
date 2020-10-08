# coding = utf-8

from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import xlwt
import sqlite3


def gethtml(url, code):
    baseurl = url + code
    head = {"User-Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_6) AppleWebKit / 537.36(KHTML, like Gecko) Chrome/ 85.0 .4183 .83 Safari / 537.36"}
    request = urllib.request.Request(baseurl, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')

        return html
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

def dataOut(html):
    soup = BeautifulSoup(html, 'html.parser')

    with open('attribute_html.txt', 'w', encoding='utf-8') as f:
        print(html, file=f)

    with open('attribute.txt', 'w', encoding='utf-8') as f:
        for element in soup.find_all("h2"):
            print(element.text, file=f)
        for element in soup.find_all('td', limit=2):
            print(element.text, file=f)


if __name__ == "__main__":
    url = "https://xn--vckya7nx51ik9ay55a3l3a.com/companies/"
    code = str(1973)
    html = gethtml(url, code)
    dataOut(html)
