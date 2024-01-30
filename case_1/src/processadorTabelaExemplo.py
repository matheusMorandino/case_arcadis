import camelot
import pandas as pd
from datetime import datetime
from processadorTabela import ProcessadorTabela


class ProcessadorTabelaExemplo(ProcessadorTabela):
    def __init__(self):
        super()

    @staticmethod
    def __colapsar_espacos_vazio(df: pd.DataFrame):
        """
        Remove células vazias de um dataframe, reduzindo uma linha para o seu estado mais compacto possível
        sem ter que mesclar células

        :param df: dataframe sem formatação pós segmentação
        :type df: pd.DataFrame
        :return: pd.DataFrame
        """
        df_limpo = pd.DataFrame()
        for _, linha in df.iterrows():
            linha_limpa = [cell for cell in linha if pd.notna(cell) and cell != '']
            df_limpo = pd.concat([df_limpo, pd.DataFrame([linha_limpa])])
        return df_limpo

    @staticmethod
    def __cria_df_info_amostra(segmentos: dict):
        """
        Cria um dataframe com os dados referentes aos dados da amostra utilizando um dos segmentos
        gerados do pdf original.

        :param segmentos: dicionário com os segmentos de dados
        :type segmentos: dict
        :return: pd.DataFrame
        """
        df_info_amostra = segmentos["DADOS REFERENTES A AMOSTRA"].drop([2, 3], axis=1).T
        df_info_amostra.columns = df_info_amostra.iloc[0]
        df_info_amostra = df_info_amostra[1:].reset_index(drop=True)

        return df_info_amostra

    @staticmethod
    def __cria_df_dados_amostra(segmentos: dict):
        """
        Cria um dataframe contendo os dados da tabela de resultados da análise de compostos utilizando
        dos segmentos gerados do pdf original.

        :param segmentos: dicionário com os segmentos de dados
        :type segmentos: dict
        :return:
        """
        df_dados = segmentos["do Ensaio"].reset_index(drop=True)
        df_dados.columns = segmentos["RESULTADO S PARA A AMO STRA"].iloc[0].tolist()

        return df_dados

    @staticmethod
    def __cria_colunas_id_amostra(df_dados: pd.DataFrame, df_info_amostra: pd.DataFrame):
        """
        Cria as colunas relacionadas a identificação da amostra

        :param df_dados: dataframe com os dados resultantes da análise da amostra.
        :type df_dados: pd.DataFrame
        :param df_info_amostra: dataframe com os dados de identificação da amostra.
        :type df_info_amostra: pd.DataFrame
        :return:
        """
        df_dados["Nome da amostra"] = df_info_amostra["Identificação do Cliente:"][0]
        df_dados["timestamp coleta"] = df_info_amostra["Data da Amostragem  :"][0]
        df_dados[["Data de coleta", "Horário de coleta"]] = df_dados["timestamp coleta"].str.split(" ", expand=True)

        return df_dados

    @staticmethod
    def __formata_colunas_amostragem(df_dados: pd.DataFrame):
        """
        Formata as colunas relacionadas aos dados da amostragem

        :param df_dados: dataframe com os dados resultantes da análise da amostra.
        :type df_dados: pd.DataFrame
        :return: pd.DataFrame
        """
        df_dados["Resultado"] = df_dados["Resultados analíticos"].apply(lambda x: "< LQ" if "<" in x else x)
        df_dados["Unidade"] = df_dados["Unidade"].str.replace("µ", "u", regex=True)
        df_dados["Identificação interna"] = (
                df_dados["Nome da amostra"] +
                "_" +
                df_dados["Data  do Início"].apply(lambda x: str(int(datetime.strptime(x, "%d/%m/%Y %H:%M").timestamp()))))

        df_dados = (
            df_dados.rename(columns={"Parâmetros": "Parâmetro químico", "LQ / Faixa": "Limite de Quantificação (LQ)"}))

        return df_dados

    def formata_arquivo_pdf(self, tabelas_segmentadas: dict) -> pd.DataFrame:
        """
        Função que recebe um arquivo pdf com dados de amostras e retorna um dataframe formatado dos
        dados presentes

        :param tabelas_segmentadas: dict com as tabelas segmentas do pdf
        :type tabelas_segmentadas: dict
        :return: pd.DataFrame
        """
        for chave, segmento in tabelas_segmentadas.items():
            tabelas_segmentadas[chave] = self.__colapsar_espacos_vazio(segmento)

        df_info_amostra = self.__cria_df_info_amostra(tabelas_segmentadas)
        df_dados = self.__cria_df_dados_amostra(tabelas_segmentadas)

        df_dados = self.__cria_colunas_id_amostra(df_dados, df_info_amostra)
        df_dados = self.__formata_colunas_amostragem(df_dados)

        # Reorganiza as colunas para o formato correto
        df_dados = df_dados[["Identificação interna", "Nome da amostra", "Data de coleta", "Horário de coleta",
                             "Parâmetro químico", "Resultado", "Unidade", "Limite de Quantificação (LQ)"]]

        return df_dados