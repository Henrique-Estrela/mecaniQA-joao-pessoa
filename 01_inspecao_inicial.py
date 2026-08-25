from pathlib import Path

import pandas as pd


DATASET_PATH = Path(__file__).with_name("mecaniqa_dataset - mecaniqa_dataset.csv.csv")


def carregar_dataset(caminho: Path = DATASET_PATH) -> pd.DataFrame:
    """Carrega o dataset e configura a coluna Data como indice temporal."""
    dados = pd.read_csv(caminho, parse_dates=["Data"])
    dados = dados.set_index("Data").sort_index()
    dados.index.name = "Data"
    return dados


def inspecionar_dataset(dados: pd.DataFrame) -> None:
    """Exibe as primeiras linhas, informacoes e dimensoes da base."""
    print("\nPrimeiras linhas (.head()):")
    print(dados.head())

    print("\nInformacoes da base (.info()):")
    dados.info()

    print(f"\nDimensoes: {dados.shape[0]} registros x {dados.shape[1]} atributos")
    print(f"Periodo: {dados.index.min().date()} a {dados.index.max().date()}")
    print(f"Atributos: {', '.join(dados.columns)}")


if __name__ == "__main__":
    dataset = carregar_dataset()
    inspecionar_dataset(dataset)
