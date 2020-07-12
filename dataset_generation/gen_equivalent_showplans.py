import os
import random
import argparse
import subprocess
import random
from pathlib import Path

from utils import extract_tables_columns


def create_filtered_queries(args, input_path):
    table_column_dict = extract_tables_columns(args.schema_path)
    with open(input_path, 'r') as f:
        string = f.read()
        select_from = string.split('where')[0]
        where_clause = 'where'.join(string.split('where')[1:])
        from_clause = select_from.split('from')[0]
        tables = from_clause.split(',')
        for table in tables:
            for column, column_data_type in table_column_dict[table]:
                if column_data_type == "int":
                    extra_filter_1 = f"{column} > {1000}"
                    extra_filter_2 = f"{column} < {10}"
                    filtered_query_1 = f"{select_from} where {extra_filter_1} and {where_clause}"
                    filtered_query_2 = f"{select_from} where {extra_filter_2} and {where_clause}"
                    print(filtered_query_1)
                    print(filtered_query_2)
                    return filtered_query_1, filtered_query_2


def drop_all_indexes(table_column_dict, args):
    count_drop_db_indexes = 0
    for table_name, column_list in table_column_dict.items():
        for _, _ in column_list:
            command = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -Q "DROP INDEX {table_name}.auto_idx_{count_drop_db_indexes};"'
            subprocess.call(command, shell=True)
            count_drop_db_indexes += 1


def generate_showplans(indices, args, split, table_column_dict, directory='.'):
    """Generate showplans from the list of queries"""
    print(f"Current split: {split}")

    count_db_indexes = 0
    # iterate through columns and create index on them
    for table_name, column_list in table_column_dict.items():
        for column_name, _ in column_list:
            command = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -Q "CREATE INDEX auto_idx_{count_db_indexes} ON {table_name}({column_name});"'
            print(command)
            subprocess.call(command, shell=True)
            count_db_indexes += 1
            for template in indices:
                for count in range(args.num_queries):
                    input_directory = f"./generated_queries/{split}/{template}/"
                    input_path = input_directory+f"{str(count)}.sql"
                    directory = f"./generated_equivalent_showplans/{split}/template_{template}/config_{count_db_indexes}/"
                    output_path = directory + str(count)
                    Path(directory).mkdir(parents=True, exist_ok=True)
                    subprocess.call('touch ' + output_path, shell=True)

                    filtered_query_1, filtered_query_2 = create_filtered_queries(args, input_path)
                    query_1_path = "./tmp_filtered_query_1.sql"
                    query_2_path = "./tmp_filtered_query_2.sql"
                    with open(query_1_path, 'w') as f:
                        f.write(filtered_query_1)
                    with open(query_2_path, 'w') as f:
                        f.write(filtered_query_2)
                    shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -i {query_1_path} -o {output_path}_0.txt'
                    print(shell_cmd)
                    subprocess.call(shell_cmd, shell=True)
                    shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -i {query_2_path} -o {output_path}_1.txt'
                    print(shell_cmd)
                    subprocess.call(shell_cmd, shell=True)
    drop_all_indexes(table_column_dict, args)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-u", "--user", help="db administrator", default="SA")
    arg_parser.add_argument("-p", "--password", help="password")
    arg_parser.add_argument("--num_queries",
                            help="Number of queries to generate per template", default=10, type=int)
    arg_parser.add_argument(
        "--server", help="The server to run sqlcmd from", default="localhost")
    arg_parser.add_argument(
        "--test_split", help="The percentage of templates to go into test set", default=0.2, type=float)
    arg_parser.add_argument(
        "--dev_split", help="The percentage of templates to go into dev set", default=0.2, type=float)
    arg_parser.add_argument("--showplan", action="store_true", default=True)
    arg_parser.add_argument(
        "--schema_path", help="Path to the schema", default="../tpc-h.sql")
    args = arg_parser.parse_args()

    table_column_dict = extract_tables_columns(args.schema_path)

    os.chdir('../dbgen')
    print(os.getcwd())
    NUM_TEMPLATES = 22

    indices = list(range(1, NUM_TEMPLATES + 1))  # 22 query templates
    random.seed("167")
    random.shuffle(indices)
    test_split = int(args.test_split * NUM_TEMPLATES)
    dev_split = test_split + int(args.dev_split * NUM_TEMPLATES)
    test_indices = indices[:test_split]
    dev_indices = indices[test_split:dev_split]
    train_indices = indices[dev_split:]

    drop_all_indexes(table_column_dict, args)
    # generate showplans
    # if args.showplan:
        # generate_showplans(train_indices, args, "train", table_column_dict)
        # generate_showplans(dev_indices, args, "dev", table_column_dict)
        # generate_showplans(test_indices, args, "test", table_column_dict)
