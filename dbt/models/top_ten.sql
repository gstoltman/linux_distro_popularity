select 
*
FROM {{ source('staging','rank_by_year') }}