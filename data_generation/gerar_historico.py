from datetime import datetime
import duckdb
from faker_generator import gerar_leva

DB_PATH = "../data/warehouse.duckdb"

def gerar_e_carregar_historico(ano=2025):
    con = duckdb.connect(DB_PATH)

    todas_vagas = []
    todos_candidatos = []
    todos_eventos = []

    for mes in range(1, 13):
        mes_referencia = datetime(ano, mes, 1)
        print(f"Gerando leva de {mes_referencia.strftime('%Y-%m')}...")
        vagas, candidatos, eventos = gerar_leva(mes_referencia)
        todas_vagas.append(vagas)
        todos_candidatos.append(candidatos)
        todos_eventos.append(eventos)

    import pandas as pd
    vagas_final = pd.concat(todas_vagas, ignore_index=True)
    candidatos_final = pd.concat(todos_candidatos, ignore_index=True)
    eventos_final = pd.concat(todos_eventos, ignore_index=True)

    con.execute("CREATE OR REPLACE TABLE raw_vagas AS SELECT * FROM vagas_final")
    con.execute("CREATE OR REPLACE TABLE raw_candidatos AS SELECT * FROM candidatos_final")
    con.execute("CREATE OR REPLACE TABLE raw_funil_eventos AS SELECT * FROM eventos_final")

    print()
    print(f"Total de vagas: {len(vagas_final)}")
    print(f"Total de candidatos: {len(candidatos_final)}")
    print(f"Total de eventos: {len(eventos_final)}")

    con.close()

if __name__ == "__main__":
    gerar_e_carregar_historico()
