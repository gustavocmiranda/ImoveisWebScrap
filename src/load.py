from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os


def upar_dados_no_banco(df: pd.DataFrame):
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    try:
        print("Iniciando conexão")
        engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
        print("Conexão estabelecida")

        # Envie o DataFrame para o banco de dados
        df.to_sql('imoveis', con=engine, if_exists='append', index=False)
        print("to_sql executado")
    except Exception as e:
        print(e)