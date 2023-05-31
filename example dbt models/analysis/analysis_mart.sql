with staging as (
    select *
from
{{ ref('staging_model') }}
),
with int_model as (
    select *
from
{{ ref('int_model') }}
)
select * from final