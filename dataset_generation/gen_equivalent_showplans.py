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
        for column_name, column_data_type in column_list:
            if column_name == "skip" or column_data_type == "text":
                continue
            command = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -Q "DROP INDEX {table_name}.auto_idx_{count_drop_db_indexes}"'
            subprocess.call(command, shell=True)
            count_drop_db_indexes += 1

def add_statistics(input_path):
    extra_statistics_query = "SET SHOWPLAN_ALL ON\nGO\n\n"
    # add extra statistics
    with open(input_path, "r") as f:
        string = f.read()
    original_string = string
    string = extra_statistics_query + string
    with open(input_path, "w") as f:
        f.write(string)
    return original_string

def restore_statistics(input_path, original_string):
    with open(input_path, "w") as f:
        f.write(original_string)

def run_shell_cmd(args, input_path, output_path, output_directory, column_name, filter_idx=None):
    extra_filter_file_name = ""
    if filter_idx != None:
        extra_filter_file_name = f"_{filter_idx}"
    
    full_input_path = f"{input_path}{extra_filter_file_name}.sql"

    if args.reduce_configs:
        with open(full_input_path, "r") as f:
            string = f.read()
            if column_name not in string:
                return

    Path(output_directory).mkdir(parents=True, exist_ok=True)
    original_string = add_statistics(full_input_path)
    shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -i {full_input_path} -o {output_path}{extra_filter_file_name}.txt'
    print(shell_cmd)
    subprocess.call(shell_cmd, shell=True)
    restore_statistics(full_input_path, original_string)

def generate_showplans(indices, args, split, table_column_dict, count_db_indexes, column_name, directory='.'):
    """Generate showplans from the list of queries"""
    print(f"Current split: {split}")

    if args.dataset in ("tpch", "tpcds"):
        for template in indices:
            if args.dataset == "tpch":
                input_directory = f"{args.input_directory}/generated_queries/{split}/{template}"
            else:
                input_directory = f"{args.input_directory}/{split}/{template}"
            for count in range(args.num_queries):
                input_path = f"{input_directory}/{str(count)}"

                directory = f"{os.path.dirname(__file__)}/generated_equivalent_showplans_{args.dataset}/{split}/template_{template}/config_{count_db_indexes}/"
                output_path = directory + str(count)

                if args.dataset == "tpch":
                    for i in range(3):
                        run_shell_cmd(args, input_path, output_path, directory, column_name, i)
                else:
                    run_shell_cmd(args, input_path, output_path, directory, column_name)

                
    elif args.dataset == "imdbload":
        for template in indices:
            for input_path in glob.glob(f"{args.input_directory}/{template}[a-z]*.sql"):
                directory = f"{os.path.dirname(__file__)}/generated_equivalent_showplans_imdbload/{split}/template_{template}/config_{count_db_indexes}/"

                original_string = add_statistics(input_path)

                # extract basename of the file
                file_name = input_path[input_path.rfind("/")+1:]
                # remove the extension
                file_name = file_name[:-4]

                output_path = directory + file_name
                Path(directory).mkdir(parents=True, exist_ok=True)
                shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d {args.dataset} -i {input_path} -o {output_path}.txt'
                # print(shell_cmd)
                subprocess.call(shell_cmd, shell=True)

                restore_statistics(input_path, original_string)

    else:
        raise NotImplementedError


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-U", "--user", help="db administrator", default="SA")
    arg_parser.add_argument("-P", "--password", help="password")
    arg_parser.add_argument("--num-queries",
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
    arg_parser.add_argument("--dataset", default="tpch", help="The dataset to choose", choices=["tpch", "imdbload", "tpcds"])
    arg_parser.add_argument("--input-directory", default=".", help="Path to the where the queries is")
    arg_parser.add_argument("--num-templates", help="Number of templates", type=int)
    arg_parser.add_argument("--reduce-configs", help="Whether to only generate necessary configurations for each query", action="store_true")
    args = arg_parser.parse_args()

    table_column_dict = extract_tables_columns(args.schema_path, args.dataset)

    if args.dataset == "tpch":
        os.chdir('../dbgen')
    print(os.getcwd())

    if args.dataset == "tpch":
        # indices for simplified tpch
        indices = [1, 2, 3, 4, 5, 6, 7, 10, 12, 14, 15, 18, 19]
    elif args.dataset == "tpcds":
        indices = [1, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    elif args.dataset == "imdbload":
        # indices for imdbload
        indices = [i + 1 for i in range(33)]
    

    random.seed("167")
    random.shuffle(indices)
    if args.num_templates == None:
        args.num_templates = len(indices)
    test_split = int(args.test_split * args.num_templates)
    dev_split = test_split + int(args.dev_split * args.num_templates)
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
                generate_showplans(train_indices, args, "train", table_column_dict, count_db_indexes, column_name)
                generate_showplans(dev_indices, args, "dev",table_column_dict, count_db_indexes, column_name)
                generate_showplans(test_indices, args, "test", table_column_dict, count_db_indexes, column_name)
            count_db_indexes += 1
