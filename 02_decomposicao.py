from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


DATASET_PATH = Path(__file__).with_name("mecaniqa_dataset - mecaniqa_dataset.csv.csv")


def carregar_dataset(caminho: Path = DATASET_PATH) -> pd.DataFrame:
    """Carrega o dataset e configura a coluna Data como indice temporal."""
    dados = pd.read_csv(caminho, parse_dates=["Data"])
    dados = dados.set_index("Data").sort_index()
    dados.index.name = "Data"
    return dados


def decompor_serie(dados: pd.DataFrame) -> None:
    """Decompoe Trocas_Oleo em tendencia, sazonalidade e ruido."""
    serie = dados["Trocas_Oleo"].interpolate(method="time")
    resultado = seasonal_decompose(serie, model="additive", period=7)

    figura = resultado.plot()
    figura.set_size_inches(12, 9)
    figura.axes[0].set_title("Serie observada")
    figura.axes[1].set_title("Tendencia")
    figura.axes[2].set_title("Sazonalidade")
    figura.axes[3].set_title("Ruido (residuos)")
    figura.tight_layout()
    figura.savefig(Path(__file__).with_name("02_decomposicao_trocas_oleo.png"), dpi=150)
    plt.show()


if __name__ == "__main__":
    dataset = carregar_dataset()
    decompor_serie(dataset)
