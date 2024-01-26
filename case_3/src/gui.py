import PySimpleGUI as sg
from consolidadorTabela import ConsolidadorTabela
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
    consolidador = ConsolidadorTabela()
    df_processados = pd.DataFrame(columns=['#sys_loc_code', 'param_code', 'param_value', 'param_unit',
       'measurement_method', 'measurement_date', 'remark', 'task_code'])

    for i, file in enumerate(input_files, start=1):
        sg.one_line_progress_meter('Processando arquivos:', i, len(input_files), 'key',
                                   'Arquivo atual: ' + os.path.basename(file))

        try:
            df_auxiliar = consolidador.consolida_arquivo(excel_path=file)
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

# Define GUI layout
layout = [
    [sg.Text("Selecione o(s) arquivo(s) .xlsx:"), sg.Input(key="-FILES-", enable_events=True), sg.FilesBrowse(file_types=(("Excel Files", "*.xlsx"),))],
    [sg.Text("Output Path:"), sg.Input(key="-OUTPUT-", enable_events=True), sg.FolderBrowse()],
    [sg.Button("Processar", key="-RUN-")]
]

# Create the window
window = sg.Window("Case 3", layout)

arquivos_selecionados = []
output_path = ""
csv_check = False
json_check = False

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == "-FILES-":
        arquivos_selecionados = values["-FILES-"].split(";")
    elif event == "-OUTPUT-":
        output_path = values["-OUTPUT-"]
    elif event == "-RUN-":
        if not arquivos_selecionados or not output_path:
            sg.popup_error("Por favor selecione um caminho para o output e pelo menos um arquivo de input.")
        else:
            progress_layout = [
                [sg.Text("Processando arquivos")],
                [sg.ProgressBar(len(arquivos_selecionados), orientation='h', size=(20, 20), key='-PROGRESS-')],
            ]

            progress_window = sg.Window("Processando", progress_layout, finalize=True)
            progress_bar = progress_window['-PROGRESS-']

            processar_arquivos(arquivos_selecionados, output_path, progress_bar)

            progress_window.close()
            sg.popup("Processamento completo!")

window.close()
