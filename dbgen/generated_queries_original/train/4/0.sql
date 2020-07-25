-- using 100 as a seed to the RNG


set showplan_all on;
go

select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	o_orderdate >= cast('1994-05-01' as datetime)
	and o_orderdate < dateadd(mm, 3, cast('1994-05-01' as datetime))
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
