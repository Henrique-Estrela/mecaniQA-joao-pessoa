# MecaniQA Automotive Tech

## Equipe: João Pessoa

Este repositório apresenta a análise do histórico de manutenção da oficina, com foco em trocas de óleo e manutenções do motor, incluindo a preparação dos dados, a validação temporal dos modelos de referência e a criação de atributos temporais para etapas futuras de modelagem.

## Integrantes

* Arthur de Aquino Anjos
* Henrique Estrela Santos
* Luan Vinicius Miranda da Silva
* Matheus Kaick Rocha da Fonseca
* Rafael Pinto Germano Pereira

## Arquivos do projeto

* [mecaniqa_joao_pessoa.ipynb](mecaniqa_joao_pessoa.ipynb): notebook principal com a análise completa
* [mecaniQA_oat1_joao_pessoa.pdf](mecaniQA_oat1_joao_pessoa.pdf): slide para apresentação
* [mecaniqa_dataset - mecaniqa_dataset.csv.csv](mecaniqa_dataset%20-%20mecaniqa_dataset.csv.csv): base de dados utilizada

## Objetivo

Entender o comportamento dos dados ao longo do tempo, verificar se há irregularidades na base, validar os modelos de referência de forma temporalmente correta e criar atributos que capturem padrões históricos para uso em modelagens futuras.

## Análise inicial

A base contém 731 registros diários, cobrindo o período entre 2024-01-01 e 2025-12-31. A coluna de data foi convertida para o formato de data e usada como referência temporal.

Durante a inspeção, foram encontrados alguns valores faltantes nas colunas de trocas de óleo e manutenção do motor. Também foi possível confirmar a quantidade de registros, o período coberto e o formato geral dos dados.

### Pontos importantes

* O conjunto de dados é diário e segue uma sequência temporal regular.
* Há registros faltantes que precisam ser avaliados com atenção.
* O comportamento das duas séries parece seguir padrões ao longo da semana e do tempo.

## Análise temporal

A parte do notebook dedicada à decomposição mostra como a série se organiza em tendência, padrão recorrente e variações pontuais. Isso ajuda a separar o que parece ser crescimento real da oficina do que parece ser um efeito periódico, como variações de semana para semana.

A análise sugere que a série de trocas de óleo tem uma tendência de crescimento ao longo do período, com variações mais fortes em determinados dias da semana. Esse tipo de comportamento é útil para orientar as etapas seguintes do projeto.

## Engenharia de atributos temporais

Foram criados novos atributos a partir da série de trocas de óleo, com o objetivo de capturar padrões históricos que possam ser usados por modelos supervisionados nas próximas etapas do projeto:

* Lags (defasagens) de 1, 7 e 30 dias, capturando o valor observado em períodos anteriores.
* Janelas rolantes (rolling windows) de 7 e 30 dias, suavizando variações de curto e médio prazo.

Todos os atributos são calculados de forma estritamente causal, usando apenas informações disponíveis até o dia anterior ao período previsto, o que evita o vazamento de dados (data leakage) entre passado e futuro.

## Validação temporal e métricas de erro

A validação foi refatorada para usar TimeSeriesSplit, preservando a ordem cronológica dos dados e evitando vazamento de informação entre passado e futuro. Essa abordagem é mais confiável para séries temporais do que a validação aleatória em K-Fold.

As métricas calculadas para os baselines foram MAE, RMSE e MAPE, com foco em responder ao cliente da oficina: em média, quantos litros de óleo o modelo erra por dia. O RMSE destaca erros grandes, enquanto o MAE mostra o erro médio geral e o MAPE expressa o percentual de erro relativo.

O baseline que se saiu melhor na avaliação temporal foi a Média Móvel de 7 dias (MM7), por apresentar o menor erro em todas as métricas (MAE, RMSE e MAPE) na comparação com os demais modelos de referência.

## Como abrir o notebook

Para visualizar a análise, basta abrir o arquivo [mecaniqa_joao_pessoa.ipynb](mecaniqa_joao_pessoa.ipynb) em uma IDE com suporte a Jupyter ou em um ambiente compatível.