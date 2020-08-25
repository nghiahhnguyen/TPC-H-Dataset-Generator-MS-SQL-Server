-- $ID$
-- TPC-H/TPC-R Returned Item Reporting Query (Q10)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
top 20
	c_custkey,
	c_name,
	sum(l_extendedprice * (1 - l_discount)) as revenue,
	c_acctbal,
	n_name,
	c_address,
	c_phone,
	c_comment
from
	customer,
	orders,
	lineitem,
	nation
where
	c_acctbal < 1000 and
	c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate >= cast(':1' as datetime)
	and o_orderdate < dateadd(mm, 3, cast(':1' as datetime))
	and l_returnflag = 'R'
	and c_nationkey = n_nationkey
group by
	c_custkey,
	c_name,
	c_acctbal,
	c_phone,
	n_name,
	c_address,
	c_comment
order by
	revenue desc;
go
