# Relatório da OAT 3 — Tunando o meu Modelo

Este documento descreve como os requisitos de código da OAT 3 foram implementados no notebook da equipe, onde encontrar cada parte e quais resultados estavam registrados na última execução conferida.

## Referências do projeto

- Enunciado: [OAT 3 - Tunando o meu Modelo (1).pdf](./OAT%203%20-%20Tunando%20o%20meu%20Modelo%20(1).pdf)
- Notebook: [mecaniqa_joao_pessoa.ipynb](./mecaniqa_joao_pessoa.ipynb)
- Base temporal: [mecaniqa_dataset - mecaniqa_dataset.csv.csv](./mecaniqa_dataset%20-%20mecaniqa_dataset.csv.csv)

As localizações abaixo usam os títulos das seções do notebook. No Jupyter, procure esses títulos e leia a célula de código logo abaixo de cada seção.

## Resumo

A OAT 3 amplia o trabalho anterior sem remover a preparação dos dados, a análise temporal, a engenharia de atributos nem os baselines. Sobre a mesma série histórica, foram adicionados dois modelos de regressão, validação temporal, busca exaustiva e aleatória de hiperparâmetros e uma comparação final, com métricas e gráfico, entre baseline, modelo inicial e modelo tunado.

| Requisito de código do enunciado | Implementação no notebook | Situação |
|---|---|---|
| Continuar usando a série temporal MecaniQA | Dataset diário de 2024–2025 carregado no início do notebook; a previsão de OAT 3 usa `Trocas_Oleo` | Implementado |
| Treinar ao menos dois modelos clássicos de regressão com `fit()` e produzir previsões com `predict()` | Regressão Linear e Árvore de Decisão, treinadas em cinco divisões cronológicas | Implementado |
| Aplicar Grid Search com espaço de hiperparâmetros e `TimeSeriesSplit` | `GridSearchCV`, 12 combinações, cinco folds, MAPE como critério; imprime `best_params_` e compara com a árvore padrão | Implementado |
| Aplicar Random Search e limitar iterações | `RandomizedSearchCV`, `n_iter=6`, mesmos dados, estimador, folds e critério da busca exaustiva | Implementado |
| Comparar tempo e precisão das buscas | Tempos medidos com `time.perf_counter()`; tabela e mensagens mostram diferenças de tempo e MAPE | Implementado |
| Comparar baseline antigo, modelo inicial e modelo tunado usando MAE, RMSE e MAPE | Métricas calculadas sobre os mesmos pontos de teste fora da amostra | Implementado |
| Mostrar uma comparação visual das previsões | Gráfico de valores reais, baseline MM7 e modelo tunado | Implementado |
| Versionar apresentação da OAT 3 e entregá-la no Blackboard | Não há apresentação OAT 3 entre os arquivos conferidos; a submissão no Blackboard não pode ser verificada pelo repositório | Pendente de confirmação/entrega externa |
| Garantir que a versão avaliada esteja na branch `main` | O estado local contém alterações ainda não confirmadas; a publicação na branch `main` deve ser confirmada pela equipe | Pendente de confirmação |

## O que foi preservado das etapas anteriores

O notebook continua usando a base diária e mantém a inspeção dos dados, o tratamento de picos, a decomposição sazonal e a criação de atributos temporais. Essas partes dão contexto aos modelos novos e não foram substituídas pela OAT 3.

- **Preparação, inspeção e tratamento da série:** seções 1, 2 e 2.1.
- **Decomposição temporal:** seção 3.
- **Atributos e prevenção de vazamento:** seção 3.1 e a célula de criação das features. Os lags de 1, 7 e 30 dias são deslocados para usar valores anteriores; as médias móveis de 7 e 30 dias usam `shift(1)`. Há verificações `assert` para conferir os valores calculados.
- **Baselines Naive, MM7 e MM30 e métricas temporais:** seções 4.1 e 4.2. Os baselines continuam disponíveis para servir de referência à nova modelagem.

## Implementações da OAT 3

### 1. Modelos clássicos de regressão

**Onde:** seção **4.3 — Regressões clássicas com hiperparâmetros padrão**.

**Como:** o notebook seleciona cinco atributos causais de `Trocas_Oleo`: lags de 1, 7 e 30 dias e médias móveis de 7 e 30 dias. A coluna `Trocas_Oleo` é o alvo. São instanciados `LinearRegression()` e `DecisionTreeRegressor()` sem parâmetros adicionais, respeitando a exigência de avaliar modelos iniciais com as configurações padrão da biblioteca. Em cada divisão do `TimeSeriesSplit`, o código treina somente com o trecho passado (`fit`) e prevê o trecho posterior (`predict`).

A tabela dessa seção combina os resultados da regressão com os resultados dos baselines, incluindo RMSE e MAPE. A comparação final mais adiante acrescenta o MAE para os três cenários pedidos pelo enunciado.

### 2. Busca exaustiva de hiperparâmetros — Grid Search

**Onde:** seção **4.4 — Otimização de hiperparâmetros com GridSearchCV**.

**Como:** o espaço de busca é definido por `parametros_arvore`:

```python
{
    "max_depth": [2, 3, 5, None],
    "min_samples_leaf": [1, 3, 5],
}
```

São 12 combinações. O `GridSearchCV` usa `TimeSeriesSplit(n_splits=5)`, `DecisionTreeRegressor(random_state=42)` e um scorer que calcula o MAPE pela função `metricas_erro`. Como o scikit-learn maximiza scores, o scorer retorna o MAPE com sinal negativo. Assim, a busca seleciona a menor média de MAPE entre os folds.

