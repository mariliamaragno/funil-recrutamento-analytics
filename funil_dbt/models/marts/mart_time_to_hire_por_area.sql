with dados_funil as (
    select * from {{ ref('int_funil_pivot') }}
    where foi_contratado = true
)

select
    area,
    count(*) as total_contratados,
    round(avg(time_to_hire_dias), 1) as time_to_hire_medio_dias,
    min(time_to_hire_dias) as time_to_hire_min_dias,
    max(time_to_hire_dias) as time_to_hire_max_dias
from dados_funil
group by area
order by time_to_hire_medio_dias desc
