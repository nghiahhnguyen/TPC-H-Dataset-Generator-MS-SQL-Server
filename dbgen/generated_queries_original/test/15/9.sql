-- using 1000 as a seed to the RNG

set showplan_all on;
go

create view revenue0 (supplier_no, total_revenue) as
	select
		l_suppkey,
		sum(l_extendedprice * (1 - l_discount))
	from
		lineitem
	where
		l_shipdate >= cast('1996-05-01' as datetime)
		and l_shipdate < dateadd(mm, 3, cast('1996-05-01' as datetime))
	group by
		l_suppkey;
go

select
	s_suppkey,
	s_name,
	s_address,
	s_phone,
	total_revenue
from
	supplier,
	revenue0
where
	s_suppkey = supplier_no
	and total_revenue = (
		select
			max(total_revenue)
		from
			revenue0
	)
order by
	s_suppkey;

drop view revenue0;
