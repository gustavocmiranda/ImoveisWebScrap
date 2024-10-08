import os
import subprocess

import scrapy
from scrapy.crawler import CrawlerProcess


def run_crawler(spider: scrapy.Spider, path: str, url: str):
    """
    Função que chama o scrapy crawl e inicia a raspagem dos dados.

    args:
    spider(Objeto scrapy.Spider que irá realizar a raspagem)
    path(Caminho em que o arquivo com os dados será salvo)
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    cmd = [
        'scrapy',
        'crawl',
        spider.name,
        '-o',
        f'../{path}',  # Saída no arquivo JSONL
        '-a',  # Passa argumento para o spider
        f'url={url}'  # Passando a URL como argumento
    ]

    try:
        subprocess.run(cmd, check=True, cwd='quintoandarscrap')
        print(f'Chamada crawl realizada com sucesso')
    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar o crawler: {e}')
