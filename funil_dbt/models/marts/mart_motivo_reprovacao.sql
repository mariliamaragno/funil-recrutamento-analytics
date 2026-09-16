with eventos as (
    select * from {{ ref('stg_funil_eventos') }}
    where status = 'reprovado'
)

select
    etapa,
    motivo_reprovacao,
    count(*) as total_ocorrencias
from eventos
group by etapa, motivo_reprovacao
order by etapa, total_ocorrencias desc
