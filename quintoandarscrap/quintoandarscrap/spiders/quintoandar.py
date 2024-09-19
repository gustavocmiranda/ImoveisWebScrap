import scrapy
from scrapy_playwright.page import PageMethod

class QuintoandarSpider(scrapy.Spider):
    name = "quintoandar"
    allowed_domains = ["www.quintoandar.com.br"]

    def start_requests(self):
        url = "https://www.quintoandar.com.br/comprar/imovel/recreio-dos-bandeirantes-rio-de-janeiro-rj-brasil"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            errback=self.errback,
        ))

    async def parse(self, response):
        cards_casas = response.css('div[data-testid="house-card-container"]').getall()
        for card in cards_casas:
            yield {
                "casa": card 
            }


    async def errback(self, failure):
        # Em caso de erro, fecha a página do Playwright
        page = failure.request.meta['playwright_page']
        await page.close()
