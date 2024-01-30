# Case de Analista Inovação Digital Python

O repositório presente é referente ao desenvolvimento dos cases para o processo seletivo do cargo de Analista Inovação Digital Python Junior

## Tabela de conteúdos

- [Introdução](#Introdução)
- [Getting Started](#getting-started)
  - [Prerequisitos](#prerequisites)
  - [Instalação](#installation)


## Introdução

O projeto seguinte contém a implementação para os 3 cases definidos para o processo de Analista Inovação Digital Python.
Cara pasta identifica o case relacionado a ela, contendo o código fonte, arquivo de requerimentos, testes, input de exemplo e um executável para a utlização do projeto sem a necessidade de instalação.


## Getting Started

Para rodar um dado projeto é possível utilizar dois métodos, **executável** ou por **manual**.

### Executável

Por esse método basta selecionar o arquivo `main.exe`, o programa deve depois de alguns segundos abrir uma interface visual para execução.
No caso do segundo case deve-se primeiro descomprimir o arquivo `case_2.zip`, nele está o executável necessário assim como os diretório com as dependências do peojeto.

### Manual

Para a excecução manual deve-se primeiro seguir os seguintes passos:

1. **Crie um ambiente virtual no diretório do case:**

    ```bash
    # No Windows
    python -m venv venv

    # No Linux
    python3 -m venv venv
    ```

2. **Ative o ambient virtual:**

    ```bash
    # No Windows
    .\venv\Scripts\activate

    # No Linux
    source venv/bin/activate
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

   Isso vai instalar todas as dependências definidas no arquivo `requirements.txt`.


4. **Run your project:**

    ```bash
    # No Windows
    python src/main.py

    # No Linux
    python3 src/main.py
    ```

5. **Desative o ambiente quando finalizar de rodar o projeto:**

    ```bash
    deactivate
    ```
