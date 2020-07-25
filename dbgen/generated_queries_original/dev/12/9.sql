-- using 1000 as a seed to the RNG



set showplan_all on;
go

select
	l_shipmode,
	sum(case
		when o_orderpriority = '1-URGENT'
			or o_orderpriority = '2-HIGH'
			then 1
		else 0
	end) as high_line_count,
	sum(case
		when o_orderpriority <> '1-URGENT'
			and o_orderpriority <> '2-HIGH'
			then 1
		else 0
	end) as low_line_count
from
	orders,
	lineitem
where
	o_orderkey = l_orderkey
	and l_shipmode in ('SHIP', 'MAIL')
	and l_commitdate < l_receiptdate
	and l_shipdate < l_commitdate
	and l_receiptdate >= cast('1995-01-01' as datetime)
	and l_receiptdate < dateadd(mm, 1, cast('1995-01-01' as datetime))
group by
	l_shipmode
order by
	l_shipmode;
