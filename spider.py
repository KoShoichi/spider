# coding = utf-8

from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error


def get_html(url):

    head = {"User-Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_6) AppleWebKit / 537.36(KHTML, like Gecko) Chrome/ 85.0 .4183 .83 Safari / 537.36"}
    request = urllib.request.Request(url, headers=head)
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
        quit()

def output_html(html,url):
    code = url.replace("https://xn--vckya7nx51ik9ay55a3l3a.com/companies/","")
    filename = "html_"+code+".txt"
    with open(filename,'w',encoding='utf-8') as f:
        print(html,file=f)


def passdata_attribute(html,url):

    soup = BeautifulSoup(html, 'html.parser')
    code = url.replace("https://xn--vckya7nx51ik9ay55a3l3a.com/companies/","")
    infolist = []
    infolist.append(code)
    i = 1

    def pass_to_infolist(element):
        nonlocal i
        infolist.append(element)
        infolist[i] = infolist[i].strip()
        i += 1

    #company name
    element = soup.find("a",class_="",href=code)
    pass_to_infolist(element.text)

    #上場市場、上場日
    for element in soup.find_all("td",limit=2):
        pass_to_infolist(element.text)

    #業種
    element = soup.find("a",href=re.compile(r"^/industries"))
    pass_to_infolist(element.text)

    #法人番号
    startpoint = soup.find(string="法人番号")
    element = startpoint.find_next("dd",class_="companies_data")
    pass_to_infolist(element.text.lstrip().rstrip().partition("\n")[0])

    #address
    element = soup.find("div",id="address2")
    unwanted = element.find("a")
    unwanted.extract()
    element = element.text.replace("[","")
    element = element.replace("]","")
    element = element.rstrip().lstrip().partition("\n")[2].lstrip()
    pass_to_infolist(element)

    return infolist


def passdata_stockholder(html,url):

    soup = BeautifulSoup(html, 'html.parser')
    code = url.replace("https://xn--vckya7nx51ik9ay55a3l3a.com/companies/", "")
    infolist = [[] for j in range(2)]
    i = 0
    j = 0

    def pass_to_infolist_1(element):
        nonlocal i
        infolist[0].append(element)
        infolist[0][i] = infolist[0][i].strip()
        i += 1

    def pass_to_infolist_2(element):
        nonlocal j
        infolist[1].append(element)
        infolist[1][j] = infolist[1][j].strip()
        j += 1

    #stockholder of the company
    startpoint = soup.find("dt",class_="companies_title",string="従業員数")
    for element in startpoint.find_all_previous(lambda tag: tag.name == 'td' and tag.get('class') == ['right']):
        pass_to_infolist_1(element.text.strip().replace("\n",""))
        element = element.find_previous("td")
        pass_to_infolist_1(element.text.strip().replace("\n",""))
        element = element.find_previous("td")
        pass_to_infolist_1(element.text.strip().replace("\n",""))

    #出資先上場企業
    startpoint = soup.find("th",string="直接持分比率")
    for element in startpoint.find_all_next("a",href=re.compile(r"^/companies")):
        pass_to_infolist_2(element.text.strip())
        element = element.find_next("td")
        pass_to_infolist_2(element.text.strip())

    return infolist

def output_to_csv(html,url,title=[]):

    atr_info = passdata_attribute(html,url)
    stock_info = passdata_stockholder(html,url)
    ni = len(atr_info) #number of attribute information
    nsh = len(stock_info[0]) #number of stockholder
    nm = len(stock_info[1]) #number of 出資先
    code = url.replace("https://xn--vckya7nx51ik9ay55a3l3a.com/companies/", "")
    filename = "content_" + code +".csv"

    with open(filename,"w",encoding='utf-8') as f:
        for i in range(ni):
            print(title[i],atr_info[i].replace(',',''),sep=",",file=f)
        print("\n大株主\n順位,株主名,持株比率",file=f)
        for i in range(nsh,0,-1):
            print(stock_info[0][i-1],end="",file=f)
            if i%3==0 or (i+1)%3==0:
                print(",",end="",file=f)
            else:
                print("\n",end="",file=f)
        print("\n出資先上場企業\n会社名,直接持株比率",file=f)
        for i in range(nm):
            print(stock_info[1][i],end="",file=f)
            if i%2==0:
                print(",",end="",file=f)
            else:
                print("\n",end="",file=f)

def read_company():
    clist = []
    with open("company_list.txt","r",encoding='utf-8') as f:
        for line in f:
            clist.append(line)
    return clist


if __name__ == "__main__":
    basic_url = "https://xn--vckya7nx51ik9ay55a3l3a.com/companies/4847"
    title = ["銘柄コード","会社名","上場市場","上場日","業種","法人番号","住所"]

    clist = read_company()

    for i in clist:
        url = basic_url.replace("4847",i).strip()
        html = get_html(url)
        output_html(html,url)
        output_to_csv(html,url,title)
