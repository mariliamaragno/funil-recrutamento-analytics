AREAS = ["Engenharia", "Comercial", "Produto", "RH", "Financeiro"]
SENIORIDADES = ["Júnior", "Pleno", "Sênior"]
FONTES = ["LinkedIn", "Indicação", "Site da empresa", "Agência de recrutamento"]

ETAPAS = ["triagem", "entrevista_rh", "entrevista_tecnica", "proposta", "contratacao"]

# Probabilidade de avançar para a próxima etapa, por área.
# Cada área tem um "gargalo" diferente, para o dashboard revelar padrões reais.
TAXAS_AVANCO = {
    "Engenharia":  {"triagem": 0.55, "entrevista_rh": 0.70, "entrevista_tecnica": 0.40, "proposta": 0.75},
    "Comercial":   {"triagem": 0.35, "entrevista_rh": 0.65, "entrevista_tecnica": 0.70, "proposta": 0.80},
    "Produto":     {"triagem": 0.50, "entrevista_rh": 0.60, "entrevista_tecnica": 0.55, "proposta": 0.70},
    "RH":          {"triagem": 0.60, "entrevista_rh": 0.75, "entrevista_tecnica": 0.65, "proposta": 0.85},
    "Financeiro":  {"triagem": 0.45, "entrevista_rh": 0.70, "entrevista_tecnica": 0.60, "proposta": 0.78},
}

MOTIVOS_REPROVACAO = {
    "triagem": ["Perfil não aderente", "Pretensão salarial incompatível", "Sem experiência mínima"],
    "entrevista_rh": ["Fit cultural", "Disponibilidade/localização", "Comunicação"],
    "entrevista_tecnica": ["Conhecimento técnico insuficiente", "Case não resolvido", "Soft skills técnicas"],
    "proposta": ["Contraproposta aceita", "Desistência do candidato", "Oferta recusada"],
}

# Dias médios que um candidato leva em cada etapa antes de avançar (ou ser reprovado)
DIAS_MEDIOS_POR_ETAPA = {
    "triagem": 3,
    "entrevista_rh": 5,
    "entrevista_tecnica": 7,
    "proposta": 4,
}

CANDIDATOS_POR_MES = 2000
