import logging

import scrapy
from scrapy_playwright.page import PageMethod


# Define the async function to handle clicking process
async def click_ver_mais_button(page):
    click_count = 0
    while click_count < 100:  # Click up to 10 times
        try:
            # Wait for the "Ver mais" button to appear
            await page.wait_for_selector(
                'button[aria-label="Ver mais"]', timeout=50000
            )

            # Scroll into view and click the button
            await page.click('button[aria-label="Ver mais"]')

            click_count += 1
            logging.warning(f'Button clicked {click_count} times')

        except Exception as e:
            logging.error(f'Error clicking button: {e}')
            break


class QuintoandarSpider(scrapy.Spider):
    name = 'quintoandar'
    allowed_domains = ['www.quintoandar.com.br']

    def __init__(self, url=None, *args, **kwargs):
        super(QuintoandarSpider, self).__init__(*args, **kwargs)
        self.url = url

    def start_requests(self):

        yield scrapy.Request(
            self.url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod(
                        'wait_for_selector',
                        'button[aria-label="Ver mais"]',
                        timeout=10000,
                    ),
                ],
                errback=self.errback,
            ),
        )

    async def parse(self, response):
        page = response.meta['playwright_page']

        await click_ver_mais_button(page)

        # Wait for a bit more to ensure all content is fully loaded
        await page.wait_for_timeout(5000)

        # Now parse all the loaded content
        content = await page.content()
        response = scrapy.http.TextResponse(
            url=page.url, body=content, encoding='utf-8'
        )

        # Scrape all the house cards
        cards_casas = response.css('div[data-testid="house-card-container"]')
        for card in cards_casas:
            yield {
                'tipo': card.css(
                    'h2[class="Cozy__CardTitle-Metadata Dg2zLY"]::text'
                ).get(),
                'preco': card.css(
                    'h3[class="CozyTypography xih2fc EKXjIf EqjlRj"]::text'
                ).get(),
                'preco_condominio': card.css(
                    'h3[class="CozyTypography xih2fc _72Hu5c Ci-jp3"]::text'
                ).get(),
                'metro_quarto_vaga': card.css(
                    'h3[class="CozyTypography o6Ojuq xih2fc EKXjIf A68t3o"]::text'
                ).get(),
                'endereco': card.css(
                    'h2[class="CozyTypography xih2fc _72Hu5c Ci-jp3"]::text'
                ).get(),
            }

        # Close the Playwright page when done
        await page.close()

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
