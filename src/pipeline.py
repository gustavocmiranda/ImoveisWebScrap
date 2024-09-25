from transform import limpar_dados
from extract import extrair_dados

path = 'data/casas.jsonl'

def main():

    extrair_dados(path=path)
    df = limpar_dados(path=path)

    print(df)

if __name__ == "__main__":
    main()