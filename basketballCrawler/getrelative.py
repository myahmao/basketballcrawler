from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import sys
import requests, urllib

reload(sys)
sys.setdefaultencoding('utf-8')


def getSoupFromURL(url, suppressOutput=True):
    """
    This function grabs the url and returns and returns the BeautifulSoup object
    """
    if not suppressOutput:
        print (url)

    try:
        r = requests.get(url)
    except:
        return None

    return BeautifulSoup(r.text, "html5lib")

#r = requests.get('http://www.basketball-reference.com/players/c/curryst01.html')
#print r.headers['content-type']
#print r.text

from bs4 import BeautifulSoup

url = "http://www.basketball-reference.com/players/c/curryst01.html"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, 'html5lib')
#print 53, soup.findAll('body')
body_text = soup.findAll('body')

#page = getSoupFromURL(url, True)
#body_text =  page.findAll('body')


response = HtmlResponse(url=url, body=str(body_text[0]))
relatvie =  Selector(response=response).xpath('//*[@id="meta"]/div[2]/p[8]/text()').extract()
for item in relatvie[:-1]:
	print str(item).lstrip(':').lstrip(';').strip()
name = response.xpath('//*[@itemprop="relatedTo"]/text()').extract()
for item in name:
	print str(item)