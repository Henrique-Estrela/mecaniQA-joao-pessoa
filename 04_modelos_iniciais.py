from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATASET_PATH = Path(__file__).with_name("mecaniqa_dataset - mecaniqa_dataset.csv.csv")


def carregar_dataset(caminho: Path = DATASET_PATH) -> pd.DataFrame:
    """Carrega o dataset e configura a coluna Data como indice temporal."""
    dados = pd.read_csv(caminho, parse_dates=["Data"])
    dados = dados.set_index("Data").sort_index()
    dados.index.name = "Data"
    return dados


def preparar_treino_teste(dados: pd.DataFrame):
    """Monta X e y para prever as trocas de amanha, sem embaralhar o tempo."""
    tabela = pd.DataFrame({
        "trocas_hoje": dados["Trocas_Oleo"],
        "manutencao_hoje": dados["Manutencao_Motor"],
        "trocas_semana_passada": dados["Trocas_Oleo"].shift(7),
        "dia_semana": dados.index.day_name(),
        "trocas_amanha": dados["Trocas_Oleo"].shift(-1),
    }).dropna(subset=["trocas_amanha"])

    X = tabela.drop(columns=["trocas_amanha"])
    y = tabela["trocas_amanha"]
    corte = int(len(tabela) * 0.8)
    return X.iloc[:corte], X.iloc[corte:], y.iloc[:corte], y.iloc[corte:]


def criar_pipeline(modelo) -> Pipeline:
    """Imputacao, encoding e escala, com o modelo nos hiperparametros de fabrica."""
    numeros = Pipeline([
        ("imputar", SimpleImputer(strategy="median")),
        ("escalar", StandardScaler()),
    ])
    textos = Pipeline([
        ("imputar", SimpleImputer(strategy="most_frequent")),
        ("codificar", OneHotEncoder(handle_unknown="ignore")),
    ])
    preparo = ColumnTransformer([
        ("numeros", numeros, ["trocas_hoje", "manutencao_hoje", "trocas_semana_passada"]),
        ("textos", textos, ["dia_semana"]),
    ])
    return Pipeline([
        ("preparo", preparo),
        ("modelo", modelo),
    ])


def mostrar_erro(nome: str, real, previsto) -> None:
    rmse = root_mean_squared_error(real, previsto)
    mape = mean_absolute_percentage_error(real, previsto) * 100
    print(f"{nome:32} RMSE {rmse:6.2f}   MAPE {mape:5.1f}%")


if __name__ == "__main__":
    dataset = carregar_dataset()
    X_train, X_test, y_train, y_test = preparar_treino_teste(dataset)

    media_movel = dataset["Trocas_Oleo"].rolling(7).mean().reindex(y_test.index)

    print(f"Treino: {X_train.index.min().date()} a {X_train.index.max().date()}")
    print(f"Teste:  {X_test.index.min().date()} a {X_test.index.max().date()}\n")
    mostrar_erro("Baseline naive (amanha = hoje)", y_test, X_test["trocas_hoje"])
    mostrar_erro("Baseline media movel 7 dias", y_test, media_movel)

    modelos = {
        "Random Forest (padrao)": RandomForestRegressor(random_state=42),
        "Gradient Boosting (padrao)": GradientBoostingRegressor(random_state=42),
    }
    for nome, modelo in modelos.items():
        pipeline = criar_pipeline(modelo)
        pipeline.fit(X_train, y_train)
        mostrar_erro(nome, y_test, pipeline.predict(X_test))
