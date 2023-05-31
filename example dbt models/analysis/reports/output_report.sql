with final as (
    select *
from
{{ ref('analysis_mart') }}
)

select * from final