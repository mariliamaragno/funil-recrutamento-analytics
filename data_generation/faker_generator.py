import random
from datetime import timedelta
from faker import Faker
import pandas as pd
from config import (
    AREAS, SENIORIDADES, FONTES, ETAPAS, TAXAS_AVANCO,
    MOTIVOS_REPROVACAO, DIAS_MEDIOS_POR_ETAPA, CANDIDATOS_POR_MES, AREA_WEIGHTS
)

fake = Faker("pt_BR")


def gerar_vagas(mes_referencia, n_vagas=8):
    vagas = []
    pesos = [AREA_WEIGHTS[a] for a in AREAS]
    for i in range(n_vagas):
        area = random.choices(AREAS, weights=pesos, k=1)[0]
        vagas.append({
            "id_vaga": f"{mes_referencia.strftime('%Y%m')}-V{i:03d}",
            "titulo": f"{random.choice(SENIORIDADES)} de {area}",
            "area": area,
            "senioridade": random.choice(SENIORIDADES),
            "recrutador_responsavel": fake.name(),
            "data_abertura": mes_referencia,
        })
    return pd.DataFrame(vagas)


def gerar_candidatos(mes_referencia, vagas_df, n_candidatos=CANDIDATOS_POR_MES):
    candidatos = []
    for i in range(n_candidatos):
        vaga = vagas_df.sample(1).iloc[0]
        data_candidatura = mes_referencia + timedelta(days=random.randint(0, 27))
        candidatos.append({
            "id_candidato": f"{mes_referencia.strftime('%Y%m')}-C{i:05d}",
            "nome": fake.name(),
            "email": fake.email(),
            "fonte": random.choice(FONTES),
            "id_vaga": vaga["id_vaga"],
            "area": vaga["area"],
            "data_candidatura": data_candidatura,
        })
    return pd.DataFrame(candidatos)


def gerar_funil_eventos(candidatos_df):
    eventos = []
    for _, candidato in candidatos_df.iterrows():
        area = candidato["area"]
        taxas = TAXAS_AVANCO[area]
        dias_medios = DIAS_MEDIOS_POR_ETAPA[area]
        data_atual = candidato["data_candidatura"]
        etapa_anterior_ok = True

        for etapa in ETAPAS:
            if etapa == "contratacao":
                if etapa_anterior_ok:
                    eventos.append({
                        "id_candidato": candidato["id_candidato"],
                        "etapa": "contratacao",
                        "data_etapa": data_atual,
                        "status": "aprovado",
                        "motivo_reprovacao": None,
                    })
                break

            if not etapa_anterior_ok:
                break

            dias_na_etapa = max(1, int(random.gauss(dias_medios[etapa], 1.5)))
            data_atual = data_atual + timedelta(days=dias_na_etapa)

            avancou = random.random() < taxas[etapa]

            if avancou:
                eventos.append({
                    "id_candidato": candidato["id_candidato"],
                    "etapa": etapa,
                    "data_etapa": data_atual,
                    "status": "aprovado",
                    "motivo_reprovacao": None,
                })
                etapa_anterior_ok = True
            else:
                eventos.append({
                    "id_candidato": candidato["id_candidato"],
                    "etapa": etapa,
                    "data_etapa": data_atual,
                    "status": "reprovado",
                    "motivo_reprovacao": random.choice(MOTIVOS_REPROVACAO[etapa]),
                })
                etapa_anterior_ok = False

    return pd.DataFrame(eventos)


def gerar_leva(mes_referencia):
    """Gera vagas, candidatos e eventos do funil para um mês de referência."""
    vagas_df = gerar_vagas(mes_referencia)
    candidatos_df = gerar_candidatos(mes_referencia, vagas_df)
    eventos_df = gerar_funil_eventos(candidatos_df)
    return vagas_df, candidatos_df, eventos_df
