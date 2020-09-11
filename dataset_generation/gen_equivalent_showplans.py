import os
import random
import argparse
import subprocess
import random
import glob
from pathlib import Path

from .utils import extract_tables_columns

def drop_all_indexes(table_column_dict, args):
    count_drop_db_indexes = 0
    for table_name, column_list in table_column_dict.items():
        for _, _ in column_list:
            command = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -Q "DROP INDEX {table_name}.auto_idx_{count_drop_db_indexes}"'
            subprocess.call(command, shell=True)
            count_drop_db_indexes += 1


def run_shell_cmd(args, input_path, output_path, filter_idx):
    shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -i {input_path}_{filter_idx}.sql -o {output_path}_{filter_idx}.txt'
    print(shell_cmd)
    subprocess.call(shell_cmd, shell=True)

def generate_showplans(indices, args, split, table_column_dict, count_db_indexes, directory='.'):
    """Generate showplans from the list of queries"""
    print(f"Current split: {split}")

    if args.dataset == "tpch":
        for template in indices:
            input_directory = f"{args.input_directory}/generated_queries/{split}/{template}/"
            for count in range(args.num_queries):
                input_path = input_directory+f"{str(count)}"
                directory = f"../dataset_generation/generated_equivalent_showplans/{split}/template_{template}/config_{count_db_indexes}/"
                output_path = directory + str(count)
                Path(directory).mkdir(parents=True, exist_ok=True)
                for i in range(3):
                    run_shell_cmd(args, input_path, output_path, i)
    elif args.dataset == "imdbload":
        for template in indices:
            template += 1
            for file_path in glob.glob(f"{args.input_directory}/{template}[a-z]*.sql"):
                directory = f"../dataset_generation/generated_equivalent_showplans_imdbload/{split}/template_{template}/config_{count_db_indexes}/"

                # extract basename of the file
                file_name = file_path[file_path.rfind("/")+1:]
                # remove the extension
                file_name = file_name[:-4]

                output_path = directory + file_name
                Path(directory).mkdir(parents=True, exist_ok=True)
                shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -i {file_path} -o {output_path}.txt'
                print(shell_cmd)
                subprocess.call(shell_cmd, shell=True)

    else:
        raise NotImplementedError


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-U", "--user", help="db administrator", default="SA")
    arg_parser.add_argument("-P", "--password", help="password")
    arg_parser.add_argument("--num_queries",
                            help="Number of queries to generate per template", default=10, type=int)
    arg_parser.add_argument(
        "--server", help="The server to run sqlcmd from", default="localhost")
    arg_parser.add_argument(
        "--test-split", help="The percentage of templates to go into test set", default=0.2, type=float)
    arg_parser.add_argument(
        "--dev-split", help="The percentage of templates to go into dev set", default=0.2, type=float)
    arg_parser.add_argument("--showplan", action="store_true", default=True)
    arg_parser.add_argument(
        "--schema-path", help="Path to the schema", default="../tpc-h.sql")
    arg_parser.add_argument("--dataset", default="tpch", help="The dataset to choose", choices=["tpch", "imdbload"])
    arg_parser.add_argument("--input-directory", default=".", help="Path to the where the queries is")
    args = arg_parser.parse_args()

    table_column_dict = extract_tables_columns(args.schema_path, args.dataset)

    os.chdir('../dbgen')
    print(os.getcwd())
    NUM_TEMPLATES = 13

#     indices = list(range(1, NUM_TEMPLATES + 1))  # 22 query templates
    indices = [1, 2, 3, 4, 5, 6, 7, 10, 12, 14, 15, 18, 19]
    random.seed("167")
    random.shuffle(indices)
    test_split = int(args.test_split * NUM_TEMPLATES)
    dev_split = test_split + int(args.dev_split * NUM_TEMPLATES)
    test_indices = indices[:test_split]
    dev_indices = indices[test_split:dev_split]
    train_indices = indices[dev_split:]

    # generate showplans
    count_db_indexes = 0
    # drop all indexes
    drop_all_indexes(table_column_dict, args)
    # iterate through columns and create index on them
    for table_name, column_list in table_column_dict.items():
        for column_name, column_data_type in column_list:
            if column_name == "skip" or column_data_type == "text":
                continue
            command = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -Q "create index auto_idx_{count_db_indexes} on {table_name}({column_name});"'
            print(command)
            subprocess.call(command, shell=True)
            if args.showplan:
                generate_showplans(train_indices, args,
                                   "train", table_column_dict, count_db_indexes)
                generate_showplans(dev_indices, args, "dev",
                                   table_column_dict, count_db_indexes)
                generate_showplans(test_indices, args,
                                   "test", table_column_dict, count_db_indexes)
            count_db_indexes += 1
