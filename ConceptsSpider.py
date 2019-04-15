import scrapy
from tinydb import TinyDB, Query
from scrapy.crawler import CrawlerProcess
import os
def SpidInit():
    if not os.path.exists("DBFiles"):
        os.makedirs("DBFiles")
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(Spider)
    process.start()
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
    CurURL=0
    urls=[['https://cncpts.com/collections/apparel?page=','Apparel'],['https://cncpts.com/collections/footwear?page=','Shoes']]
    def start_requests(self):
        yield scrapy.Request(url=self.urls[0][0]+str(self.x), callback=self.parse)
    def parse(self, response):
        db=TinyDB('DBFiles/ConceptsDB.json')
        Q = Query()
        if not response.css('div#customer'):
            items = response.css('div.product')
            for item in items:
                combo = item.css('h4.product-title').css('a::text').extract()[0]
                if sepNameColor(combo):
                    name = sepNameColor(combo)[0]
                    colors = sepNameColor(combo)[1]
                else:
                    name = combo
                    colors = "N/A"
                ahref = item.css('a::attr(href)').extract()[0]
                price = item.css('span::text').extract()[0]
                image = item.css('img::attr(src)').extract()[0]
                if name != "Unknown":
                    db.upsert({'Site':'Concepts','catagory':self.urls[0][1],'title':name,'price':price.strip(), 'colors':colors, 'image':image, 'href':'cncpts.com'+str(ahref)}, Q.href == 'cncpts.com'+str(ahref))
            self.x +=1
            yield scrapy.Request(url=self.urls[self.CurURL][0]+str(self.x), callback=self.parse)
        else:
            self.x = 1
            self.CurURL += 1
            if self.CurURL < len(self.urls):
                yield scrapy.Request(url=self.urls[self.CurURL][0]+str(self.x), callback=self.parse)
SpidInit()