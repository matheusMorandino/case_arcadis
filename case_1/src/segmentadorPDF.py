import camelot
import pandas as pd


class SegmentadorPDF:
    @staticmethod
    def __extrai_tabela_do_pdf(pdf_path: str):
        """
        Faz a leitura de um dado pdf, retornando o conteúdo em um df. O df retornado é o primeiro e maior da
        hierarquia de tabelas encontradas

        :param pdf_path: caminho para o arquivo de
        :type pdf_path: str
        :return: pd.DataFrame
        """
        tabelas = camelot.read_pdf(pdf_path, flavor='stream', pages='all', row_tol=1, col_tol=0)

        df_list = []
        for tabela in tabelas:
            df_list.append(tabela.df)

        return df_list[0]

    @staticmethod
    def __extrai_segmentos(df: pd.DataFrame):
        """
        Realiza a leitura do df extraido do pdf e segmenta ele baseado nas linhas que possuem apenas um dado,
        sendo que elas representam o cabeçalho de cada tabela

        :param df: dataframe com os dados crus do pdf
        :type df: pd.DataFrame
        :return: dict
        """
        segmentos = {}
        header_atual = None
        segmento_atual = pd.DataFrame()

        for index, row in df.iterrows():
            # Verifica se a linha tem apenas um valor não vazio
            linha_unitaria = sum(1 for cell in row if cell != '')
            if linha_unitaria == 1:
                # Se um novo cabeçalho é encontrado armazenar o segmento atual
                if header_atual is not None:
                    segmentos[header_atual] = segmento_atual.copy()
                header_atual = row[row != ''].values[0]
                segmento_atual = pd.DataFrame()
            else:
                segmento_atual = pd.concat([segmento_atual, pd.DataFrame([row])])

        # Armazena segmento final
        if header_atual is not None:
            segmentos[header_atual] = segmento_atual.copy()

        return segmentos

    def segmenta_pdf(self, path_arquivo: str):
        """
        Função responsável por preprocessar e segmentar o arquivo pdf para o processamento da tabela

        :param path_arquivo: caminho para o arquivo de pdf
        :type path_arquivo: str
        """
        tabela = self.__extrai_tabela_do_pdf(path_arquivo)

        tabelas_segmentadas = self.__extrai_segmentos(tabela)

        return tabelas_segmentadas
