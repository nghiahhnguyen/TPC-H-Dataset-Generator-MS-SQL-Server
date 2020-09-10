import os
import random
import argparse
import subprocess
import random
from pathlib import Path

from .utils import extract_tables_columns


def extract_clauses(string):
    print(f"String:\n {string}\n")
    if 'where' in string:
        split_keyword = 'where'
    else:
        split_keyword = 'group by'

    stack = []
    current_word = ''
    split_position = -1
    for i, char in enumerate(string):
        print(f"'{char}'", current_word)
        if char in [' ', '\t', '\n']:
            if current_word == split_keyword:
                print(stack)
                while stack[-1] != 'select':
                    stack.pop()
                stack.pop()
                if len(stack) == 0:
                    split_position = i
                    break
            if char == ' ' and current_word == 'group':
                current_word = current_word + char
            else:
                current_word = ''
            # else:
            #     current_word = current_word + char
        else:
            current_word = current_word + char
        if current_word in ['select', 'from']:
            stack.append(current_word)

    # print(string.split(split_keyword))
    # select_from = string.split(split_keyword)[0]
    select_from = string[:split_position - len(split_keyword)]
    # print("select_from", select_from)
    # conditions_clause = split_keyword.join(string.split(split_keyword)[1:])
    conditions_clause = string[split_position:]
    # print("where_clause", where_clause)
    from_clause = 'from'.join(select_from.split('from')[1:])
    select_clause = select_from.split('from')[0]
    from_clause = from_clause.strip()
    return select_from, conditions_clause, select_clause, from_clause, split_keyword


def create_filtered_queries(args, input_path, table_column_dict):
    with open(input_path, 'r') as f:
        string = f.read()
        # print(string)
        query_options = string.split('go')[0]
        # print(string.split('\ngo\n'))
        string = '\ngo\n'.join(
            list(filter(lambda x: len(x.strip()) > 0, string.split('\ngo\n')))[-1:])
        select_from, where_clause, select_clause, from_clause, split_keyword = extract_clauses(
            string)
        # print(f"From Clause: \n{from_clause}")
        if from_clause[0] == '(':
            inner_statement = from_clause[1:-1]
            count = 0
            stack = []
            for char in from_clause:
                if char == '(':
                    stack.append(char)
                elif char == ')':
                    stack.pop()
                    if len(stack) == 0:
                        break
                count += 1
            inner_statement = from_clause[1:count]
            print(f"Inner Statement:\n{inner_statement}")
            inner_select_from, inner_where, _, inner_from, _ = extract_clauses(
                inner_statement)
            if ',' in inner_from:
                tables = inner_from.strip().split(',')
            else:
                tables = inner_from.strip().split('left outer join')
            for table in tables:
                table = table.strip()
                for column, column_data_type in table_column_dict[table]:
                    if column_data_type == "int":
                        extra_filter_1 = f"{column} > {1000}"
                        extra_filter_2 = f"{column} < {10}"
                        from_clause_1 = f"{inner_select_from} where {extra_filter_1} and {inner_where}"
                        from_clause_2 = f"{inner_select_from} where {extra_filter_2} and {inner_where}"
                        filtered_query_1 = f"{query_options}\ngo\n{select_clause} from ({from_clause_1}) {split_keyword} {extra_filter_1} and {where_clause}"
                        filtered_query_2 = f"{query_options}\ngo\n{select_clause} from ({from_clause_2})  {split_keyword}where {extra_filter_2} and {where_clause}"
                        return filtered_query_1, filtered_query_2
        tables = from_clause.split(',')
        for table in tables:
            table = table.strip()
            for column, column_data_type in table_column_dict[table]:
                if column_data_type == "int":
                    extra_filter_1 = f"{column} > {1000}"
                    extra_filter_2 = f"{column} < {10}"
                    filtered_query_1 = f"{query_options}\ngo\n{select_from} where {extra_filter_1} and {where_clause}"
                    filtered_query_2 = f"{query_options}\ngo\n{select_from} where {extra_filter_2} and {where_clause}"
                    return filtered_query_1, filtered_query_2


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
        indices = [i + 1 for i in range(33)]
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
        for column_name, _ in column_list:
            if column_name == "skip":
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
