use tpch;
go

declare @qry nvarchar(max);
select @qry = 
(SELECT  'DROP INDEX [' + ix.name + '] ON ' + OBJECT_NAME(ID) + '; '
FROM  sysindexes ix
WHERE   ix.Name IS NOT null and ix.Name like '%prefix_%'
for xml path(''));
exec sp_executesql @qry