from ..quintoandarscrap.quintoandarscrap.spiders.quintoandar import QuintoandarSpider
from scrapy.crawler import CrawlerProcess




def extrair_dados(path:str):
    process = CrawlerProcess(settings={
    'FEED_FORMAT': 'jsonlines',
    'FEED_URI': 'file:///' + path
    })
    
    process.crawl(QuintoandarSpider)
    process.start()