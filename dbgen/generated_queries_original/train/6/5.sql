-- using 600 as a seed to the RNG


set showplan_all on;
go

select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= cast('1994-01-01' as datetime)
	and l_shipdate < dateadd(yy, 1, cast('1994-01-01' as datetime))
	and l_discount between 0.04 - 0.01 and 0.04 + 0.01
	and l_quantity < 25;
go
