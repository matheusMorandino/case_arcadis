import pandas as pd
from abc import ABC, abstractmethod


class ConsolidadorTabela(ABC):
    @abstractmethod
    def consolida_arquivo(self, excel_path: str) -> pd.DataFrame:
        """
        Recebe o path para um arquivo de excel. O conteúdo de tal sendo consolidado em
        um único dataframe.

        :param excel_path: Path para o arquivo excel
        :type excel_path: str
        :return: pd.DataFrame
        """
        pass