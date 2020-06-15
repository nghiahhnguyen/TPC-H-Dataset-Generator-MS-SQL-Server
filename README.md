# TPC-H Dataset Generator

TPC-H Data and Query Generator for Microsoft SQL Server on Linux. This repo was modified from version 2.18 of TPC-H benchmark. The modification is created with the purpose of introducing better support for loading this benchmark in Microsoft SQL on Linux.

## Getting started
- Move to main directory for generation related operations:
 
 ```
 cd dbgen
 ```

- Compile the necessary object and executable files:
 
```
make
```

- Generate the data. Choose the scale factor you want for the data. TPC-H runs are only compliant when run against SF's 
      of 1, 10, 100, 300, 1000, 3000, 10000, 30000, 100000. If you want more option, try to take a look at dbgen/README:

```
dbgen -s <scale>
```

After that, the bulk file will be created under the extension of .tbl.

- Create the schema and load the data into the database. Remember to modify the path of the .tbl files at the end of this sql script before running it. Supply the username and password of your database into \<username\> and \<password\>:

```
sqlcmd -S localhost -U <username> -P <password> -i tpc-h.sql
```

- Create primary keys and foreign keys. If you ran into errors such as not being able create primary key on nullable column, you could try looking inside the script and running the lines involving altering the columns for primary key to NOT NULL:

```
sqlcmd -S localhost -U <username> -P <password> -i fk.sql
```
