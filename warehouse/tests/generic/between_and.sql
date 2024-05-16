{% test between_and(model, column_name, left_bound, right_bound) %}

select *
from {{ model }}
where {{ column_name}} not between {{ left_bound }} and {{ right_bound }}

{% endtest %}