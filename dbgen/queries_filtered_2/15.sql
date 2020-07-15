-- $ID$
-- TPC-H/TPC-R Top Supplier Query (Q15)
-- Functional Query Definition
-- Approved February 1998
:x
set showplan_all on;
go

create view revenue:s (supplier_no, total_revenue) as
	select
		l_suppkey,
		sum(l_extendedprice * (1 - l_discount))
	from
		lineitem
	where
		l_shipdate >= cast(':1' as datetime)
		and l_shipdate < dateadd(mm, 3, cast(':1' as datetime))
	group by
		l_suppkey;
go
:o
select
	s_suppkey,
	s_name,
	s_address,
	s_phone,
	total_revenue
from
	supplier,
	revenue:s
where
	s_acctbal > 1000 and
	s_suppkey = supplier_no
	and total_revenue = (
		select
			max(total_revenue)
		from
			revenue:s
	)
order by
	s_suppkey;

drop view revenue:s;
