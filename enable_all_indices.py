import argparse
import subprocess

from dataset_generation.utils import extract_tables_columns


if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument(
		"-U", "--user", help="db administrator", default="SA")
	arg_parser.add_argument("-P", "--password", help="password")
	arg_parser.add_argument("--server", help="The server to run sqlcmd from", default="localhost")
	arg_parser.add_argument("--schema-path", help="Path to the schema", choices=("./schema/tpch.sql", "./schema/imdbload-postgres.sql"))
	arg_parser.add_argument("--dataset", choices=("tpch", "imdbload"))
	arg_parser.add_argument("--docker", help="Name of the container if you are using docker")
	args = arg_parser.parse_args()

	count_db_indexes = 0
	table_column_dict = extract_tables_columns(args.schema_path, args.dataset)
	for table_name, column_list in table_column_dict.items():
		for column_name, column_data_type in column_list:
			if column_name != "skip" and column_data_type != "text":
				if args.dataset == "imdbload":
					column_name = column_name[column_name.find(".") + 1:]
				if args.docker != None:
					command = f'docker exec -it {args.docker} sh -c "/opt/mssql-tools/bin/sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -Q \'CREATE INDEX auto_idx_{count_db_indexes} ON {table_name}({column_name});\'"'
				else:
					command = f'/opt/mssql-tools/bin/sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -Q \'CREATE INDEX auto_idx_{count_db_indexes} ON {table_name}({column_name})\''
				print(command)
				subprocess.call(command, shell=True)
				count_db_indexes += 1
