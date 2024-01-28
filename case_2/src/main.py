import os
import unificadorTabelas

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_path = os.path.join(ROOT_DIR, "input", "Material_Case_Ex2.xlsx")

    unificador = unificadorTabelas.UnificadorTabela()

    df = unificador.consolida_dados_subistancias(input_path, para_output=True)

    print(df.to_string())