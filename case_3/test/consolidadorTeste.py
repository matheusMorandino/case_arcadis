import numpy as np
import pandas as pd
import pytest
from src.consolidadorTabela import ConsolidadorTabela

# Criar dados de exemplo para os testes
cadastro_data = {
    "Cliente:": ["Cliente1"],
    "Código:": [1],
    "Task:*": ["Task1"],
    "Solicitante (nome e sobrenome):*": ["Solicitante1"]
}

ezmtp_data = {
    "sys_loc_code": [1, 2],
    "Data da medição": ["2022-01-01", "2022-01-02"],
    "Hora da medição": ["10:00:00", "12:00:00"],
    "Método de coleta": ["Coleta1", "Coleta2"],
    "Tipo do turbidímetro": ["Turbid1", "Turbid2"],
    "Temp. \n(°C)": [25.5, 26.0],
    "Condutividade (µS/cm)": [500, 550],
    "OD \n(mg/L)": [5.0, 5.5],
    "pH": [7.0, 7.2],
    "ORP \n(mV)": [200, 210],
    "Turbidez \n(NTU)": [10.0, 11.0],
    "Responsável pela coleta": ["Responsavel1", "Responsavel2"],
    "Condição climática": ["Clima1", "Clima2"]
}

# Converter dados em DataFrames
df_cadastro = pd.DataFrame(cadastro_data)
df_ezmtp = pd.DataFrame(ezmtp_data)

# Testes
def test_normaliza_nome_colunas_ezmtp():
    consolidador = ConsolidadorTabela()
    result_df = consolidador.normaliza_nome_colunas_ezmtp(df_ezmtp)
    assert set(result_df.columns) == {
        "#sys_loc_code", "measurement_method", "remark", "Resp Coleta", "Cond clim", "Temp", "pH", "measurement_date", "Cond elet", "OD", "ORP", "Turb"
    }

def test_avalia_integridade_input():
    consolidador = ConsolidadorTabela()
    with pytest.raises(ValueError, match="Colunas necessárias ausentes: Cliente:"):
        consolidador.avalia_integridade_input(df_cadastro.drop(columns=["Cliente:"]), df_ezmtp)

def test_verificar_nan_no_dataframe():
    consolidador = ConsolidadorTabela()
    ezmtp_data_nan = ezmtp_data
    ezmtp_data_nan["Data da medição"] = ["2022-01-01", np.nan]
    ezmt_df_nan = pd.DataFrame(ezmtp_data_nan)

    with pytest.raises(ValueError, match="A planilha EZMtp contém valores vazios e/ou inválidos.\nCoordenadas dos valores inválidos:\nLinha: 1, Coluna: Data da medição\n"):
        consolidador.verificar_nan_no_dataframe(ezmt_df_nan, sheet_nome="EZMtp")

def test_adicionando_identificadores_medicao():
    consolidador = ConsolidadorTabela()
    # Garanta que as colunas necessárias estejam presentes nos dataframes
    ezmtp_sheet_df = consolidador.normaliza_nome_colunas_ezmtp(df_ezmtp)
    df_extracao = consolidador.extrai_valores_ezmt(ezmtp_sheet_df)
    df_id = consolidador.normaliza_nome_colunas_ezmtp(df_ezmtp)

    # Realize a junção
    result_df = consolidador.adicionando_identificadores_medicao(df_extracao=df_extracao, df_ezmtp=df_id)

    # Verifique se as colunas identificadoras estão presentes no resultado
    assert all(
        col in result_df.columns for col in ["#sys_loc_code", "measurement_method", "measurement_date", "remark"])


def test_adicona_unidade_param():
    consolidador = ConsolidadorTabela()
    ezmtp_sheet_df = consolidador.normaliza_nome_colunas_ezmtp(df_ezmtp)
    df_extracao = consolidador.extrai_valores_ezmt(ezmtp_sheet_df)

    # Aplique a função
    result_df = consolidador.adicona_unidade_param(df_extracao)

    # Verifique se a coluna "param_unit" está presente no resultado
    assert "param_unit" in result_df.columns

    # Verifique se as unidades estão corretamente atribuídas
    assert result_df.loc[0, "param_unit"] == "-"
    assert result_df.loc[1, "param_unit"] == "-"
