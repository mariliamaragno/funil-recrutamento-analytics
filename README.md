# Funil de Recrutamento — Pipeline de Dados Sintéticos

Projeto de portfólio simulando um pipeline completo de recrutamento e seleção, do candidato à contratação, usando dados sintéticos gerados com Faker.

**[🔗 Acesse o dashboard ao vivo](https://funil-recrutamento-analytics-4ygfhu5a9pns3l5zl4be3t.streamlit.app/)**

## Objetivo

Simular um funil de recrutamento real (triagem → entrevista RH → entrevista técnica → proposta → contratação) para construir métricas de conversão, time-to-hire e identificação de gargalos por etapa e por área — mostrando, na prática, a diferença entre um gargalo de **volume** (onde mais gente é reprovada) e um gargalo de **velocidade** (onde o processo demora mais, mesmo aprovando).

## Stack

- **Faker** — geração de dados sintéticos (candidatos, vagas, eventos de funil)
- **DuckDB** — banco de dados analítico embarcado
- **dbt (dbt-duckdb)** — transformação e modelagem em camadas
- **Airflow** — orquestração simulando ingestão mensal (backfill de 12 meses)
- **Streamlit + Plotly** — dashboard interativo, publicado no Streamlit Community Cloud

## Nota sobre os dados

Todos os dados são 100% sintéticos, gerados via Faker — nenhuma informação real de candidatos ou empresas está presente neste projeto. As taxas de conversão e os tempos médios por etapa foram propositalmente desenhados de forma desigual entre áreas, para simular gargalos realistas que a análise pudesse "descobrir".

## Arquitetura

- **data_generation** — gerador Python (Faker) com uma função `gerar_leva(mes)`, chamada mês a mês pela DAG do Airflow, simulando a chegada real de uma nova leva de candidatos
- **staging** — limpeza e padronização das três tabelas brutas (vagas, candidatos, eventos de funil)
- **intermediate** — `int_funil_pivot`: pivota os eventos em uma linha por candidato, com a data de cada etapa em colunas, calculando `time_to_hire_dias` e a flag `foi_contratado`
- **marts** — métricas finais: conversão por etapa, time-to-hire por área, motivo de reprovação mais comum por etapa

## Qualidade de dados

11 testes automatizados no dbt cobrindo:
- Valores nulos e unicidade em colunas críticas (`not_null`, `unique`)
- Valores aceitos dentro de listas válidas (`accepted_values`)
- Um teste customizado garantindo a **ordem cronológica das etapas** — nenhum candidato pode ter, por exemplo, uma data de contratação anterior à da proposta

## Metodologia da orquestração

A DAG `dag_ingestao_mensal` simula, para cada um dos 12 meses de 2025, a chegada de uma nova leva de ~2.000 candidatos, seguida de `dbt run` e `dbt test` — reproduzindo o ciclo real de ingestão → transformação → validação que rodaria em produção. Devido a uma limitação de concorrência do SQLite (banco de metadados padrão do Airflow em ambiente local), as 12 execuções foram processadas via `airflow dags test`, que roda cada execução de forma síncrona e isolada — evitando o problema sem alterar a lógica da DAG.

## Principais achados

**1. O maior gargalo de volume está na triagem**
Apenas 48,5% dos candidatos avançam da triagem — a etapa mais restritiva do funil, sozinha, é responsável pela maior perda de candidatos (11.332 de 22.000).

**2. A entrevista técnica é o segundo maior gargalo de conversão**
51,9% de aprovação — bem abaixo da entrevista de RH (66,3%) e da proposta (75,9%), confirmando que a etapa técnica concentra o segundo maior volume de reprovações do funil.

**3. Gargalo de volume e gargalo de velocidade são fenômenos distintos**
Engenharia tem o maior time-to-hire médio (21,2 dias), mas não é a área com pior taxa de conversão — o problema ali é a duração da etapa técnica, não o volume de reprovação. Já a triagem (gargalo de volume) afeta o funil inteiro de forma mais homogênea. Um mesmo sintoma ("processo lento") pode ter causas raiz completamente diferentes, exigindo ações diferentes.

**4. Áreas de apoio (RH, Financeiro) têm volume de contratação proporcionalmente menor**
RH (214 contratados) e Financeiro (70) representam uma fração pequena frente a Engenharia (1.058) e Produto (689) — reflexo de quadros mais enxutos nessas áreas, e não de um processo seletivo pior.

**5. RH tem o processo mais ágil de todas as áreas**
13,3 dias médios de time-to-hire — quase 8 dias mais rápido que Engenharia — sugerindo um processo mais simples ou vagas com perfil menos competitivo/específico.

## Dashboard

O dashboard interativo (Streamlit + Plotly) permite filtrar por área e visualizar:
- KPIs gerais (total de candidatos, contratados, taxa de conversão, time-to-hire médio)
- Funil de conversão visual, etapa a etapa
- Gráfico de gargalos, com escala de cor vermelho-verde para identificação rápida
- Comparação de time-to-hire e volume de contratação entre áreas
- Distribuição de motivos de reprovação por etapa

## Como rodar localmente

```bash
python3 -m venv venv && source venv/bin/activate
pip install faker duckdb dbt-duckdb pandas streamlit plotly apache-airflow

# 1. Gerar dados sintéticos
cd data_generation
python3 gerar_historico.py

# 2. Rodar o dbt
cd ../funil_dbt
dbt deps
dbt run
dbt test

# 3. Rodar o dashboard
cd ../dashboard
streamlit run app.py
```

## Roadmap

- [x] Gerador de dados sintéticos (Faker) — vagas, candidatos, eventos de funil, com taxas e tempos variando por área
- [x] Carga em DuckDB
- [x] Modelagem em camadas via dbt (staging → intermediate → marts)
- [x] Testes de qualidade de dados (11 testes, incluindo consistência cronológica)
- [x] Orquestração via Airflow (simulando ingestão mensal, backfill de 12 meses)
- [x] Dashboard interativo (Streamlit + Plotly), publicado no Streamlit Community Cloud

---

Projeto desenvolvido por [Marília Maragno](https://www.linkedin.com/in/mariliamaragno/) como parte de estudo aplicado em engenharia e análise de dados.
