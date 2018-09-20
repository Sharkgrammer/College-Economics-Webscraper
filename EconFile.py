from lxml import html
from lxml.html import document_fromstring
from lxml.etree import tostring
import sys 
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
import requests
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import datetime

class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit() 
    
def f(x):
    return {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }.get(x)

def toMySQLdate(date):
    returndate = ""
    #YYYY-MM-DD
    #31/08/2018
    #23 Aug 2018 17:37
    #2018-08-27
    #8102-90-81
    if "/" in date:
        date = date[::-1]
        for x in range(0, 3):
            returndate += date.split("/")[x][::-1]
            if x != 2: 
                returndate += "-"
    elif " " in date:
        for x in range(0, 3):
            if x != 1: 
                returndate += date.split(" ")[x][::-1]
            else:
                returndate += f(date.split(" ")[x])[::-1]
            if x != 2: 
                returndate += "-"
        returndate = returndate[::-1]
    else:
        returndate = date
    return returndate

weburl = "http://pokergamelabs.gearhostpreview.com/pyplace/EconFile.php?"
page = requests.get('http://www.ise.ie/Market-Data-Announcements/Companies/Equity-History/?equity=2015120')
tree = html.fromstring(page.content)
url = 'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/company-news.html?fourWayKey=IE0003290289IEEURSSQ3'  
r = Render(url)  
result = r.frame.toHtml()

stockData = tree.xpath('//td[@class="equityName"]/text()')
crtl = True
z = 0
#update the stcck price here pls
while crtl:
    post_fields = {'type': 2, 'd': toMySQLdate(str(stockData[z])), 'p': "€" + str(stockData[z + 1].replace("Â €", "")), 'm': "€" + str(stockData[z + 2])}
    request = Request(weburl, urlencode(post_fields).encode())
    toMySQLdate(str(stockData[z]))
    content2 = urlopen(request).read().decode()
    print (content2 + " €" + str(stockData[z + 1].replace("Â €", "")))
    z = z + 3
    if z == len(stockData):
        crtl = False
        
tree = html.fromstring(str(result.encode('utf-8')))

doc = document_fromstring(str(result.encode('utf-8')))

newsData = tree.xpath('//li[@class="newsContainer"]//a/text()')
newsDataDate = tree.xpath('//li[@class="newsContainer"]//span[@class="hour"]/text()')
LinkList = doc.xpath('//li[@class="newsContainer"]//a')
#All data recieved, lets update boi

for z in range(0, 40):
    crtl = True
    if crtl == True:
        if z < 20:
            post_fields = {'type': 1, 'l': "https://www.londonstockexchange.com" + LinkList[z].get("href").split("'")[1].replace("\\", ""), 'd': toMySQLdate(newsDataDate[z].replace("\\n", "").replace("\\t", "")), 'n': newsData[z].replace("\\n", "").replace("\\t", "")}
            request = Request(weburl, urlencode(post_fields).encode())
            content2 = urlopen(request).read().decode()
        else:
            post_fields = {'type': 1, 'l': "https://www.londonstockexchange.com" + LinkList[z].get("href"), 'd': toMySQLdate(newsDataDate[z].replace("\\n", "").replace("\\t", "")), 'n': newsData[z].replace("\\n", "").replace("\\t", "")}
            request = Request(weburl, urlencode(post_fields).encode())
            content2 = urlopen(request).read().decode()
        toMySQLdate(newsDataDate[z].replace("\\n", "").replace("\\t", ""))
        print (content2 + " " + newsData[z].replace("\\n", "").replace("\\t", ""))
        
def googledata(page):
    doc = document_fromstring(page.content)
    newsDataGoogle = doc.xpath('//h3[@class="r"]//a')
    newsDateGoogle = doc.xpath('//span[@class="f"]/text()')
    for x in range(0, len(newsDataGoogle)):
        tempStr = ""
        date = ""
        workingStr = str(tostring(newsDataGoogle[x]))
        for y in range(1, len(workingStr.split(">"))):
            tempStr += workingStr.split(">")[y].replace("<b", "").replace("</b", "").replace("</a", "").replace("\\", "").replace("...", "").replace("'", "").replace("&#", "").replace(";", "")
        if (newsDateGoogle[x].split("- ")[1].find("day")):
            date = str((datetime.datetime.now() - datetime.timedelta(days=(int(newsDateGoogle[x].split("- ")[1].split(" ")[0])))).date())
        else:
            date = newsDateGoogle[x].split("- ")[1]
        post_fields = {'type': 1, 'l': newsDataGoogle[x].get("href").replace("/url?q=", "").split("&sa=")[0], 'd': toMySQLdate(date), 'n': tempStr}
        toMySQLdate(date)
        request = Request(weburl, urlencode(post_fields).encode())
        content2 = urlopen(request).read().decode()
        print(content2 + " " + tempStr)
        
googledata(requests.get('https://www.google.ie/search?q=fbd+insurance&tbm=nws&tbs=sbd:1'))
googledata(requests.get('https://www.google.ie/search?q=fbd+insurance&tbm=nws&tbs=sbd:1&start=10'))
googledata(requests.get('https://www.google.ie/search?q=fbd+insurance&tbm=nws&tbs=sbd:1&start=20'))