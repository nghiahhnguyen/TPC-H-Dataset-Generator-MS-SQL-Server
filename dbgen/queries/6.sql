-- $ID$
-- TPC-H/TPC-R Forecasting Revenue Change Query (Q6)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= cast(':1' as datetime)
	and l_shipdate < dateadd(yy, 1, cast(':1' as datetime))
	and l_discount between :2 - 0.01 and :2 + 0.01
	and l_quantity < :3;
go
