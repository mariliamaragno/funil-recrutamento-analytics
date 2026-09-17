import sys
import os
from datetime import datetime
import duckdb

sys.path.insert(0, os.path.expanduser("~/projetos/funil-recrutamento/data_generation"))

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

DB_PATH = os.path.expanduser("~/projetos/funil-recrutamento/data/warehouse.duckdb")
DBT_PROJECT_DIR = os.path.expanduser("~/projetos/funil-recrutamento/funil_dbt")


def _gerar_leva_mes(**context):
    from faker_generator import gerar_leva

    data_execucao = context["logical_date"]
    mes_referencia = datetime(data_execucao.year, data_execucao.month, 1)

    vagas, candidatos, eventos = gerar_leva(mes_referencia)

    con = duckdb.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS raw_vagas AS SELECT * FROM vagas LIMIT 0")
    con.execute("CREATE TABLE IF NOT EXISTS raw_candidatos AS SELECT * FROM candidatos LIMIT 0")
    con.execute("CREATE TABLE IF NOT EXISTS raw_funil_eventos AS SELECT * FROM eventos LIMIT 0")

    con.execute("INSERT INTO raw_vagas SELECT * FROM vagas")
    con.execute("INSERT INTO raw_candidatos SELECT * FROM candidatos")
    con.execute("INSERT INTO raw_funil_eventos SELECT * FROM eventos")

    print(f"Leva de {mes_referencia.strftime('%Y-%m')} carregada: "
          f"{len(vagas)} vagas, {len(candidatos)} candidatos, {len(eventos)} eventos.")

    con.close()


with DAG(
    dag_id="dag_ingestao_mensal",
    description="Simula a chegada mensal de uma nova leva de candidatos no funil de recrutamento",
    schedule="@monthly",
    start_date=datetime(2025, 1, 1),
    catchup=True,
    tags=["funil-recrutamento", "dbt", "portfolio"],
) as dag:

    gerar_leva_mes = PythonOperator(
        task_id="gerar_leva_mes",
        python_callable=_gerar_leva_mes,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_DIR} && {sys.executable.replace('python3', 'dbt')} run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_DIR} && {sys.executable.replace('python3', 'dbt')} test",
    )

    gerar_leva_mes >> dbt_run >> dbt_test
