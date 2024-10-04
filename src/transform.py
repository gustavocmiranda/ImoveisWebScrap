import os
from datetime import datetime

import numpy as np
import pandas as pd

pd.options.display.float_format = (
    lambda x: f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
)


def limpar_dados(path: str) -> pd.DataFrame:
    """
    Função que realiza a limpeza dos dados coletados.

    args: path(caminho para o arquivo gerado com os dados)

    return: Dataframe com dados limpos
    """
    df = pd.read_json(path, lines=True)

    df['preco'] = (
        df['preco']
        .str.replace('R$\xa0', '')
        .str.strip()
        .str.replace('.', '')
        .astype(float)
    )
    df['preco_condominio'] = (
        df['preco_condominio']
        .str.replace('R$\xa0', '')
        .str.replace(' Condo. + IPTU', '')
        .str.replace('.', '')
        .astype(float)
    )

    df['endereco'] = df['endereco'].str.split(', ')
    df['bairro_cidade'] = df['endereco'].str.get(1)
    df['endereco'] = df['endereco'].str.get(0)
    df['bairro_cidade'] = df['bairro_cidade'].str.split(' · ')
    df['bairro'] = df['bairro_cidade'].str.get(0)
    df['cidade'] = df['bairro_cidade'].str.get(1)

    df['metro_quarto_vaga'] = df['metro_quarto_vaga'].str.split(' · ')
    df['metros'] = df['metro_quarto_vaga'].str[0]
    df['metros'] = df['metros'].str.replace(' m²', '').astype(int)
    df['quartos'] = df['metro_quarto_vaga'].str[1]
    df['quartos'] = (
        df['quartos']
        .str.replace(' quartos', '')
        .str.replace(' quarto', '')
        .astype(int)
    )
    df['vagas'] = np.where(
        df['metro_quarto_vaga'].str.len() == 3,
        df['metro_quarto_vaga'].str[2],
        '0',
    )
    df['vagas'] = (
        df['vagas']
        .str.replace(' vagas', '')
        .str.replace(' vaga', '')
        .astype(int)
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
