import os
from datetime import datetime

import numpy as np
import pandas as pd

pd.options.display.float_format = (
    lambda x: f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
)


def extrair_vagas(row):
    """Função auxiliar que define o número de vagas de um registro."""
    if len(row['metro_quarto_vaga']) == 3:
        return row['metro_quarto_vaga'][2]
    elif len(row['metro_quarto_vaga']) == 2 and (
        'vaga' in row['metro_quarto_vaga'][1]
        or 'vagas' in row['metro_quarto_vaga'][1]
    ):
        return row['metro_quarto_vaga'][1]
    else:
        return '0'


def extrair_quartos(row):
    """Função auxiliar que define o número de quartos de um registro."""
    if len(row['metro_quarto_vaga']) == 3:
        return row['metro_quarto_vaga'][1]
    elif len(row['metro_quarto_vaga']) == 2 and (
        'quarto' in row['metro_quarto_vaga'][1]
        or 'quartos' in row['metro_quarto_vaga'][1]
    ):
        return row['metro_quarto_vaga'][1]
    else:
        return '0'


def limpar_dados(path: str) -> pd.DataFrame:
    """
    Função que realiza a limpeza dos dados coletados.

    args: path(caminho para o arquivo gerado com os dados)

    return: Dataframe com dados limpos
    """
    df = pd.read_json(path, lines=True)

    df.dropna(axis=0, inplace=True)

    df['preco'] = (
        df['preco']
        .str.replace('R$\xa0', '')
        .str.strip()
        .str.replace('.', '')
        .astype(float, errors='ignore')
    )
    df['preco_condominio'] = (
        df['preco_condominio']
        .str.replace('R$\xa0', '')
        .str.replace(' Condo. + IPTU', '')
        .str.replace('.', '')
        .astype(float, errors='ignore')
    )

    df['endereco'] = df['endereco'].str.split(', ')
    df['bairro_cidade'] = df['endereco'].str.get(1)
    df['endereco'] = df['endereco'].str.get(0)
    df['bairro_cidade'] = df['bairro_cidade'].str.split(' · ')
    df['bairro'] = df['bairro_cidade'].str.get(0)
    df['cidade'] = df['bairro_cidade'].str.get(1)

    df['metro_quarto_vaga'] = df['metro_quarto_vaga'].str.split(' · ')
    df['metros'] = df['metro_quarto_vaga'].str.get(0)
    df['metros'] = (
        df['metros'].str.replace(' m²', '').astype(int, errors='ignore')
    )

    df['quartos'] = df.apply(extrair_quartos, axis=1)
    df['quartos'] = (
        df['quartos']
        .str.replace(r'\s*quartos?', '', regex=True)
        .astype(int, errors='ignore')
    )

    df['vagas'] = df.apply(extrair_vagas, axis=1)
    df['vagas'] = (
        df['vagas']
        .str.replace(r'\s*vagas?', '', regex=True)
        .astype(int, errors='ignore')
    )

    df['data_coleta'] = datetime.today()

    df.drop_duplicates(
        subset=['tipo', 'endereco', 'bairro', 'cidade', 'metros', 'quartos'],
        inplace=True,
    )

    df.drop('metro_quarto_vaga', axis=1, inplace=True)
    df.drop('bairro_cidade', axis=1, inplace=True)

    os.remove(path)

    return df
