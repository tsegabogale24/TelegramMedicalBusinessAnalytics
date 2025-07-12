-- Custom test to check for future messages
select *
from {{ ref('fct_messages') }}
where message_date > current_timestamp
