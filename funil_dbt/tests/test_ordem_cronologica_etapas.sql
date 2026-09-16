-- Este teste falha se encontrar qualquer linha onde uma etapa posterior
-- tenha data anterior a uma etapa que deveria vir antes dela.
select *
from {{ ref('int_funil_pivot') }}
where
    (data_entrevista_rh is not null and data_triagem is not null and data_entrevista_rh < data_triagem)
    or (data_entrevista_tecnica is not null and data_entrevista_rh is not null and data_entrevista_tecnica < data_entrevista_rh)
    or (data_proposta is not null and data_entrevista_tecnica is not null and data_proposta < data_entrevista_tecnica)
    or (data_contratacao is not null and data_proposta is not null and data_contratacao < data_proposta)
