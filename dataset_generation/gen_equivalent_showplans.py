import os
import random
import argparse
import subprocess
import random
from pathlib import Path

from utils import extract_tables_columns


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
        # print("from_clause", from_clause)
        tables = from_clause.split(',')
        # print(tables)
        for table in tables:
            table = table.strip()
            for column, column_data_type in table_column_dict[table]:
                if column_data_type == "int":
                    extra_filter_1 = f"{column} > {1000}"
                    extra_filter_2 = f"{column} < {10}"
                    filtered_query_1 = f"{query_options}\ngo\n{select_from} where {extra_filter_1} and {where_clause}"
                    filtered_query_2 = f"{query_options}\ngo\n{select_from} where {extra_filter_2} and {where_clause}"
                    # print(filtered_query_1)
                    # print(filtered_query_2)
                    return filtered_query_1, filtered_query_2


def drop_all_indexes(table_column_dict, args):
    count_drop_db_indexes = 0
    for table_name, column_list in table_column_dict.items():
        for _, _ in column_list:
            command = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -Q "DROP INDEX {table_name}.auto_idx_{count_drop_db_indexes};"'
            subprocess.call(command, shell=True)
            count_drop_db_indexes += 1


def generate_showplans(indices, args, split, table_column_dict, count_db_indexes, directory='.'):
    """Generate showplans from the list of queries"""
    print(f"Current split: {split}")

    for template in indices:
        for count in range(args.num_queries):
            input_directory = f"./generated_queries/{split}/{template}/"
            input_path = input_directory+f"{str(count)}"
            directory = f"../dataset_generation/generated_equivalent_showplans/{split}/template_{template}/config_{count_db_indexes}/"
            output_path = directory + str(count)
            Path(directory).mkdir(parents=True, exist_ok=True)
            subprocess.call('touch ' + output_path, shell=True)

            # filtered_query_1, filtered_query_2 = create_filtered_queries(
            #     args, input_path, table_column_dict)
            # print(
            #     f"Filtered query 1: {filtered_query_1}\n\nFiltered query 2: {filtered_query_2}\n")
            # query_1_path = "./tmp_filtered_query_1.sql"
            # query_2_path = "./tmp_filtered_query_2.sql"
            # with open(query_1_path, 'w') as f:
            #     f.write(filtered_query_1)
            # with open(query_2_path, 'w') as f:
            #     f.write(filtered_query_2)
            shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -i {input_path}_0.sql -o {output_path}_0.txt'
            print(shell_cmd)
            subprocess.call(shell_cmd, shell=True)
            shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -i {input_path}_1.sql -o {output_path}_1.txt'
            print(shell_cmd)
            subprocess.call(shell_cmd, shell=True)


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
        "--test_split", help="The percentage of templates to go into test set", default=0.2, type=float)
    arg_parser.add_argument(
        "--dev_split", help="The percentage of templates to go into dev set", default=0.2, type=float)
    arg_parser.add_argument("--showplan", action="store_true", default=True)
    arg_parser.add_argument(
        "--schema_path", help="Path to the schema", default="../tpc-h.sql")
    # arg_parser.add_argument(
    #     '--filter', type=int, help="The filter you want to apply", choices=[0, 1]
    # )
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

    # generate showplans
    count_db_indexes = 0
    # iterate through columns and create index on them
    for table_name, column_list in table_column_dict.items():
        for column_name, _ in column_list:
            command = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d tpch -Q "CREATE INDEX auto_idx_{count_db_indexes} ON {table_name}({column_name});"'
            print(command)
            subprocess.call(command, shell=True)
            count_db_indexes += 1
            if args.showplan:
                generate_showplans(train_indices, args,
                                   "train", table_column_dict, count_db_indexes)
                generate_showplans(dev_indices, args, "dev",
                                   table_column_dict, count_db_indexes)
                generate_showplans(test_indices, args,
                                   "test", table_column_dict, count_db_indexes)
    drop_all_indexes(table_column_dict, args)
