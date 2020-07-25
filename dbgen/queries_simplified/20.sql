-- $ID$
-- TPC-H/TPC-R Potential Part Promotion Query (Q20)
-- Function Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	s_name,
	s_address
from
	supplier,
	nation
where
	s_nationkey = n_nationkey
	and n_name = ':3'
order by
	s_name;
