from quintoandarscrap.quintoandarscrap.spiders.quintoandar import (
    QuintoandarSpider,
)
from src.extract import run_crawler
from src.load import upar_dados_no_banco
from src.transform import limpar_dados

path = 'data/casas.jsonl'
url = 'https://www.quintoandar.com.br/comprar/imovel/sao-paulo-sp-brasil'
# url = 'https://www.quintoandar.com.br/comprar/imovel/belo-horizonte-mg-brasil'
# url = 'https://www.quintoandar.com.br/comprar/imovel/rio-de-janeiro-rj-brasil'


def main():
    """Pipeline que faz as chamadas das funções de Extract, Transform e Load."""
    run_crawler(spider=QuintoandarSpider, path=path, url=url)
    df = limpar_dados(path=path)
    upar_dados_no_banco(df=df)


if __name__ == '__main__':
    main()
