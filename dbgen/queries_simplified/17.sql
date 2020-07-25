-- $ID$
-- TPC-H/TPC-R Small-Quantity-Order Revenue Query (Q17)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	l_extendedprice
from
	lineitem,
	part
where
	p_partkey = l_partkey
	and p_brand = ':1'
	and p_container = ':2'
	and l_quantity < 1000
