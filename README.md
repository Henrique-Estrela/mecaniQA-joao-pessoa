# MecaniQA Automotive Tech

## Equipe: João Pessoa

## Contexto

Este repositório será utilizado para o desenvolvimento da atividade **OAT 1 – Compreensão e Baseline**, proposta pelo Programa de Trainee da MecaniQA Automotive Tech.

Nesta atividade, a equipe atuará como o time de Ciência de Dados da MecaniQA, com o objetivo de compreender o histórico de **Trocas de Óleo e Manutenções de Motor**, realizar a preparação e análise dos dados temporais e desenvolver modelos preditivos baseline que servirão como referência para as próximas etapas do projeto.

## Objetivos

* Compreender os dados temporais de manutenção;
* Realizar a limpeza e preparação dos dados;
* Analisar tendência, sazonalidade e ruído;
* Tratar dados ausentes e outliers;
* Desenvolver modelos baseline de previsão;
* Comparar os resultados obtidos.

## Integrantes

* Arthur de Aquino Anjos
* Henrique Estrela Santos
* Luan Vinicius Miranda da Silva
* Matheus Kaick Rocha da Fonseca
* Rafael Pinto Germano Pereira

## Encontro 1: inspeção inicial

### Fatos

* O dataset possui 731 registros diários, de 2024-01-01 a 2025-12-31.
* A coluna `Data` deve ser convertida para `datetime` e definida como índice do DataFrame.
* Os atributos medidos são `Trocas_Oleo` e `Manutencao_Motor`.
* A inspeção inicial encontrou 6 valores ausentes em `Trocas_Oleo` e 3 em `Manutencao_Motor`.
* A rotina executável está em [01_inspecao_inicial.py](01_inspecao_inicial.py).

### Questões para a próxima etapa

* Os valores ausentes representam falhas de registro ou dias sem ocorrência?
* Devemos preencher os ausentes com zero, interpolar ou manter como `NaN`?
* Há registros duplicados ou datas fora da frequência diária esperada?

### Ideias

* Verificar a completude do calendário e a frequência temporal antes de modelar.
* Comparar as duas séries com estatísticas descritivas e gráficos de tendência.
* Definir uma política documentada para valores ausentes e outliers.

### Execução

Na raiz do repositório, com Python e pandas instalados:

```bash
python 01_inspecao_inicial.py
```

## Encontro 2: decomposição da série temporal

### Brainstorm guiado

1. **Aditivo ou multiplicativo?**
   Decisão da equipe: **aditivo** (`Y = T + S + R`).
   O nível das trocas de óleo cresce ao longo de 2024–2025, mas a amplitude das oscilações semanais permanece parecida em termos absolutos (cerca de 15 a 20 trocas entre dias fracos e fins de semana). No modelo multiplicativo os picos deveriam aumentar na mesma proporção da tendência; isso não aparece no histórico. O modelo aditivo também tolera melhor interpolações pontuais e valores próximos de zero.

2. **Janela de tempo (média móvel)?**
   Decisão da equipe: **7 dias**.
   Os dados são diários e o ciclo mais claro é o da semana (terças mais fracas, sexta a domingo mais fortes). Uma média móvel de 7 dias percorre um ciclo semanal completo e anula essa sazonalidade no cálculo da tendência. Janela de 30 dias misturaria o efeito de fim de mês com sobras do ciclo semanal; 12 meses seria adequado só se a série fosse mensal.

### Fatos

* A rotina executável está em [02_decomposicao.py](02_decomposicao.py) e reutiliza o mesmo carregamento temporal do encontro 1.
* A decomposição usa `statsmodels.tsa.seasonal.seasonal_decompose` com `model='additive'` e `period=7`.
* Os 6 valores ausentes de `Trocas_Oleo` (10 a 15 de abril de 2024) são interpolados só para esta etapa, porque o Statsmodels não aceita `NaN` na série.
* Os quatro gráficos empilhados (observada, tendência, sazonalidade e ruído) são salvos em [02_decomposicao_trocas_oleo.png](02_decomposicao_trocas_oleo.png).
* A tendência de `Trocas_Oleo` começa perto de 18, recua no segundo semestre de 2024 e termina perto de 35 no fim de 2025.
* A sazonalidade semanal confirma dias úteis mais fracos (segunda a quinta, cerca de -5 a -7) e sexta a domingo mais fortes (cerca de +8).

### Questões para a próxima etapa

* A tendência crescente é estável o suficiente para um baseline ingênuo, ou ainda há quebras de nível?
* O efeito de fim de mês sobrevive no ruído depois de retirar o ciclo semanal?
* Outliers pontuais (por exemplo, 150 trocas em 15/02/2024) devem ser tratados antes da modelagem?

### Ideias

* Usar a tendência isolada como leitura do crescimento real da oficina, sem o sobe-e-desce da semana.
* Guardar o padrão semanal da componente sazonal como regra operacional (dias fracos vs. dias fortes).
* Tratar o ruído e os outliers antes de avançar para modelos de previsão.

### Execução

Na raiz do repositório, com Python, pandas, matplotlib e statsmodels instalados:

```bash
python 02_decomposicao.py
```

### Versionamento e convite

O repositório deve seguir o padrão `mecaniQA-<nome-do-time>`, neste caso `mecaniQA-joao-pessoa`. Depois de criar o repositório no GitHub, o fluxo inicial é:

```bash
git init
git add README.md 01_inspecao_inicial.py "mecaniqa_dataset - mecaniqa_dataset.csv.csv"
git commit -m "Adiciona rotina de inspeção inicial"
git branch -M main
git remote add origin <URL_DO_REPOSITORIO>
git push -u origin main
```

No GitHub, acesse **Settings > Collaborators** e convide o usuário `lasilva` como colaborador do repositório.
