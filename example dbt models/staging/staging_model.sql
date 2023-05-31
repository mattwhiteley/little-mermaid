with final as (
    select *
from
{{ source('ops_tool', 'user_table') }}
)

select * from final