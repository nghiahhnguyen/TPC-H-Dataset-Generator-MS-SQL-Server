-- using 100 as a seed to the RNG


set showplan_all on;
go

select
	100.00 * sum(case
		when p_type like 'PROMO%'
			then l_extendedprice * (1 - l_discount)
		else 0
	end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from
	lineitem,
	part
where
	l_partkey = p_partkey
	and l_shipdate >= cast('1994-09-01' as datetime)
	and l_shipdate < dateadd(mm, 1, cast('1994-09-01' as datetime));
