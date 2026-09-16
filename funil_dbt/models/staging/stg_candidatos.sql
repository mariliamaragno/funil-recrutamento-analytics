select
    id_candidato,
    nome,
    email,
    fonte,
    id_vaga,
    area,
    data_candidatura
from {{ source('raw', 'raw_candidatos') }}
