import os
import random
import argparse
import subprocess
import random
from pathlib import Path


def generate_configuration(args):
    # get the string for each table
    table_column_dict = {}
    with open(args.schema_path, "r") as f:
        string = f.read()
        string = list(string.split("GO"))
        table_strings = string[2:-1]
        for table_string in table_strings:
            start, end = table_string.find('('), table_string.rfind(')')
            table_content = table_string[start + 1: end]
            table_header = table_string[:start]
            table_name = table_header[table_header.rfind(
                '[') + 1: table_header.rfind(']')]
            print(f"Table name: {table_name}")
            table_column_dict[table_name] = []
            column_strs = list(table_content.split(','))
            for column_str in column_strs:
                if '[' not in column_str or ']' not in column_str:
                    continue
                column_name = column_str[column_str.find(
                    '[') + 1: column_str.find(']')]
                column_name = column_name.lower()
                table_column_dict[table_name].append(column_name)
                print(column_name)
    return table_column_dict


def generate_showplans(indices, args, split, table_column_dict, directory='.'):
    """Generate showplans from the list of queries"""
    print(f"Current split: {split}")
    count_db_indices = 0
    for table_name, column_list in table_column_dict.items():
        for column_name in column_list:
            command = f'sqlcmd -s {args.server} -u {args.user} -p {args.password} -d tpch -q "CREATE INDEX auto_idx_{count_db_indices} ON {table_name}.{column_name}'
            count_db_indices += 1
            for template in indices:
                for count in range(args.num_queries):
                    input_directory = f"./generated_queries/{split}/{template}/"
                    input_path = input_directory+f"{str(count)}.sql"
                    directory = f"./generated_equivalent_showplans/{split}/template_{template}/config_{count_db_indices}/"
                    output_path = directory + str(count) + '.txt'
                    Path(directory).mkdir(parents=True, exist_ok=True)
                    subprocess.call('touch ' + output_path, shell=True)
                    shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -i {input_path} -o {output_path}'
                    print(shell_cmd)
                    subprocess.call(shell_cmd, shell=True)


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
        "--schema_path", help="Path to the schema", default="tpc-h.sql")
    args = arg_parser.parse_args()

    table_column_dict = generate_configuration(args)

    os.chdir('./dbgen')
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

    if args.showplan:
        # generate showplans
        generate_showplans(train_indices, args, "train", table_column_dict)
        generate_showplans(dev_indices, args, "dev", table_column_dict)
        generate_showplans(test_indices, args, "test", table_column_dict)
