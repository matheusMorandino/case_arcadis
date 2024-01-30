import openpyxl
from sheetNomeEnum import SheetNome
from consolidadorTabela import ConsolidadorTabela
from consolidadorTabelaExemplo import ConsolidadorTabelaExemplo

class FabricaConsolidador:
    @staticmethod
    def criar_consolidador(excel_path: str) -> ConsolidadorTabela:
        """
        Factory method responsável por detectar qual tipo de arquivo o xlsx atual é retornar o objeto correspondente
        para processamento das tabelas presentes

        :param file_path: path para arquivo de input
        :type file_path: str
        :return: UnificadorTabelas
        """
        workbook = openpyxl.load_workbook(excel_path)
        sheet_nomes = workbook.sheetnames

        if set(SheetNome.NOMES_EXEMPLO.value) == set(sheet_nomes):
            return ConsolidadorTabelaExemplo()
        else:
            err_msg = ("Arquivo atual não é de um tipo reconhecido. Por favor não seleciona-lo para processamento \n\n" +
                       "Arquivo em processamento: " + str(excel_path))
            raise Exception(err_msg)
