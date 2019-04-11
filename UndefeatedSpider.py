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
def cleanLink(link):
    group = link.split('\n')
    nlink = "".join(group)
    group = nlink.split('\t')
    nlink = "".join(group)
    # print(nlink)
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
    urls=[['https://undefeated.com/collections/footwear?page=','Shoes']]
    site=None
    catagory=None
    
    def start_requests(self):
        for url in self.urls:
            self.site=url[0]
            self.catagory = url[1]
            yield scrapy.Request(url=url[0]+str(self.x), callback=self.parse)
    def parse(self, response):
        db=TinyDB('DBFiles/UndefeatedDB.json')
        dbQ = TinyDB('DBFiles/DatabaseQueue.json')
        Q = Query()
        # listXPath = ('//body/div[@class="boxes-wrapper"]/div[@id="page-body"]/*[@id="body-content"]/div[@id="main-content"]/div/div/div[@class="row"]/div[@id="col-main"]')#
        # text = response.xpath(listXPath)
        isitem = '//*[@class="col-md-4"]/product-grid-item  '
        items = response.css('div.product-grid-item  ')
        i = 1
        if items:
            for item in items:
                dirtyimage = item.css('img::attr(src)').extract()
                namecolor = item.css('a::text').extract()
                if sepNameColor(namecolor[0]):
                    combo = sepNameColor(namecolor[0])
                else:
                    combo = ["Unknown","Unknown"]
                #MODIFIED ABOVE OUTPUT BELOW
                name = combo[0]
                colors = combo[1]
                image = cleanLink(dirtyimage[0])
                ahref = item.css('a::attr(href)').extract()[0]
                price = item.css('span.money::text').extract()[0]
                db.upsert({"Site":"Undefeated","catagory":self.urls[0][1], 'title':name,'price':price, 'colors':colors, 'image':image, 'href':'undefeated.com'+str(ahref)}, Q.href == 'undefeated.com'+str(ahref))
            self.x += 1
            yield scrapy.Request(url=self.urls[0][0]+str(self.x), callback=self.parse)
        else:
            pass
