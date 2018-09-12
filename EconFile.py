from lxml import html
from lxml.html import document_fromstring
import sys 
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
import requests
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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
    post_fields = {'type': 2, 'd': str(stockData[z]), 'p': "€" + str(stockData[z + 1].replace("Â €", "")), 'm': "€" + str(stockData[z + 2])}
    request = Request(weburl, urlencode(post_fields).encode())
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
            post_fields = {'type': 1, 'l': "https://www.londonstockexchange.com" + LinkList[z].get("href").split("'")[1].replace("\\", ""), 'd': newsDataDate[z].replace("\\n", "").replace("\\t", ""), 'n': newsData[z].replace("\\n", "").replace("\\t", "")}
            request = Request(weburl, urlencode(post_fields).encode())
            content2 = urlopen(request).read().decode()
        else:
            post_fields = {'type': 1, 'l': "https://www.londonstockexchange.com" + LinkList[z].get("href"), 'd': newsDataDate[z].replace("\\n", "").replace("\\t", ""), 'n': newsData[z].replace("\\n", "").replace("\\t", "")}
            request = Request(weburl, urlencode(post_fields).encode())
            content2 = urlopen(request).read().decode()
        print (content2 + " " + newsData[z].replace("\\n", "").replace("\\t", ""))
  