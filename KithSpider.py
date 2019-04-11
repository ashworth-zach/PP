import scrapy
from tinydb import TinyDB, Query
import re
from scrapy.crawler import CrawlerProcess
import scrapy.crawler as crawler
from time import sleep
import os
import KithScraper
test_contains = lambda value, search: search in value
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
class Spider(scrapy.Spider):

    name = "Kith"
    x=1
    urls=[['https://kith.com/collections/mens-footwear?page=','Shoes']]
    site=None
    catagory=None
    storage=1
    def start_requests(self):
        
        for url in self.urls:
            self.site = url[0]
            self.catagory = url[1]
            yield scrapy.Request(url=url[0]+str(self.x), callback=self.parse)
    def parse(self, response):
        db=TinyDB('DBFiles/KithDB.json')
        dbQ = TinyDB('DBFiles/DatabaseQueue.json')
        Q = Query()
        text = response.xpath('//body/div[@id="page-container"]/main/div[@id="collection-template"]/ul[@class="collection-products"]/li')
        isitem = '//*[@class="product-card"]/div/a'
        if 'https://kith.com'.join(text.xpath(isitem).css('a::attr(href)').extract()):
            items = response.css('li.collection-product')
            for item in items:
                title = item.css('h1.product-card__title::text').extract()
                ahref = item.css('a.product-card__image-slide::attr(href)').extract_first()
                price = item.css('span.product-card__price::text').extract()
                colors = item.css('h2.product-card__color::text').extract()
                image = item.css('img.product-card__image::attr(src)').extract_first()
                if str(price[0].strip()) == "":
                    dbQ.insert({'Site':'Kith','catagory':str(self.catagory),'title':str(title[0]),'price':"REPLACEME",'colors':colors[0],'image':image, 'href':'kith.com'+str(ahref)})
                else:
                    db.upsert({'Site':'Kith','catagory':str(self.catagory),'title':str(title[0]),'price':str(price[0].strip()),'colors':colors[0],'image':image, 'href':'kith.com'+str(ahref)}, Q.href == 'kith.com'+str(ahref))
            self.x +=1
            yield scrapy.Request(url=self.site+str(self.x), callback=self.parse)
                #print({'title':str(title[0]),'price':str(price[0].strip()),'colors':colors[0],'image':image, 'href':'kith.com'+str(ahref)})
            #     # with open(filename, 'w') as f:
            #     #     f.write(' https://kith.com'.join(
                
            #     for index, i in enumerate(text.xpath(ahref).css('a::attr(href)').extract_first()):
            #         x = text.xpath(prodtitle).extract()
            #         if not db.search(Q.href == "https://kith.com"+str(i)):
        else:
            KithScraper.addOne()
            if KithScraper.listchecker():
                self.x = 1
                self.site = str(KithScraper.KITHURLs[KithScraper.getX()][0])
                self.catagory = str(KithScraper.KITHURLs[KithScraper.getX()][1])
                sleep(50)
                yield scrapy.Request(url=self.site+str(self.x), callback=self.parse)
            else:
                yield scrapy.Request(url=str("https://"+dbQ.get(doc_id=1)['href']), callback=self.DatabaseCleanup)
    def DatabaseCleanup(self, response):
        db = TinyDB('DBFiles/KithDB.json')
        dbQ = TinyDB('DBFiles/DatabaseQueue.json')
        selected = dbQ.get(doc_id=self.storage)
        items = response.xpath('descendant-or-self::span').extract()
        Q = Query()
        for item in items:
            if 'data-product-price' in item:
                selected['price'] = cleanhtml(item)
                db.upsert(selected, Q.href == selected['href'])
                #self.log("adding "+str(selected)+" into main db")
                self.storage += 1
                if self.storage <= len(dbQ) and dbQ.get(doc_id=self.storage) != None and dbQ.get(doc_id=self.storage)['href'] != None:
                    yield scrapy.Request(url=str("https://"+dbQ.get(doc_id=self.storage)['href']), callback=self.DatabaseCleanup)
                

