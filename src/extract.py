import os
import subprocess
import scrapy

from scrapy.crawler import CrawlerProcess

def run_crawler(crawler: scrapy.Spider, path: str):
    
    # Defina o caminho completo para o arquivo onde os dados minerados serão salvos
    # output_file = os.path.join('data', 'casas.jsonl')

    # Certifique-se de que o diretório 'data' existe
    if not os.path.exists('data'):
        os.makedirs('data')

    # Comando para executar o Scrapy com o spider 'quintoandar' e salvar a saída no arquivo .jsonl
    cmd = [
        'scrapy', 'crawl', crawler.name,
        '-o', f'../{path}',  # Saída no arquivo JSONL
        '-t', 'jsonlines'    # Formato da saída
    ]

    # Executa o comando
    try:
        subprocess.run(cmd, check=True, cwd='quintoandarscrap')
        print(f"Dados minerados com sucesso e salvos em {path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o crawler: {e}")
    