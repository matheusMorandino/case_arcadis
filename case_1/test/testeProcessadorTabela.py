import os
import pytest
import pandas as pd
import numpy as np
from src.processadorTabela import ProcessadorTabela

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cria_df_teste_cru():
    data = {
        0: ['', 'DADOS REFERENTES AO CLIENTE', '', '', '', '', '', '', ''],
        1: ['', 'Cliente:', 'Endereço:', 'Contato:', 'Item de Ensaiol:', 'Observações:', 'Data da Amostragem :',
            'Data de Recebimento:', 'Resultado da Amostra'],
        2: ['', 'Empresa XYZ', 'Rua Principal, 123 - Bairro Central, Rio de Janeiro/RJ', 'Joana Silva', 'Teste A',
            'Amostra de produto X', '15/02/2024 10:30', '16/02/2024 14:45', 'Aprovado'],
        3: ['', 'RESUMO DOS RESULTADOS DA AMOSTRA N° 00001/2024-1', '', '', '', '', '', '', ''],
        4: ['', 'Cliente:', 'Endereço:', 'Contato:', 'Item de Ensaiol:', 'Observações:', 'Data da Amostragem :',
            'Data de Recebimento:', 'Resultado da Amostra'],
        5: ['', 'Empresa ABC', 'Av. Desconhecida, 789 - Bairro Desinformado, São Paulo/SP', 'Carlos Oliveira',
            'Teste B', 'Amostra de produto Y', '16/02/2024 11:00', '17/02/2024 15:20', 'Reprovado'],
        6: ['', 'RESUMO DOS RESULTADOS DA AMOSTRA N° 00002/2024-2', '', '', '', '', '', '', ''],
        7: ['', 'Cliente:', 'Endereço:', 'Contato:', 'Item de Ensaiol:', 'Observações:', 'Data da Amostragem :',
             'Data de Recebimento:', 'Resultado da Amostra'],
        8: ['', 'Empresa LMN', 'Rua Desinformada, 456 - Bairro Central, São Paulo/SP', 'Lucas Santos', 'Teste C',
             'Amostra de produto Z', '17/02/2024 09:45', '18/02/2024 13:15', 'Aprovado'],
    }

    return pd.DataFrame(data).T

def cria_df_info_cliente_cru():
    dado = {0: ['Identificação do item de ensaio:',
                 'Identificação do Cliente:',
                 'Amostra  Rotulada como:',
                 'Coletor:',
                 'Data da Amostragem  :',
                 'Data da entrada no laboratório:'],
             1: ['123456',
                 'Client123',
                 'Teste',
                 'Ful',
                 '2022-01-01',
                 '2022-01-02'],
             2: [np.nan,
                 np.nan,
                 np.nan,
                 np.nan,
                 np.nan,
                 'Data de Elaboração do RRA:'],
             3: [np.nan,
                 np.nan,
                 np.nan,
                 np.nan,
                 np.nan,
                 '24/01/2024']
             }

    return pd.DataFrame(dado)


@pytest.fixture
def example_pdf_path():
    return os.path.join(ROOT_DIR, "input\\Material_Case_Ex1.pdf")

def test_extrai_tabela_do_pdf(example_pdf_path):
    processador = ProcessadorTabela()
    df = processador._ProcessadorTabela__extrai_tabela_do_pdf(example_pdf_path)
    assert isinstance(df, pd.DataFrame)


def test_extrai_segmentos():
    df = cria_df_teste_cru()

    processador = ProcessadorTabela()
    segmentos = processador._ProcessadorTabela__extrai_segmentos(df)

    assert 'DADOS REFERENTES AO CLIENTE' in segmentos.keys()
    assert 'RESUMO DOS RESULTADOS DA AMOSTRA N° 00001/2024-1' in segmentos.keys()
    assert 'RESUMO DOS RESULTADOS DA AMOSTRA N° 00002/2024-2' in segmentos.keys()

def test_colapsar_espacos_vazio():
    # Create a sample DataFrame for testing
    df = pd.DataFrame({
        'col1': [1, '', 3],
        'col2': ['', 5, 6],
        'col3': [7, 8, '']
    })

    processador = ProcessadorTabela()
    df_limpo = processador._ProcessadorTabela__colapsar_espacos_vazio(df)

    assert len(df_limpo.columns) == 2
    assert len(df_limpo) == 3


def test_formata_arquivo_pdf(example_pdf_path):
    processador = ProcessadorTabela()
    df_result = processador.formata_arquivo_pdf(example_pdf_path)

    assert isinstance(df_result, pd.DataFrame)
    assert len(df_result) > 0
    assert 'Identificação interna' in df_result.columns
    assert 'Parâmetro químico' in df_result.columns
    assert 'Resultado' in df_result.columns


def test_cria_df_info_amostra():
    segment = {'DADOS REFERENTES A AMOSTRA': cria_df_info_cliente_cru()}

    processador = ProcessadorTabela()
    df_info_amostra = processador._ProcessadorTabela__cria_df_info_amostra(segment)

    assert isinstance(df_info_amostra, pd.DataFrame)
    assert 'Identificação do Cliente:' in df_info_amostra.columns
    assert 'Data da Amostragem  :' in df_info_amostra.columns
    assert 'Data de Elaboração do RRA:' not in df_info_amostra.columns
    assert 'Client123' == df_info_amostra['Identificação do Cliente:'][0]
    assert '2022-01-01' == df_info_amostra['Data da Amostragem  :'][0]
