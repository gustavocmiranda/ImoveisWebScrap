import os
import subprocess
import scrapy

from scrapy.crawler import CrawlerProcess

def run_crawler(crawler: scrapy.Spider, path: str):
    
    if not os.path.exists('data'):
        os.makedirs('data')

    cmd = [
        'scrapy', 'crawl', crawler.name,
        '-o', f'../{path}',  # Saída no arquivo JSONL
        '-t', 'jsonlines'    # Formato da saída
    ]

    try:
        subprocess.run(cmd, check=True, cwd='quintoandarscrap')
        print(f"Chamada crawl realizada com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o crawler: {e}")
    