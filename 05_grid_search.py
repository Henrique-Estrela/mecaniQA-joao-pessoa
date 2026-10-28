from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATASET_PATH = Path(__file__).with_name("mecaniqa_dataset - mecaniqa_dataset.csv.csv")

PARAMETROS = {
    "modelo__n_estimators": [50, 100, 200],
    "modelo__max_depth": [2, 3, 5],
    "modelo__learning_rate": [0.05, 0.1, 0.2],
}


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
    """Imputacao, encoding e escala, e depois o Gradient Boosting."""
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


def mape(real, previsto) -> float:
    return mean_absolute_percentage_error(real, previsto) * 100


if __name__ == "__main__":
    dataset = carregar_dataset()
    X_train, X_test, y_train, y_test = preparar_treino_teste(dataset)

    padrao = criar_pipeline(GradientBoostingRegressor(random_state=42))
    padrao.fit(X_train, y_train)
    mape_padrao = mape(y_test, padrao.predict(X_test))

    busca = GridSearchCV(
        criar_pipeline(GradientBoostingRegressor(random_state=42)),
        PARAMETROS,
        cv=TimeSeriesSplit(n_splits=5),
        scoring="neg_mean_absolute_percentage_error",
    )
    busca.fit(X_train, y_train)
    mape_tunado = mape(y_test, busca.predict(X_test))
    reducao = (mape_padrao - mape_tunado) / mape_padrao * 100

    print("best_params_:")
    print(busca.best_params_)
    print(f"\nMAPE da semana passada: {mape_padrao:.1f}%")
    print(f"MAPE tunado:            {mape_tunado:.1f}%")
    print(f"Reducao do erro:        {reducao:.1f}%")
