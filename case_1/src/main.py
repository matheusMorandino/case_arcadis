import os
from processadorTabela import ProcessadorTabela

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    pdf_path = os.path.join(ROOT_DIR, "input\\Material_Case_Ex1.pdf")

    processaTabela = ProcessadorTabela()

    df_dados = processaTabela.formata_arquivo_pdf(path_arquivo=pdf_path)

    print(df_dados)
