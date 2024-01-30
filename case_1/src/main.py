import os
import sys
import pandas as pd
from gui import GUI
import PySimpleGUI as sg
from segmentadorPDF import SegmentadorPDF
from fabricaProcessadorPDF import FabricaProcessadorPDF
from construtorOutput import ConstrutorOutput
from datetime import datetime


def processar_arquivos(input_files: list[str], output_path: str, progress_bar: sg.Window):
    """
    Função responsável por chamar o consolidador de arquivos e processar as tabelas

    :param input_files:
    :param output_path:
    :param progress_bar:
    :return:
    """
    segmentador = SegmentadorPDF()

    df_processados = pd.DataFrame(columns=["Identificação interna", "Nome da amostra", "Data de coleta",
                                           "Horário de coleta", "Parâmetro químico", "Resultado",
                                           "Unidade", "Limite de Quantificação (LQ)"])

    for i, file in enumerate(input_files, start=1):
        sg.one_line_progress_meter('Processando arquivos:', i, len(input_files), 'key',
                                   'Arquivo atual: ' + os.path.basename(file))

        try:
            dados_segmentados = segmentador.segmenta_pdf(path_arquivo=file)
            processa_tabela = FabricaProcessadorPDF().criar_processador(tabelas_segmentadas=dados_segmentados)

            df_auxiliar = processa_tabela.formata_arquivo_pdf(tabelas_segmentadas=dados_segmentados)
            df_processados = pd.concat([df_processados, df_auxiliar], ignore_index=True)
        except Exception as e:
            sg.popup_error(f"Erro {os.path.basename(file)}: {str(e)}")
            sys.exit()

    sg.one_line_progress_meter_cancel('key')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_name = "case_1_consolidado_" + timestamp

    # Salvando resultado consolidado como .xslx
    output_path = os.path.join(output_path, output_name + ".xlsx")
    ConstrutorOutput(df=df_processados).salvar_workbook_formatado(output_path)


if __name__ == '__main__':
    gui = GUI(nome_janela="Case 1", processar_arquivos=processar_arquivos)
    gui.get_eventos()
    gui.fechar_janela()
