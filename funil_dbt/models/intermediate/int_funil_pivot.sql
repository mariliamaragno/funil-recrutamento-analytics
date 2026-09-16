with candidatos as (
    select * from {{ ref('stg_candidatos') }}
),

eventos as (
    select * from {{ ref('stg_funil_eventos') }}
),

vagas as (
    select * from {{ ref('stg_vagas') }}
),

eventos_aprovados as (
    select
        id_candidato,
        etapa,
        data_etapa
    from eventos
    where status = 'aprovado'
),

pivot_datas as (
    select
        id_candidato,
        max(case when etapa = 'triagem' then data_etapa end) as data_triagem,
        max(case when etapa = 'entrevista_rh' then data_etapa end) as data_entrevista_rh,
        max(case when etapa = 'entrevista_tecnica' then data_etapa end) as data_entrevista_tecnica,
        max(case when etapa = 'proposta' then data_etapa end) as data_proposta,
        max(case when etapa = 'contratacao' then data_etapa end) as data_contratacao
    from eventos_aprovados
    group by id_candidato
),

ultima_etapa as (
    select
        id_candidato,
        etapa as etapa_final,
        status as status_final,
        motivo_reprovacao as motivo_reprovacao_final,
        data_etapa as data_ultima_etapa,
        row_number() over (partition by id_candidato order by data_etapa desc) as rn
    from eventos
),

final as (
    select
        c.id_candidato,
        c.nome,
        c.fonte,
        c.id_vaga,
        c.area,
        v.senioridade,
        v.recrutador_responsavel,
        c.data_candidatura,
        p.data_triagem,
        p.data_entrevista_rh,
        p.data_entrevista_tecnica,
        p.data_proposta,
        p.data_contratacao,
        u.etapa_final,
        u.status_final,
        u.motivo_reprovacao_final,
        case when p.data_contratacao is not null then true else false end as foi_contratado,
        case
            when p.data_contratacao is not null
            then date_diff('day', c.data_candidatura, p.data_contratacao)
        end as time_to_hire_dias
    from candidatos c
    left join pivot_datas p on c.id_candidato = p.id_candidato
    left join vagas v on c.id_vaga = v.id_vaga
    left join ultima_etapa u on c.id_candidato = u.id_candidato and u.rn = 1
)

select * from final
