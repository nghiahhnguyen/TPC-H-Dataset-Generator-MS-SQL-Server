-- $ID$
-- TPC-H/TPC-R Promotion Effect Query (Q14)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select	*
from
	lineitem,
	part
where
	l_quantity < 1000 and
	l_partkey = p_partkey
	and l_shipdate >= cast(':1' as datetime)
	and l_shipdate < dateadd(mm, 1, cast(':1' as datetime));
