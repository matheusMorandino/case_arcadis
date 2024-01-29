import PySimpleGUI as sg


class GUI:
    def __init__(self, nome_janela: str, processar_arquivos=lambda input_files, output_path, progress_bar: None):
        self.arquivos_selecionados = []
        self.output_path = ""

        # Definindo GUI layout
        self.layout = [
            [sg.Text("Selecione o(s) arquivo(s) .pdf:"), sg.Input(key="-FILES-", enable_events=True),
             sg.FilesBrowse(file_types=(("PDF Files", "*.pdf"),))],
            [sg.Text("Output Path:"), sg.Input(key="-OUTPUT-", enable_events=True), sg.FolderBrowse()],
            [sg.Button("Processar", key="-RUN-")]
        ]

        # Criando janela
        self.window = sg.Window(nome_janela, self.layout)

        # Implementando a função de processamento de arquivos
        self.processar_arquivos_callback = processar_arquivos

    def limpar_campos_input(self):
        self.window["-FILES-"].update("")
        self.window["-OUTPUT-"].update("")

    def get_eventos(self):
        while True:
            event, valor = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "-FILES-":
                self.arquivos_selecionados = valor["-FILES-"].split(";")
            elif event == "-OUTPUT-":
                self.output_path = valor["-OUTPUT-"]
            elif event == "-RUN-":
                if not self.arquivos_selecionados or not self.output_path:
                    sg.popup_error("Por favor selecione um caminho para o output e pelo menos um arquivo de input.")
                else:
                    progress_layout = [
                        [sg.Text("Processando arquivos")],
                        [sg.ProgressBar(len(self.arquivos_selecionados), orientation='h', size=(20, 20), key='-PROGRESS-')],
                    ]

                    progress_window = sg.Window("Processando", progress_layout, finalize=True)
                    progress_bar = progress_window['-PROGRESS-']

                    self.processar_arquivos_callback(self.arquivos_selecionados, self.output_path, progress_bar)
                    self.limpar_campos_input()

                    progress_window.close()
                    sg.popup("Processamento completo!")

    def fechar_janela(self):
        self.window.close()
