from src.transform import limpar_dados
from src.extract import run_crawler
from quintoandarscrap.quintoandarscrap.spiders.quintoandar import QuintoandarSpider

path = 'data/casas.jsonl'

def main():

    run_crawler(crawler=QuintoandarSpider, path= path)
    df = limpar_dados(path=path)

    print(df)

if __name__ == "__main__":
    main()