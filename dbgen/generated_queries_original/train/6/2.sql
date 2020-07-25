-- using 300 as a seed to the RNG


set showplan_all on;
go

select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= cast('1993-01-01' as datetime)
	and l_shipdate < dateadd(yy, 1, cast('1993-01-01' as datetime))
	and l_discount between 0.07 - 0.01 and 0.07 + 0.01
	and l_quantity < 25;
go
