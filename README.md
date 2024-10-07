# ImoveisWebScrap
Projeto de WebScrap em site de vendas de imóveis

## Arquitetura do Projeto
![etldrawio-5](https://github.com/user-attachments/assets/c38d0d06-5a1a-4b80-a4ef-8060fb06773f)


## Como Rodar o Projeto

Para rodar este projeto, é necessário ter o **Poetry** instalado. Siga os passos abaixo:

1. **Navegue até a raiz do projeto**
2. Preencha o arquivo `.env` com os dados de conexão do seu banco de dados.
3. Instale as dependências listadas no arquivo requirements.txt:
   ```bash
   poetry add $(cat requirements.txt)
   ```
4. Execute o pipeline do projeto:
   - No Linux ou Mac:
     ```bash
     python3 -m src.pipeline
     ```
   - No Windows:
     ```bash
     python -m src.pipeline
     ```


## Descrição do Projeto

Este projeto realiza **Web Scraping** de um site de venda de imóveis, extraindo informações relevantes para análise e armazenamento. A pipeline do projeto é composta pelas seguintes etapas:

1. **Extração de dados (Web Scraping)**:  
   Utiliza a biblioteca Scrapy para coletar dados de imóveis à venda, como tipo, preço, localização, metragem, número de quartos e vagas de garagem. Os dados são salvos temporariamente em um arquivo no formato `.jsonl`.

2. **Transformação dos dados**:  
   Após a extração, os dados são carregados em um **DataFrame** do Pandas, onde passam por um processo de limpeza e transformação para padronização e adequação às necessidades da análise e armazenamento. São tratadas inconsistências, dados ausentes e criadas colunas úteis como bairro e cidade.

3. **Persistência dos dados**:  
   Os dados transformados são então persistidos em um banco de dados **PostgreSQL**, hospedado na plataforma **Render**. Durante essa fase, é garantida a integridade dos dados utilizando uma constraint de unicidade, para evitar duplicação de registros.

4. **Exclusão do arquivo temporário**:  
   Após a persistência, o arquivo de dados temporário gerado é deletado, mantendo o ambiente de trabalho limpo.

### Tecnologias Utilizadas:
- **Scrapy**: para realizar o Web Scraping.
- **Pandas**: para manipulação e transformação de dados.
- **SQLAlchemy**: para a comunicação e inserção dos dados no banco de dados PostgreSQL.
- **PostgreSQL**: banco de dados relacional para armazenamento dos dados.
- **Render**: plataforma de hospedagem do banco de dados PostgreSQL.
- **Python**: linguagem principal para desenvolvimento do projeto.
