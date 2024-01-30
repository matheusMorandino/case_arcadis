from gui import GUI
import PySimpleGUI as sg
from fabricaConsolidador import FabricaConsolidador
import pandas as pd
from datetime import datetime
import sys
import os


def processar_arquivos(input_files: list[str], output_path: str, progress_bar: sg.Window):
    """
    Função responsável por chamar o consolidador de arquivos e processar as tabelas

    :param input_files:
    :param output_path:
    :param progress_bar:
    :return:
    """
    consolidador = FabricaConsolidador()
    df_processados = pd.DataFrame(columns=['#sys_loc_code', 'param_code', 'param_value', 'param_unit',
                                           'measurement_method', 'measurement_date', 'remark', 'task_code'])

    for i, file in enumerate(input_files, start=1):
        sg.one_line_progress_meter('Processando arquivos:', i, len(input_files), 'key',
                                   'Arquivo atual: ' + os.path.basename(file))

        try:
            df_auxiliar = consolidador.criar_consolidador(excel_path=file).consolida_arquivo(excel_path=file)
            df_processados = pd.concat([df_processados, df_auxiliar], ignore_index=True)
        except Exception as e:
            sg.popup_error(f"Erro {os.path.basename(file)}: {str(e)}")
            sys.exit()

        progress_bar.update_bar(i, len(input_files))

    sg.one_line_progress_meter_cancel('key')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_name = "case_3_consolidado_"+timestamp

    # Salvando resultado consolidado como .xslx
    df_processados.to_excel(os.path.join(output_path, output_name+".xlsx"), index=False)


if __name__ == "__main__":
    gui = GUI(nome_janela="Case 3", processar_arquivos=processar_arquivos)
    gui.get_eventos()
    gui.fechar_janela()
