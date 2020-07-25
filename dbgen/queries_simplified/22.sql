-- $ID$
-- TPC-H/TPC-R Global Sales Opportunity Query (Q22)
-- Functional Query Definition
-- Approved February 1998
:x
:o
set showplan_all on;
go

select
	substring(c_phone, 1, 2) as cntrycode,
	c_acctbal
from
	customer
where
	substring(c_phone, 1, 2) in
		(':1', ':2', ':3', ':4', ':5', ':6', ':7')
group by
	cntrycode
order by
	cntrycode;
