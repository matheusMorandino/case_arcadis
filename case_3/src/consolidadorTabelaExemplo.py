import pandas as pd
from consolidadorTabela import ConsolidadorTabela


class ConsolidadorTabelaExemplo(ConsolidadorTabela):
    @staticmethod
    def __normaliza_nome_colunas_ezmtp(df_ezmtp: pd.DataFrame):
        """
        Altera o nome das colunas seguintes para o formato correto

        :param df_ezmtp:
        :type df_ezmtp: pd.DataFrame
        :return: pd.DataFrame
        """
        ezmtp_sheet_df = df_ezmtp.rename(columns={
            "sys_loc_code": "#sys_loc_code",
            "Método de coleta": "measurement_method",
            "Tipo do turbidímetro": "remark",
            "Responsável pela coleta": "Resp Coleta",
            "Condição climática": "Cond clim",
            "Temp. \n(°C)": "Temp",
            "Condutividade (µS/cm)": "Cond elet",
            "OD \n(mg/L)": "OD",
            "ORP \n(mV)": "ORP",
            "Turbidez \n(NTU)": "Turb",
        })

        # Corrigindo colunas de data e hora
        ezmtp_sheet_df["Data da medição"] = pd.to_datetime(ezmtp_sheet_df["Data da medição"])
        ezmtp_sheet_df["Hora da medição"] = pd.to_datetime(ezmtp_sheet_df['Hora da medição'], format='%H:%M:%S')

        ezmtp_sheet_df["measurement_date"] = (
                ezmtp_sheet_df["Data da medição"].dt.strftime('%d/%m/%Y') +
                " " +
                ezmtp_sheet_df["Hora da medição"].dt.strftime('%H:%M')
        )

        ezmtp_sheet_df = ezmtp_sheet_df.drop(["Data da medição", "Hora da medição"], axis=1)

        return ezmtp_sheet_df

    @staticmethod
    def __avalia_integridade_input(df_cadastro: pd.DataFrame, df_ezmtp: pd.DataFrame):
        """
        Avalia se os arquivos de input possuem todas as colunas necessárias

        :param df_cadastro:
        :param df_ezmtp:
        :return:
        """
        colunas_cadastro = ['Cliente:', 'Código:', 'Task:*', 'Solicitante (nome e sobrenome):*']
        colunas_ezmtp = ['sys_loc_code', 'Data da medição', 'Hora da medição', 'Método de coleta',
                         'Tipo do turbidímetro', 'Temp. \n(°C)', 'Condutividade (µS/cm)', 'OD \n(mg/L)',
                         'pH', 'ORP \n(mV)', 'Turbidez \n(NTU)', 'Responsável pela coleta', 'Condição climática']

        # Integridade de EZMtp
        colunas_faltando_ezmtp = set(colunas_ezmtp) - set(df_ezmtp.columns)
        if len(colunas_faltando_ezmtp) > 0:
            mensagem_erro = f"Colunas necessárias ausentes: {', '.join(colunas_faltando_ezmtp)}"
            raise ValueError(mensagem_erro)

        # Integridade de Cadastro
        colunas_faltando_cadastro = set(colunas_cadastro) - set(df_cadastro.columns)
        if len(colunas_faltando_cadastro) > 0:
            mensagem_erro = f"Colunas necessárias ausentes: {', '.join(colunas_faltando_cadastro)}"
            raise ValueError(mensagem_erro)

    @staticmethod
    def __verificar_nan_no_dataframe(df: pd.DataFrame, sheet_nome: str):
        """
        Encontra todas as coordenadas (linha, coluna) dos valores NaN no DataFrame

        :param df:
        :param sheet_nome:
        :return:
        """
        coordenadas_nans = [(index, column) for index, row in df.iterrows() for column, value in row.items() if
                            pd.isna(value)]

        if coordenadas_nans:
            mensagem_erro = f"A planilha {sheet_nome} contém valores vazios e/ou inválidos."
            mensagem_erro += "\nCoordenadas dos valores inválidos:\n"
            for coordenada in coordenadas_nans:
                mensagem_erro += f"Linha: {coordenada[0]}, Coluna: {coordenada[1]}\n"
            raise ValueError(mensagem_erro)

    @staticmethod
    def __ezmtp_formatador(df_ezmtp: pd.DataFrame):
        """
        Função responsável por formatar o conteúdo do dataframe com os dados da planilha ezmtp
        para um formato usável.

        :param df_ezmtp: DataFrame com a planilha ezmtp
        :type df_ezmtp: pd.DataFrame
        :return: pd.DataFrame
        """
        ezmtp_sheet_df = df_ezmtp.iloc[1:, 3:]
        ezmtp_sheet_df.iloc[0] = ezmtp_sheet_df.iloc[1].combine_first(ezmtp_sheet_df.iloc[0])
        ezmtp_sheet_df.columns = ezmtp_sheet_df.iloc[0]
        ezmtp_sheet_df = ezmtp_sheet_df.iloc[2:].reset_index(drop=True)

        return ezmtp_sheet_df

    @staticmethod
    def __cadastro_formatador(df_cadastro: pd.DataFrame):
        """
        Função responsável por formatar o conteúdo do dataframe com os dados da planilha cadatro
        para um formato usável.

        :param df_cadastro: DataFrame com a planilha cadatro
        :type df_cadastro: pd.DataFrame
        :return: pd.DataFrame
        """
        cadastro_sheet_df = df_cadastro.iloc[:4, 1:]
        cadastro_sheet_df = cadastro_sheet_df.T
        cadastro_sheet_df.columns = cadastro_sheet_df.iloc[0]
        cadastro_sheet_df = cadastro_sheet_df.iloc[1:].reset_index(drop=True)

        return cadastro_sheet_df

    @staticmethod
    def __extrai_valores_ezmt(df_ezmtp: pd.DataFrame):
        """
        Extrai um subconjunto do dataframe contendo apenas as colunas relevantes para a coluna param_code
        do dataframe final.

        :param df_ezmtp:
        :type df_ezmtp: pd.DataFrame
        :return: pd.DataFrame
        """
        segmento_ezmtp = df_ezmtp[
            ['#sys_loc_code',
             'measurement_method',
             'remark',
             'Resp Coleta',
             'Cond clim',
             'Temp',
             'Cond elet',
             'OD',
             'ORP',
             'Turb']
        ]

        melt_segmento_ezmtp = pd.melt(segmento_ezmtp,
                                      id_vars=['#sys_loc_code'], var_name='param_code', value_name='param_value')

        return melt_segmento_ezmtp

    @staticmethod
    def __adicionando_identificadores_medicao(df_extracao: pd.DataFrame, df_ezmtp: pd.DataFrame):
        """
        Adiciona as colunas de identificação para data e método dos medições para o dataframe final.

        :param df_extracao:
        :type df_extracao: pd.DataFrame
        :param df_ezmtp:
        :type df_ezmtp: pd.DataFrame
        :return: pd.DataFrame
        """
        df_id = df_ezmtp[["#sys_loc_code", "measurement_method", "measurement_date", "remark"]]

        df_join = df_extracao.merge(df_id, on="#sys_loc_code", how="right")

        return df_join

    @staticmethod
    def __adicona_unidade_param(df_extracao: pd.DataFrame):
        """
        Realiza um apply no dataframe de extração, adicionando uma coluna para as unidades dos valores
        listados na planilha.

        :param df_extracao:
        :type df_extracao: pd.DataFrame
        :return: pd.DataFrame
        """
        def mapea_tipo_unidade(col_nome: str):
            if col_nome == "Cond elet":
                return "uS/cm"
            elif col_nome == "OD":
                return "mg/L"
            elif col_nome == "Temp":
                return "C"
            elif col_nome == "ORP":
                return "mV"
            elif col_nome == "Turb":
                return "NTU"
            else:
                return "-"

        df_extracao["param_unit"] = df_extracao["param_code"].apply(mapea_tipo_unidade)

        return df_extracao

    def consolida_arquivo(self, excel_path: str) -> pd.DataFrame:
        """
        Recebe o path para um arquivo de excel. O conteúdo de tal sendo consolidado em
        um único dataframe.

        :param excel_path: Path para o arquivo excel
        :type excel_path: str
        :return: pd.DataFrame
        """
        try:
            excel_dataframes = pd.read_excel(excel_path, sheet_name=['Cadastro', 'EZMtp'])
        except FileNotFoundError as e:
            raise FileNotFoundError(f"O arquivo {excel_path} não foi encontrado.") from e

        # Verificando se as abas necessárias estão presentes
        if 'Cadastro' not in excel_dataframes or 'EZMtp' not in excel_dataframes:
            raise ValueError("O arquivo Excel não contém as abas necessárias: 'Cadastro' e 'EZMtp'.")

        # Dados de cada sheet on excel
        cadastro_sheet_df = self.__cadastro_formatador(excel_dataframes["Cadastro"])
        ezmtp_sheet_df = self.__ezmtp_formatador(excel_dataframes["EZMtp"])

        self.__avalia_integridade_input(cadastro_sheet_df, ezmtp_sheet_df)
        self.__verificar_nan_no_dataframe(cadastro_sheet_df, sheet_nome="Cadastro")
        self.__verificar_nan_no_dataframe(cadastro_sheet_df, sheet_nome="EZMtp")

        # Processando os valores para o formato necessário
        ezmtp_sheet_df = self.__normaliza_nome_colunas_ezmtp(ezmtp_sheet_df)

        sheet_extracao = self.__extrai_valores_ezmt(ezmtp_sheet_df)
        sheet_extracao = self.__adicona_unidade_param(sheet_extracao)
        df_consolidado = self.__adicionando_identificadores_medicao(df_extracao=sheet_extracao,
                                                                    df_ezmtp=ezmtp_sheet_df)

        # Adicionando o identificador da task
        df_consolidado["task_code"] = cadastro_sheet_df["Task:*"][0]

        return df_consolidado