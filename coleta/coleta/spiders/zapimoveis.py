import scrapy
from urllib.parse import urlencode


API_KEY = 'c3c6850f-a8ed-4aad-937a-512efb9d5d00'

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'bypass': 'cloudflare_level_1'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class ZapimoveisSpider(scrapy.Spider):
    name = "zapimoveis"
    allowed_domains = ["www.zapimoveis.com.br"]
    start_urls = ["https://www.zapimoveis.com.br/venda/imoveis/rj+rio-de-janeiro+zona-oeste+recreio-dos-bandeirantes/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse)

    def parse(self, response):
        pass


