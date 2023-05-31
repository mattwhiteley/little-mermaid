with final_dash as (
    select *
from
{{ ref('analysis_mart') }}
)

select * from final_dash