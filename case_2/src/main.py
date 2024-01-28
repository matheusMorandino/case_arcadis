import os
import sys
from gui import GUI
import pandas as pd
import PySimpleGUI as sg
import unificadorTabelas
import outputConstrutor
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def processar_arquivos(input_files: list[str], output_path: str, progress_bar: sg.Window):
    """
    Função responsável por chamar o consolidador de arquivos e processar as tabelas

    :param input_files:
    :param output_path:
    :param progress_bar:
    :return:
    """
    unificador = unificadorTabelas.UnificadorTabela()

    df_processados = pd.DataFrame(columns=["CAS", "Parâmetro", "efeito", "Concentração de solubilidade",
                                           "Valor VOR (mg/l)", "VOR", "amb aberto", "CMA aberto", "amb fechado",
                                           "CMA fechado", "cinza_cma_aberto", "cinza_cma_fechado",
                                           "laranja_cma_aberto", "laranja_cma_fechado"])

    for i, file in enumerate(input_files, start=1):
        sg.one_line_progress_meter('Processando arquivos:', i, len(input_files), 'key',
                                   'Arquivo atual: ' + os.path.basename(file))

        try:
            df_auxiliar = unificador.consolida_dados_subistancias(file_path=file, para_output=True)
            df_processados = pd.concat([df_processados, df_auxiliar], ignore_index=True)
        except Exception as e:
            sg.popup_error(f"Erro {os.path.basename(file)}: {str(e)}")
            sys.exit()

    sg.one_line_progress_meter_cancel('key')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_name = "case_2_consolidado_" + timestamp

    # Salvando resultado consolidado como .xslx
    construtor_out = outputConstrutor.OutputConstrutor(df=df_processados)
    output_path = os.path.join(output_path, output_name+".xlsx")
    construtor_out.salvar_workbook_formatado(output_path)


if __name__ == "__main__":
    gui = GUI(nome_janela="Case 2", processar_arquivos=processar_arquivos)
    gui.get_eventos()
    gui.fechar_janela()
