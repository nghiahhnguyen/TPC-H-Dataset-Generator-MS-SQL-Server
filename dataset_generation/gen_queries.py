import os
import random
import argparse
import subprocess
import random
from pathlib import Path

from utils import extract_tables_columns


"""
For TPC-H, we randomly sampled 80% of the templates into the training group, 
then put the remaining 20% of the templates into the test group (modulo rounding). 
Then we randomly sampled these templates with replacement until we'd reached the appropriate number of queries in each group.
"""


def generate_queries(indices, args, split, directory='.'):
    """Generate queries from the list of allowed templates"""
    print(f"Template for {split}: ", end='')
    for template in indices:
        print(template, end=' ')
        for count in range(args.num_queries):
            directory = f"./generated_queries/{split}/{template}/"
            file_path = directory+f"{str(count)}_{args.filter}.sql"
            Path(directory).mkdir(parents=True, exist_ok=True)
            subprocess.call('touch ' + file_path, shell=True)
            shell_cmd = f'./qgen {str(template)} -r {(count + 1) * 100} -s 1000 > {file_path}'
            # print(shell_cmd)
            subprocess.call(shell_cmd, shell=True)
    print()


def generate_showplans(indices, args, split, directory='.'):
    """Generate showplans from the list of queries"""
    for template in indices:
        for count in range(args.num_queries):
            input_directory = f"./generated_queries/{split}/{template}/"
            input_path = input_directory+f"{str(count)}.sql"
            directory = f"./generated_showplans/{split}/{template}/"

            output_path = directory + str(count) + '.txt'
            Path(directory).mkdir(parents=True, exist_ok=True)
            subprocess.call('touch ' + output_path, shell=True)
            shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d TPCH -i {input_path} -o {output_path}'
            # print(shell_cmd)
            subprocess.call(shell_cmd, shell=True)


if __name__ == "__main__":
    os.chdir('../dbgen')
    print(os.getcwd())
    NUM_TEMPLATES = 13

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-U", "--user", help="db administrator", default="SA")
    arg_parser.add_argument("-P", "--password", help="password")
    arg_parser.add_argument("--num_queries",
                            help="Number of queries to generate per template", type=int)
    arg_parser.add_argument(
        "--server", help="The server to run sqlcmd from", default="localhost")
    arg_parser.add_argument(
        "--test_split", help="The percentage of templates to go into test set", default=0.2, type=float)
    arg_parser.add_argument(
        "--dev_split", help="The percentage of templates to go into dev set", default=0.2, type=float)
    arg_parser.add_argument("--generate_queries",
                            action="store_true", default=False)
    arg_parser.add_argument("--showplan", action="store_true", default=False)
    arg_parser.add_argument("--filter", type=int)
    arg_parser.add_argument("--dataset", choices=("tpch", "tpcds"))
    args = arg_parser.parse_args()

#     indices = list(range(1, NUM_TEMPLATES + 1))  # 22 query templates
    if args.dataset == "tpch":
        indices = [1, 2, 3, 4, 5, 6, 7, 10, 12, 14, 15, 18, 19]
    else:
        indices = [1, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    random.seed("167")
    random.shuffle(indices)
    test_split = int(args.test_split * NUM_TEMPLATES)
    dev_split = test_split + int(args.dev_split * NUM_TEMPLATES)
    test_indices = indices[:test_split]
    dev_indices = indices[test_split:dev_split]
    train_indices = indices[dev_split:]

    if args.generate_queries:
        # generate queries
        generate_queries(train_indices, args, "train")
        generate_queries(dev_indices, args, "dev")
        generate_queries(test_indices, args, "test")
    if args.showplan:
        # generate showplans
        generate_showplans(train_indices, args, "train")
        generate_showplans(dev_indices, args, "dev")
        generate_showplans(test_indices, args, "test")
