-- using 700 as a seed to the RNG


set showplan_all on;
go

select
	n_name,
	sum(l_extendedprice * (1 - l_discount)) as revenue
from
	customer,
	orders,
	lineitem,
	supplier,
	nation,
	region
where
	c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and l_suppkey = s_suppkey
	and c_nationkey = s_nationkey
	and s_nationkey = n_nationkey
	and n_regionkey = r_regionkey
	and r_name = 'AMERICA'
	and o_orderdate >= cast('1997-01-01' as datetime)
	and o_orderdate < dateadd(yy, 1, cast('1997-01-01' as datetime))
group by
	n_name
order by
	revenue desc;
go