A saída mostra os melhores parâmetros, o MAPE da árvore padrão e o MAPE da configuração vencedora. Também calcula a redução percentual do MAPE em relação à árvore padrão — referência coerente para medir o impacto da otimização do mesmo modelo.

### 3. Busca aleatória e comparação de custo versus erro

**Onde:** seção **4.5 — Busca aleatória com RandomizedSearchCV** e subseção **Trade-off: tempo contra erro**.

**Como:** a busca aleatória usa `RandomizedSearchCV` com `n_iter=6` e `random_state=42`. Ela compartilha com o Grid Search o estimador com semente fixa, o espaço de parâmetros, o `TimeSeriesSplit` com cinco folds e o critério MAPE. Ambas rodam com `n_jobs=1`, permitindo comparar a duração sem introduzir a diferença de abrir múltiplos processos. O tempo é medido com `time.perf_counter()`.

Uma tabela apresenta o número de combinações avaliadas, o tempo, o MAPE e os melhores parâmetros de cada busca. Mensagens adicionais explicam se a busca aleatória economizou ou gastou mais tempo e se o erro aumentou, diminuiu ou permaneceu igual. Essa comparação é medida novamente ao executar o notebook; os tempos não são tratados como valores universais.

### 4. Avaliação final: baseline, modelo inicial e modelo tunado

**Onde:** seção **4.6 — Motor de métricas e comparação visual**.

**Como:** a função `previsao_fora_da_amostra` refaz o treinamento fold a fold e guarda previsões apenas nos blocos de teste. A configuração tunada é escolhida entre os resultados do Grid Search e do Random Search, tomando a que obteve menor MAPE médio.

Com as mesmas datas previstas, a célula calcula simultaneamente:

1. **Baseline MM7:** média móvel de sete dias já calculada com histórico anterior ao dia previsto.
2. **Modelo ML inicial:** árvore de decisão com parâmetros padrão.
3. **Modelo ML tunado:** árvore com os parâmetros vencedores da busca selecionada.

Para cada cenário são calculados MAE, RMSE e MAPE. Em seguida, a célula calcula e imprime a redução percentual de cada erro do modelo tunado em relação ao baseline MM7. O gráfico sobrepõe a demanda real, o baseline MM7 e as previsões fora da amostra do modelo tunado, como solicitado no enunciado.

### 5. Resumo da entrega técnica no notebook

**Onde:** seção **5 — Resumo da Entrega Técnica**.

Essa seção final resume os modelos, as buscas, a comparação das métricas e a visualização, e orienta a interpretar as saídas geradas pelo notebook, em vez de afirmar ganhos que os resultados não demonstrem.

## Resultados da última execução registrada

Os números a seguir foram lidos das saídas salvas no notebook no momento desta conferência. Eles descrevem essa execução e podem variar entre ambientes ou novas execuções.

### Busca de hiperparâmetros

| Busca | Combinações | Tempo medido | MAPE médio | Melhores parâmetros |
|---|---:|---:|---:|---|
| Grid Search | 12 | 0,495 s | 26,95% | `max_depth=3`, `min_samples_leaf=1` |
| Random Search | 6 | 0,203 s | 27,77% | `max_depth=2`, `min_samples_leaf=1` |

Na execução registrada, o Random Search economizou **0,292 s**, mas apresentou MAPE **0,83 ponto percentual maior** que o Grid Search. Para o Grid Search, o MAPE caiu de **29,82%** na árvore padrão para **26,95%** após a otimização, uma redução calculada de **9,65%** em relação à árvore padrão.

### Comparação final nos mesmos pontos de teste

| Cenário | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Baseline MM7 | 7,37 | 8,11 | 37,47% |
| Modelo ML inicial | 5,23 | 6,94 | 28,91% |
| Modelo ML tunado | 5,02 | 6,74 | 26,88% |

Na saída registrada, o modelo tunado reduziu o erro em relação ao MM7 em **31,81% no MAE**, **16,79% no RMSE** e **28,26% no MAPE**. Esses percentuais são calculados pela própria célula final, usando as métricas dos mesmos períodos de teste.

## Validação e observações importantes

- A última conferência do notebook indicava as células executadas com sucesso, incluindo as células finais de Grid Search, Random Search e comparação.
- O MAPE desconsidera observações em que o valor real é zero, pois a divisão percentual não é definida para esses casos. O mesmo critério é usado durante as buscas e na comparação final.
- Os tempos de busca dependem do computador e da carga do ambiente; compare os resultados que o notebook imprimir ao ser executado.
- A árvore inicial é criada com os parâmetros padrão e sem `random_state`; por isso, resultados exatos dessa árvore podem variar entre execuções. As duas buscas usam `random_state=42` para tornar a comparação entre elas reproduzível.
- A presença do PDF de instruções e do PDF da OAT 1 no repositório não comprova a existência da apresentação da OAT 3. O enunciado solicita uma apresentação versionada com o padrão `mecaniQA_oat3_<nome_da_equipe>.pdf` e também a submissão pelo formulário do Blackboard; essas entregas precisam ser verificadas separadamente.
- O enunciado também determina que a versão avaliada esteja na branch `main`. Como o notebook e o README têm alterações locais pendentes no momento desta documentação, ainda é necessário confirmar que a versão final foi commitada e publicada na branch exigida.
