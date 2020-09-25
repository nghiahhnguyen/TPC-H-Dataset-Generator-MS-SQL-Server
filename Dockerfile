FROM mcr.microsoft.com/mssql/server:2019-CU5-ubuntu-18.04
MAINTAINER huunghia
RUN mkdir -p /opt/tpch/
COPY dbgen/. /opt/tpch
ENV MSSQL_SA_PASSWORD='P#ssw0rd'
WORKDIR /opt/tpch/
RUN ( /opt/mssql/bin/sqlservr --accept-eula & ) | grep -q "Service Broker manager has started" \
&& /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'P#ssw0rd' -i /opt/tpch/dbgen/tpch-h.sql\
&& /opt/mssql
