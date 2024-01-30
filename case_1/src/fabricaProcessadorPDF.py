from segmentosKeysEnum import SegmentosKeys
from processadorTabela import ProcessadorTabela
from processadorTabelaExemplo import ProcessadorTabelaExemplo


class FabricaProcessadorPDF:
    @staticmethod
    def criar_processador(file_path: str, tabelas_segmentadas: dict) -> ProcessadorTabela:
        """
        Factory method responsável por detectar qual tipo de arquivo o pdf atual é retornar o objeto correspondente
        para processamento das tabelas presentes

        :param file_path: path para arquivo de input
        :type file_path: str
        :param tabelas_segmentadas: dict com as tabelas segmentas do pdf
        :type tabelas_segmentadas: dict
        :return: ProcessadorTabela
        """
        if all(x == y for x, y in zip(tabelas_segmentadas.keys(), SegmentosKeys.TIPO_EXEMPLO.value)):
            return ProcessadorTabelaExemplo()
        else:
            err_msg = ("Arquivo atual não é de um tipo reconhecido. Por favor não seleciona-lo para processamento \n\n" +
                       "Arquivo em processamento: " + str(file_path))
            raise Exception(err_msg)
