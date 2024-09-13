import scrapy
from urllib.parse import urlencode
from dotenv import dotenv_values 



config = dotenv_values(".env")

def get_scrapeops_url(url):
    payload = {'api_key': config['API_KEY'], 'url': url, 'bypass': 'cloudflare_level_1'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class ZapimoveisSpider(scrapy.Spider):
    name = "zapimoveis"
    allowed_domains = ["www.zapimoveis.com.br"]
    start_urls = ["https://www.zapimoveis.com.br/venda/imoveis/rj+rio-de-janeiro+zona-oeste+recreio-dos-bandeirantes/"]

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse, headers=self.HEADERS)

    def parse(self, response):
        pass


