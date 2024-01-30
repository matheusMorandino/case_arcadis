import pandas as pd
from abc import ABC, abstractmethod


class ProcessadorTabela(ABC):
    @abstractmethod
    def formata_arquivo_pdf(self, tabelas_segmentadas: dict) -> pd.DataFrame:
        """
        Método abstrato que as subclasses devem implementar para formatar um arquivo PDF.

        :param tabelas_segmentadas: dict com as tabelas segmentas do pdf
        :type tabelas_segmentadas: dict
        :return: pd.DataFrame
        """
        pass