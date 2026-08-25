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
