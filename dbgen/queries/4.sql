-- $ID$
-- TPC-H/TPC-R Order Priority Checking Query (Q4)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	o_orderdate >= cast(':1' as datetime)
	and o_orderdate < dateadd(mm, '3', cast(':1' as datetime))
	and exists (
		select
			*
		from
			lineitem
		where
			l_orderkey = o_orderkey
			and l_commitdate < l_receiptdate
	)
group by
	o_orderpriority
order by
	o_orderpriority;
