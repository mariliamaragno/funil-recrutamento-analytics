select
    id_vaga,
    titulo,
    area,
    senioridade,
    recrutador_responsavel,
    data_abertura
from {{ source('raw', 'raw_vagas') }}
