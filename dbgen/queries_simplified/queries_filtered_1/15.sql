-- $ID$
-- TPC-H/TPC-R Top Supplier Query (Q15)
-- Functional Query Definition
-- Approved February 1998
:x
set showplan_all on;
go

select
	l_suppkey,
	sum(l_extendedprice * (1 - l_discount))
from
	lineitem
where
	l_quantity < 1000 and
	l_shipdate >= cast(':1' as datetime)
	and l_shipdate < dateadd(mm, 3, cast(':1' as datetime))
group by
	l_suppkey;
go
