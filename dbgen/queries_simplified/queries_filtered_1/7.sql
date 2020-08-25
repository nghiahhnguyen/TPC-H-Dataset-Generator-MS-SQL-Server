-- $ID$
-- TPC-H/TPC-R Volume Shipping Query (Q7)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	n1.n_name as supp_nation,
	n2.n_name as cust_nation,
	datepart(yy, l_shipdate) as l_year,
	l_extendedprice * (1 - l_discount) as volume
from
	supplier,
	lineitem,
	orders,
	customer,
	nation n1,
	nation n2
where
	s_acctbal < 1000 and
	s_suppkey = l_suppkey
	and o_orderkey = l_orderkey
	and c_custkey = o_custkey
	and s_nationkey = n1.n_nationkey
	and c_nationkey = n2.n_nationkey
	and l_shipdate between cast('1995-01-01' as datetime) and cast('1996-12-31' as datetime);
go
