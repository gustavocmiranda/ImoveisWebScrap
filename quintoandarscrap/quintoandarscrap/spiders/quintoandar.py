import scrapy
from scrapy_playwright.page import PageMethod
import logging

# Define the async function to handle clicking process
async def click_ver_mais_button(page):
    click_count = 0
    while True:  # Click up to 10 times
        try:
            # Wait for the "Ver mais" button to appear
            await page.wait_for_selector('button[aria-label="Ver mais"]', timeout=10000)
            
            # Scroll into view and click the button
            # await page.evaluate('document.querySelector(\'button[aria-label="Ver mais"]\').scrollIntoView()')
            await page.click('button[aria-label="Ver mais"]')
            
            click_count += 1
            logging.info(f"Button clicked {click_count} times")

            # Wait for new content (like new house cards) to be loaded
            await page.wait_for_selector('div[data-testid="house-card-container"]', timeout=10000)

            # Wait for 2 seconds before the next click
            await page.wait_for_timeout(2000)
        except Exception as e:
            logging.error(f"Error clicking button: {e}")
            break  # Stop trying if there's an issue

class QuintoandarSpider(scrapy.Spider):
    name = "quintoandar"
    allowed_domains = ["www.quintoandar.com.br"]

    def start_requests(self):
        url = "https://www.quintoandar.com.br/comprar/imovel/recreio-dos-bandeirantes-rio-de-janeiro-rj-brasil"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", 'button[aria-label="Ver mais"]', timeout=10000),
            ],
            errback=self.errback,
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]  # Retrieve the Playwright page
        
        # Call the async function to click the "Ver mais" button multiple times
        await click_ver_mais_button(page)

        # Wait for a bit more to ensure all content is fully loaded
        await page.wait_for_timeout(5000)  # Adjust this timeout as needed

        # Now parse all the loaded content
        content = await page.content()  # Get the full page content after all clicks
        response = scrapy.http.TextResponse(url=page.url, body=content, encoding='utf-8')

        # Scrape all the house cards
        cards_casas = response.css('div[data-testid="house-card-container"]')
        for card in cards_casas:
            yield {
                "tipo": card.css('h2[class="Cozy__CardTitle-Metadata Dg2zLY"]::text').get(),
                "preco": card.css('h3[class="CozyTypography xih2fc EKXjIf EqjlRj"]::text').get(),
                "preco_condominio": card.css('h3[class="CozyTypography xih2fc _72Hu5c Ci-jp3"]::text').get(),
                "metro_quarto_vaga": card.css('h3[class="CozyTypography o6Ojuq xih2fc EKXjIf A68t3o"]::text').get(),
                "endereco": card.css('h2[class="CozyTypography xih2fc _72Hu5c Ci-jp3"]::text').get()
            }

        # Close the Playwright page when done
        await page.close()

    async def errback(self, failure):
        # Handle errors and close Playwright page
        page = failure.request.meta['playwright_page']
        await page.close()
