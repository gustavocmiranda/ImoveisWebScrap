import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError


def upar_dados_no_banco(df: pd.DataFrame):
    """
    Função que carrega os dados em um banco de dados Postgres.

    As informações necessária para se conectar ao banco devem estar em um arquivo .env na raíz do projeto,
    e serão lidas pela função load_dotenv()

    args: df(DataFrame contendo as informações já limpas e de acordo com a estrutura do banco)
    """
    load_dotenv()

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    try:
        print('Iniciando conexão')
        engine = create_engine(
            f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
        )
        print('Conexão estabelecida')

        # Envie o DataFrame para o banco de dados
        with engine.connect() as conn:
            for _, row in df.iterrows():
                trans = conn.begin()
                try:
                    insert_query = text(
                        """
                    INSERT INTO imoveis (tipo, preco, preco_condominio, endereco, bairro, cidade, metros, quartos, vagas, data_coleta)
                    VALUES (:tipo, :preco, :preco_condominio, :endereco, :bairro, :cidade, :metros, :quartos, :vagas, :data_coleta)
                    ON CONFLICT (tipo, endereco, bairro, cidade, metros, quartos) DO NOTHING;
                    """
                    )

                    conn.execute(
                        insert_query,
                        {
                            'tipo': row['tipo'],
                            'preco': row['preco'],
                            'preco_condominio': row['preco_condominio'],
                            'endereco': row['endereco'],
                            'bairro': row['bairro'],
                            'cidade': row['cidade'],
                            'metros': row['metros'],
                            'quartos': row['quartos'],
                            'vagas': row['vagas'],
                            'data_coleta': row['data_coleta'],
                        },
                    )
                    trans.commit()
                    # print('Query executada')

                except Exception as ex:
                    print(ex)
                    trans.rollback()
            print('Executado')
    except Exception as e:
        print(e)
