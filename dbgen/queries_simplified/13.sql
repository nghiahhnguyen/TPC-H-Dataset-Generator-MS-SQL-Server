-- $ID$
-- TPC-H/TPC-R Customer Distribution Query (Q13)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	c_count,
	c_custkey,
	count(o_orderkey)
from
	customer, orders 
where
	c_custkey = o_custkey
	and o_comment not like '%:1%:2%'
group by
	c_custkey, c_count
