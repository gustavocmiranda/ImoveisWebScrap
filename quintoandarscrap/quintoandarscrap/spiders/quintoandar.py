import scrapy
from scrapy_playwright.page import PageMethod

class QuintoandarSpider(scrapy.Spider):
    name = "quintoandar"
    allowed_domains = ["www.quintoandar.com.br"]

    def start_requests(self):
        url = "https://www.quintoandar.com.br/comprar/imovel/recreio-dos-bandeirantes-rio-de-janeiro-rj-brasil"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            # playwright_include_page=True,
            playwright_page_methods = [
                PageMethod("click", 'button[aria-label="Ver mais"]'),
                PageMethod("wait_for_timeout", 2000),
                PageMethod("click", 'button[aria-label="Ver mais"]'),
                PageMethod("wait_for_timeout", 2000),
                PageMethod("click", 'button[aria-label="Ver mais"]'),
                PageMethod("wait_for_timeout", 2000),
                PageMethod("click", 'button[aria-label="Ver mais"]'),
                PageMethod("wait_for_timeout", 2000),
                PageMethod("click", 'button[aria-label="Ver mais"]'),
                PageMethod("wait_for_timeout", 2000),

            ],
            errback=self.errback,
        ))

    async def parse(self, response):
        cards_casas = response.css('div[data-testid="house-card-container"]')
        for card in cards_casas:
            yield {
                "tipo": card.css('h2[class="Cozy__CardTitle-Metadata Dg2zLY"]::text').get(),
                "preco": card.css('h3[class="CozyTypography xih2fc EKXjIf EqjlRj"]::text').get(),
                "preco_condominio": card.css('h3[class="CozyTypography xih2fc _72Hu5c Ci-jp3"]::text').get(),
                "metro_quarto_vaga": card.css('h3[class="CozyTypography o6Ojuq xih2fc EKXjIf A68t3o"]::text').get(),
                "endereco": card.css('h2[class="CozyTypography xih2fc _72Hu5c Ci-jp3"]::text').get()
            }


    async def errback(self, failure):
        # Em caso de erro, fecha a página do Playwright
        page = failure.request.meta['playwright_page']
        await page.close()