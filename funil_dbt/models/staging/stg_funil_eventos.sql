select
    id_candidato,
    etapa,
    data_etapa,
    status,
    motivo_reprovacao
from {{ source('raw', 'raw_funil_eventos') }}
