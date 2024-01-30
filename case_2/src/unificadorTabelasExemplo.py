import pandas as pd
import numpy as np
from unificadorTabelas import UnificadorTabelas


class UnificadorTabelasExemplo(UnificadorTabelas):
    def __init__(self):
        super()

    @staticmethod
    def __calcula_cma(input_df: pd.DataFrame, amb_col: str, cma_col: str):
        """
        Função responsável por calcular o CMA de um composto em um dado ambiente. Seleciona o mínimo
        dos possíveis valores de exposição para canceroso e não canceroso. Retorna um dataframe apenas com as
        colunas necessárias para identificar o composto e o valor de CMA.

        :param input_df: Dataframe com os identificadores dos compostos e valores de exposição
        :type input_df: pandas.DataFrame
        :param amb_col: Nome da coluna de exposição
        :type amb_col: string
        :param cma_col: Nome desejado para coluna de CMA
        :type cma_col: string
        :return: pd.DataFrame
        """
        linha_com_amb = input_df[input_df[amb_col] != '-']

        min_valor_amb = linha_com_amb.groupby(['CAS', 'Parâmetro'])[amb_col].min().reset_index()

        result_df = min_valor_amb.rename(columns={amb_col: cma_col})

        result_df[cma_col] = result_df[cma_col].replace('-', np.nan)

        return result_df

    @staticmethod
    def __normaliza_tabela_risco(df_risco: pd.DataFrame):
        """
        Remove as linhas relacionadas aos cabeçalhos mesclados do excel e coloca a tabela em um
        formato usável.

        :param df_risco:
        :type df_risco: pd.DataFrame
        :return: pd.DataFrame
        """
        df_risco.columns = ["index", "CAS", "Parâmetro", "efeito", "amb aberto", "amb fechado"]
        df_risco = df_risco.drop(columns=["index"])
        df_risco = df_risco.fillna(method='ffill')

        return df_risco

    def __criar_colunas_cma(self, df: pd.DataFrame):
        """
        Função responsável por definir a criação das colunas de cma. Retorna um dataframe com as
        colunas definidas

        :param df:
        :type df: pd.DataFrame
        :return: pd.DataFrame
        """
        df_cma = df.copy()

        cols = {"amb aberto": "CMA aberto",
                "amb fechado": "CMA fechado"}

        for amb_col, cma_col in cols.items():
            df_cma = df_cma.merge(self.__calcula_cma(df, amb_col, cma_col), on=["CAS", "Parâmetro"], how="left")

        return df_cma

    @staticmethod
    def __adiciona_flag_cma_maior_solubilidade(df_consol: pd.DataFrame):
        """
        Flag para escurecer a célula do CMA caso ele seja maior que a concentração de solubilidade

        :param df_consol:
        :type df_consol: pd.DataFrame
        :return: pd.DataFrame
        """
        df_consol["cinza_cma_aberto"] = df_consol.apply(
            lambda x: True if x["CMA aberto"] > x["Concentração de solubilidade"] else False, axis=1)
        df_consol["cinza_cma_fechado"] = df_consol.apply(
            lambda x: True if x["CMA fechado"] > x["Concentração de solubilidade"] else False, axis=1)

        return df_consol

    @staticmethod
    def __adiciona_flag_vor_maior_cma(df_consol: pd.DataFrame):
        """
        Flag que indica se o VOR é maior que o CMA calculado dos valores de ambiente

        :param df_consol:
        :return: pd.DataFrame
        """
        df_consol["laranja_cma_aberto"] = df_consol.apply(
            lambda x: True if x["Valor VOR (mg/l)"] > x["CMA aberto"] else False, axis=1)
        df_consol["laranja_cma_fechado"] = df_consol.apply(
            lambda x: True if x["Valor VOR (mg/l)"] > x["CMA fechado"] else False, axis=1)

        return df_consol

    def __adiciona_flags_para_output(self, df: pd.DataFrame):
        """
        Adicona as flags necessárias para formatação do arquivo de output

        :param df:
        :type df: pd.DataFrame
        :return: pd.DataFrame
        """
        df = self.__adiciona_flag_cma_maior_solubilidade(df)
        df = self.__adiciona_flag_vor_maior_cma(df)

        return df

    @staticmethod
    def __atualiza_cma_menor_que_vor(df_consol: pd.DataFrame):
        """
        Atualiza os valores da coluna de CMA caso ela seja menor que o VOR

        :param df_consol:
        :return: pd.DataFrame
        """
        df_consol["CMA aberto"] = df_consol.apply(
            lambda x: x["Valor VOR (mg/l)"] if x["Valor VOR (mg/l)"] > x["CMA aberto"] else x["CMA aberto"], axis=1)
        df_consol["CMA fechado"] = df_consol.apply(
            lambda x: x["Valor VOR (mg/l)"] if x["Valor VOR (mg/l)"] > x["CMA aberto"] else x["CMA fechado"], axis=1)

        return df_consol

    @staticmethod
    def __reorganiza_colunas_consolidadas(df_consol: pd.DataFrame):
        """
        Reorganiza as colunas do dataframe consolidado para um formato condizente ao esperado para o output

        :param df_consol: Dataframe com os dados consolidados
        :type df_consol: pd.DataFrame
        :return: pd.DataFrame
        """
        df_consol = df_consol[[
            "CAS", "Parâmetro", "efeito", "Concentração de solubilidade", "Valor VOR (mg/l)", "VOR", "amb aberto",
            "CMA aberto",
            "amb fechado", "CMA fechado", "cinza_cma_aberto", "cinza_cma_fechado", "laranja_cma_aberto",
            "laranja_cma_fechado"
        ]]

        return df_consol

    def consolida_dados_subistancias(self, file_path: str, para_output: bool=False):
        """
        Consolida os dados da planilha de exposição de compostos, retornando um dataframe com
        todos os dados relevantes presentes.

        :param file_path: path para arquivo de input
        :type file_path: str
        :param para_output: Se o dataframe deve ser preprocessado para o output em excel
        :type para_output: bool
        :return:
        """
        df_risco = pd.read_excel(file_path, header=list(range(0, 7)), sheet_name='Avaliacao_Risco_Case')
        df_orientadores = pd.read_excel(file_path, sheet_name='Valores_orientadores')

        df_risco = self.__normaliza_tabela_risco(df_risco)
        df_consol = df_risco.merge(df_orientadores, on=["CAS", "Parâmetro"], how="left")

        df_consol["Concentração de solubilidade"] = 500   # Concentração de solubilidade é 500 por padrão

        df_consol = self.__criar_colunas_cma(df_consol)

        if para_output:
            df_consol = self.__adiciona_flags_para_output(df_consol)

        df_consol = self.__atualiza_cma_menor_que_vor(df_consol)

        if para_output:
            df_cma = df_consol.drop(columns=["efeito", "amb aberto", "amb fechado"]).drop_duplicates(ignore_index=True)
            df_cma = df_cma.fillna(value="")
            df_cma["efeito"] = "C"

            df_formatado = df_risco.merge(df_cma, on=["CAS", "Parâmetro", "efeito"], how="left")

            duplicates_mask = df_formatado.duplicated(subset=["CAS", "Parâmetro"], keep='first')
            df_formatado.loc[duplicates_mask, ["CAS", "Parâmetro"]] = np.nan

            df_formatado.fillna(value=np.nan)

            return self.__reorganiza_colunas_consolidadas(df_formatado)

        return df_consol

