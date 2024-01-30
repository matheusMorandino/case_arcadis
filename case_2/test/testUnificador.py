import pandas as pd
import numpy as np
import pytest
from src import unificadorTabelasExemplo


# Helper function to create a sample DataFrame for testing
def create_sample_flag_df():
    data = {
        'CAS': ['123-45-6', '789-10-1'],
        'Parâmetro': ['A', 'B'],
        'efeito': ['Effect1', 'Effect2'],
        'amb aberto': [1.0, 2.0],
        'amb fechado': [3.0, 4.0],
        'CMA aberto': [5.0, 6.0],
        'CMA fechado': [7.0, 8.0],
        'Concentração de solubilidade': [500, 500],
        'Valor VOR (mg/l)': [10.0, 12.0],
        'VOR': [15.0, 18.0],
        'cinza_cma_aberto': [False, True],
        'cinza_cma_fechado': [True, False],
        'laranja_cma_aberto': [False, True],
        'laranja_cma_fechado': [True, False],
    }
    return pd.DataFrame(data)


def create_sample_df():
    data = {
        'CAS': ['123-45-6', '789-10-1'],
        'Parâmetro': ['A', 'B'],
        'efeito': ['Effect1', 'Effect2'],
        'amb aberto': [1.0, 2.0],
        'amb fechado': [3.0, 4.0],
        'CMA aberto': [5.0, 6.0],
        'CMA fechado': [7.0, 8.0],
        'Concentração de solubilidade': [500, 500],
        'Valor VOR (mg/l)': [10.0, 12.0],
        'VOR': [15.0, 18.0],
    }
    return pd.DataFrame(data)


def create_sample_sem_cma_df():
    data = {
        'CAS': ['123-45-6', '789-10-1'],
        'Parâmetro': ['A', 'B'],
        'efeito': ['Effect1', 'Effect2'],
        'amb aberto': [1.0, 2.0],
        'amb fechado': [3.0, 4.0],
        'Concentração de solubilidade': [500, 500],
        'Valor VOR (mg/l)': [10.0, 12.0],
        'VOR': [15.0, 18.0],
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_unificador_tabela():
    return unificadorTabelasExemplo.UnificadorTabelasExemplo()


def test_calcula_cma(sample_unificador_tabela):
    input_df = create_sample_df()
    result_df = sample_unificador_tabela._UnificadorTabela__calcula_cma(input_df, 'amb aberto', 'CMA aberto')
    expected_cols = {'CAS', 'Parâmetro', 'CMA aberto'}

    assert set(result_df.columns) == expected_cols


def test_criar_colunas_cma(sample_unificador_tabela):
    input_df = create_sample_sem_cma_df()
    result_df = sample_unificador_tabela._UnificadorTabela__criar_colunas_cma(input_df)
    expected_cols = {'CAS', 'Parâmetro', 'efeito', 'amb aberto', 'amb fechado', 'Concentração de solubilidade',
                     'Valor VOR (mg/l)', 'VOR', 'CMA aberto', 'CMA fechado'}

    assert set(result_df.columns) == expected_cols


def test_adiciona_flag_cma_maior_solubilidade(sample_unificador_tabela):
    input_df = create_sample_df()
    result_df = sample_unificador_tabela._UnificadorTabela__adiciona_flag_cma_maior_solubilidade(input_df)
    expected_cols = {'CAS', 'Parâmetro', 'efeito', 'amb aberto', 'amb fechado', 'Concentração de solubilidade',
                     'Valor VOR (mg/l)', 'VOR', 'CMA aberto', 'CMA fechado', 'cinza_cma_aberto', 'cinza_cma_fechado'}

    assert set(result_df.columns) == expected_cols


def test_adiciona_flag_vor_maior_cma(sample_unificador_tabela):
    input_df = create_sample_df()
    result_df = sample_unificador_tabela._UnificadorTabela__adiciona_flag_vor_maior_cma(input_df)
    expected_cols = {'CAS', 'Parâmetro', 'efeito', 'Concentração de solubilidade', 'amb aberto', 'amb fechado',
                     'CMA aberto', 'CMA fechado', 'Valor VOR (mg/l)', 'VOR', 'laranja_cma_aberto',
                     'laranja_cma_fechado'}

    assert set(result_df.columns) == expected_cols


def test_adiciona_flags_para_output(sample_unificador_tabela):
    input_df = create_sample_df()
    result_df = sample_unificador_tabela._UnificadorTabela__adiciona_flags_para_output(input_df)
    expected_cols ={'CAS', 'Parâmetro', 'efeito', 'amb aberto', 'amb fechado', 'CMA aberto','CMA fechado',
                    'Concentração de solubilidade', 'Valor VOR (mg/l)','VOR', 'cinza_cma_aberto',
                    'cinza_cma_fechado', 'laranja_cma_aberto', 'laranja_cma_fechado'}

    assert set(result_df.columns) == expected_cols


def test_atualiza_cma_menor_que_vor(sample_unificador_tabela):
    input_df = create_sample_df()
    result_df = sample_unificador_tabela._UnificadorTabela__atualiza_cma_menor_que_vor(input_df)
    expected_cols = {'CAS', 'Parâmetro', 'efeito', 'amb aberto', 'amb fechado', 'CMA aberto',
                     'CMA fechado', 'Concentração de solubilidade', 'Valor VOR (mg/l)', 'VOR'}

    assert set(result_df.columns) == expected_cols
