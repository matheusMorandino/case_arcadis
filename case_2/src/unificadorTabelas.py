import pandas as pd
from abc import ABC, abstractmethod


class UnificadorTabelas(ABC):
    @abstractmethod
    def consolida_dados_subistancias(self, file_path: str, para_output: bool=False) -> pd.DataFrame:
        """
        Método abstrato que as subclasses devem implementar para consolida os dados da planilha de
        exposição de compostos.

        :param file_path: path para arquivo de input
        :type file_path: str
        :param para_output: Se o dataframe deve ser preprocessado para o output em excel
        :type para_output: bool
        :return:
        """
        pass