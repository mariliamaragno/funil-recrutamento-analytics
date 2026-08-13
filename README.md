# Funil de Recrutamento — Pipeline de Dados Sintéticos

Projeto de portfólio simulando um pipeline completo de recrutamento e seleção, do candidato à contratação, usando dados sintéticos gerados com Faker.

## Objetivo

Simular um funil de recrutamento real (triagem → entrevista RH → entrevista técnica → proposta → contratação) para construir métricas de conversão, time-to-hire e identificação de gargalos por etapa e por área.

## Stack

- **Faker** — geração de dados sintéticos (candidatos, vagas, eventos de funil)
- **DuckDB** — banco de dados analítico embarcado
- **dbt (dbt-duckdb)** — transformação e modelagem em camadas
- *(em construção)* **Airflow** — orquestração simulando ingestão mensal
- *(em construção)* **Streamlit + Plotly** — dashboard interativo

## Nota sobre os dados

Todos os dados são 100% sintéticos, gerados via Faker — nenhuma informação real de candidatos ou empresas está presente neste projeto.

## Como rodar localmente

\`\`\`bash
python3 -m venv venv && source venv/bin/activate
pip install faker duckdb dbt-duckdb pandas streamlit plotly apache-airflow

cd data_generation
python3 gerar_historico.py

cd ../funil_dbt
dbt deps
dbt run
dbt test
\`\`\`

## Roadmap

- [x] Gerador de dados sintéticos (Faker) — vagas, candidatos, eventos de funil
- [x] Carga em DuckDB
- [ ] Modelagem em camadas via dbt
- [ ] Orquestração via Airflow (simulando ingestão mensal)
- [ ] Dashboard interativo (Streamlit + Plotly)
