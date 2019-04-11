import scrapy
from tinydb import TinyDB, Query
import re
from scrapy.crawler import CrawlerProcess
import scrapy.crawler as crawler
from time import sleep
import os
def SpidInit():
    if not os.path.exists("DBFiles"):
        os.makedirs("DBFiles")
    dbQ = TinyDB('DBFiles/DatabaseQueue.json')
    dbQ.purge()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(Spider)
    process.start()
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
def sepNameColor(namecolor):
    if len(namecolor.split(' - ')) == 2:
        return namecolor.split(' - ')
    elif len(namecolor.split('(')) == 2:
        tmp = namecolor.split(')')
        x = "".join(tmp)
        tmp = x.split(' (')
        return tmp
    else:
        return
class Spider(scrapy.Spider):
    name = "Undefeated"
    x=1
    urls=[['https://cncpts.com/collections/footwear?page=','Shoes']]
    site=None
    catagory=None
    
    def start_requests(self):
        for url in self.urls:
            self.site=url[0]
            self.catagory = url[1]
            yield scrapy.Request(url=url[0]+str(self.x), callback=self.parse)
    def parse(self, response):
        db=TinyDB('DBFiles/ConceptsDB.json')
        dbQ=TinyDB('DBFiles/DatabaseQueue.json')
        Q = Query()
        if not response.css('div#customer'):
            items = response.css('div.product')
            for item in items:
                combo = item.css('h4.product-title').css('a::text').extract()[0]
                if sepNameColor(combo):
                    name = sepNameColor(combo)[0]
                    colors = sepNameColor(combo)[1]
                else:
                    name = "Unknown"
                    colors = "Unknown"
                ahref = item.css('a::attr(href)').extract()[0]
                price = item.css('span::text').extract()[0]
                image = item.css('img::attr(src)').extract()[0]
                if name != "Unknown":
                    db.upsert({'Site':'Concepts','catagory':self.urls[0][1],'title':name,'price':price.strip(), 'colors':colors, 'image':image, 'href':'cncpts.com'+str(ahref)}, Q.href == 'cncpts.com'+str(ahref))
            self.x +=1
            yield scrapy.Request(url=self.urls[0][0]+str(self.x), callback=self.parse)
SpidInit()