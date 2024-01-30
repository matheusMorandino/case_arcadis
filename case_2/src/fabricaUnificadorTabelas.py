import openpyxl
from sheetNomeEnum import SheetNome
from unificadorTabelas import UnificadorTabelas
from unificadorTabelasExemplo import UnificadorTabelasExemplo


class FabricaUnificadorTabelas:
    @staticmethod
    def criar_unificador(file_path: str) -> UnificadorTabelas:
        """
        Factory method responsável por detectar qual tipo de arquivo o xlsx atual é retornar o objeto correspondente
        para processamento das tabelas presentes

        :param file_path: path para arquivo de input
        :type file_path: str
        :return: UnificadorTabelas
        """
        workbook = openpyxl.load_workbook(file_path)
        sheet_nomes = workbook.sheetnames

        if set(SheetNome.NOMES_EXEMPLO.value) == set(sheet_nomes):
            return UnificadorTabelasExemplo()
        else:
            err_msg = ("Arquivo atual não é de um tipo reconhecido. Por favor não seleciona-lo para processamento \n\n" +
                       "Arquivo em processamento: " + str(file_path))
            raise Exception(err_msg)