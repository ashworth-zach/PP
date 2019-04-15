import scrapy
from tinydb import TinyDB, Query
from scrapy.crawler import CrawlerProcess
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
def cleanLink(link):
    group = link.split('\n')
    nlink = "".join(group)
    group = nlink.split('\t')
    nlink = "".join(group)
    return nlink
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
    urls=[['https://undefeated.com/collections/apparel/tees?page=', 'Tees'],['https://undefeated.com/collections/apparel/tops?page=','Tops'],['https://undefeated.com/collections/apparel/outerwear?page=','Outerwear'],['https://undefeated.com/collections/footwear?page=','Shoes']]
    site=None
    catagory=None
    def start_requests(self):
        if self.CurURL < len(self.urls):
            self.site=self.urls[self.CurURL][0]
            self.catagory = self.urls[self.CurURL][1]
            yield scrapy.Request(url=self.urls[self.CurURL][0]+str(self.x), callback=self.parse)
    def parse(self, response):
        db=TinyDB('DBFiles/UndefeatedDB.json')
        Q = Query()
        items = response.css('div.product-grid-item  ')
        if items:
            for item in items:
                dirtyimage = item.css('img::attr(src)').extract()
                namecolor = item.css('a::text').extract()
                if sepNameColor(namecolor[0]):
                    combo = sepNameColor(namecolor[0])
                else:
                    combo = [namecolor[0],"N/A"]
                name = combo[0]
                colors = combo[1]
                image = cleanLink(dirtyimage[0])
                ahref = item.css('a::attr(href)').extract()[0]
                price = item.css('span.money::text').extract()[0]
                db.upsert({"Site":"Undefeated","catagory":self.urls[self.CurURL][1], 'title':name,'price':price, 'colors':colors, 'image':image, 'href':'undefeated.com'+str(ahref)}, Q.href == 'undefeated.com'+str(ahref))
            self.x += 1
            yield scrapy.Request(url=self.urls[self.CurURL][0]+str(self.x), callback=self.parse)
        else:
            self.x = 1
            self.CurURL += 1
            if self.CurURL < len(self.urls):
                self.site=self.urls[self.CurURL][0]
                self.catagory = self.urls[self.CurURL][1]
                yield scrapy.Request(url=self.urls[self.CurURL][0]+str(self.x), callback=self.parse)
SpidInit()