with eventos as (
    select * from {{ ref('stg_funil_eventos') }}
),

por_etapa as (
    select
        etapa,
        count(*) as total_candidatos,
        sum(case when status = 'aprovado' then 1 else 0 end) as total_aprovados,
        sum(case when status = 'reprovado' then 1 else 0 end) as total_reprovados
    from eventos
    group by etapa
)

select
    etapa,
    total_candidatos,
    total_aprovados,
    total_reprovados,
    round(100.0 * total_aprovados / total_candidatos, 1) as taxa_conversao_pct
from por_etapa
order by
    case etapa
        when 'triagem' then 1
        when 'entrevista_rh' then 2
        when 'entrevista_tecnica' then 3
        when 'proposta' then 4
        when 'contratacao' then 5
    end
