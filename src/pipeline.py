from src.transform import limpar_dados
from src.extract import run_crawler
from src.load import upar_dados_no_banco
from quintoandarscrap.quintoandarscrap.spiders.quintoandar import QuintoandarSpider

path = 'data/casas.jsonl'

def main():

    run_crawler(crawler=QuintoandarSpider, path= path)
    df = limpar_dados(path=path)
    upar_dados_no_banco(df=df)

    print(df.head())

if __name__ == "__main__":
    main()