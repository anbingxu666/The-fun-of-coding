#coding=utf-8
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time,getpass

headers ={
'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
}
num=input("-----------------------\n请输入学号:")
pas=getpass.getpass("请输入密码:")
def getLT(url,sessions):
    itcontent = sessions.get(url)
    itcontentsoup = BeautifulSoup(itcontent.text, 'html.parser')
    Lt=itcontentsoup.find("input",attrs={"name":"lt"})["value"]
    return Lt

def login(LT,sessions):
    datas = {
        'username': num,
        'password': pas,
        'submit': '',
        'lt': LT,
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rmShown': '1'
    }
    response = sessions.post(url, headers=headers, data=datas)
    url2 = "http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017%D1%A7%C4%EA%B5%DA%B6%FE%D1%A7%C6%DA(%C1%BD%D1%A7%C6%DA)"
    score = sessions.get(url2)
    #soup2即课表的html
    soup2 = BeautifulSoup(score.text,"html.parser")
    return soup2

def savePage(name,page):
    file=page.encode("gbk")
    with open(name,"wb") as f:
        f.write(file)
    # print("成功保存成绩")
    print("-"*30)
def TableSpider(url):
    sessions = requests.Session()
    LT=getLT(url,sessions)
    file=login(LT,sessions)
    savePage("成绩.html",file)
    code=str(saveText(sessions))
    return code

def saveText(sessions):
    text=sessions.get("http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=001",headers=headers).text
    cont=etree.HTML(text)
    fincont=cont.xpath('//tr[@class="odd"]')
    for x in fincont:
        xx=x.xpath('./td')
        yy=x.xpath('./td/p')
        name=xx[2].text
        score=yy[0].text
        name=name.strip()
        score=score.strip()
        s=name+":"+score
        print(s)
    print("\n一共%s门课程"%(len(fincont)))
    return len(fincont)

if __name__=="__main__":
	while(1):
	    url="http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
	    code=TableSpider(url)
	    print("-------------------第一次获取")
	    i=1
	    while str(code)=="0":
	        time.sleep(3)
	        code = TableSpider(url)
	        i=i+1
	        if i>10:
	            print("超时了！！！")
	            break
	        print("\n-------------------第%d次获取"%(i))

	    print("若无法正常显示成绩请重试")
	    time.sleep(500)
