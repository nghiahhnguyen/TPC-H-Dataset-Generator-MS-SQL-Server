-- $ID$
-- TPC-H/TPC-R Discounted Revenue Query (Q19)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	sum(l_extendedprice* (1 - l_discount)) as revenue
from
	lineitem,
	part
where
	p_partkey = l_partkey
	and p_brand = ':1'
	and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
	and l_quantity >= :4 and l_quantity <= :4 + 10
	and p_size between 1 and 5
	and l_shipmode in ('AIR', 'AIR REG')
	and l_shipinstruct = 'DELIVER IN PERSON';
