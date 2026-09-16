AREAS = ["Engenharia", "Comercial", "Produto", "RH", "Financeiro"]
SENIORIDADES = ["Júnior", "Pleno", "Sênior"]
FONTES = ["LinkedIn", "Indicação", "Site da empresa", "Agência de recrutamento"]

ETAPAS = ["triagem", "entrevista_rh", "entrevista_tecnica", "proposta", "contratacao"]

# Probabilidade de avançar para a próxima etapa, por área.
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

# Dias médios por etapa, agora variando por área — reflete que áreas com
# processos mais rigorosos numa etapa também tendem a demorar mais nela
# (mais rodadas de avaliação, mais pessoas envolvidas na decisão).
DIAS_MEDIOS_POR_ETAPA = {
    "Engenharia":  {"triagem": 3, "entrevista_rh": 4, "entrevista_tecnica": 12, "proposta": 4},
    "Comercial":   {"triagem": 6, "entrevista_rh": 4, "entrevista_tecnica": 5,  "proposta": 3},
    "Produto":     {"triagem": 4, "entrevista_rh": 5, "entrevista_tecnica": 8,  "proposta": 5},
    "RH":          {"triagem": 3, "entrevista_rh": 3, "entrevista_tecnica": 6,  "proposta": 3},
    "Financeiro":  {"triagem": 4, "entrevista_rh": 5, "entrevista_tecnica": 7,  "proposta": 4},
}

CANDIDATOS_POR_MES = 2000

# Peso de cada área na abertura de vagas — reflete que áreas de apoio
# (RH, Financeiro) têm quadro mais enxuto e abrem menos vagas por ano
# que áreas de receita/crescimento (Engenharia, Comercial, Produto).
AREA_WEIGHTS = {
    "Engenharia": 0.32,
    "Comercial": 0.305,
    "Produto": 0.28,
    "Financeiro": 0.055,
    "RH": 0.04,
}
