import argparse
import subprocess

from dataset_generation.utils import extract_tables_columns


if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument(
		"-U", "--user", help="db administrator", default="SA")
	arg_parser.add_argument("-P", "--password", help="password")
	arg_parser.add_argument("--server", help="The server to run sqlcmd from", default="localhost")
	arg_parser.add_argument("--schema_path", help="Path to the schema", default="./tpc-h.sql")
	args = arg_parser.parse_args()

	count_db_indexes = 0
	table_column_dict = extract_tables_columns(args.schema_path)
	for table_name, column_list in table_column_dict.items():
		for column_name, _ in column_list:
			command = f'docker exec -it mssql sh -c "/opt/mssql-tools/bin/sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -Q \'CREATE INDEX auto_idx_{count_db_indexes} ON {table_name}({column_name});\'"'
			print(command)
			subprocess.call(command, shell=True)
			count_db_indexes += 1
