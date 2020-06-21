import os
import random
import argparse
import subprocess
import random
from pathlib import Path


"""For TPC-H, we randomly sampled 80% of the templates into the training group, then put the remaining 20% of the templates into the test group (modulo rounding). Then we randomly sampled these templates with replacement until we'd reached the appropriate number of queries in each group."""


def generate_queries(indices,  args, split, directory='.'):
    """Generate queries from the list of allowed templates"""
    print(f"Template for {split}: ", end='')
    for template in indices:
        print(template, end=' ')
        for count in range(args.num_queries):
            directory = f"./generated_queries/{split}/{template}/"
            file_path = directory+f"{str(count)}.sql"
            Path(directory).mkdir(parents=True, exist_ok=True)
            subprocess.call('touch ' + file_path, shell=True)
            shell_cmd = './qgen ' + str(template) + ' > ' + file_path
            subprocess.call(shell_cmd, shell=True)
            # print(shell_cmd)
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
            subprocess.call(shell_cmd, shell=True)
            # print(shell_cmd)


if __name__ == "__main__":
    os.chdir('./dbgen')
    print(os.getcwd())
    NUM_TEMPLATES = 22

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-u", "--user", help="db administrator", default="SA")
    arg_parser.add_argument("-p", "--password", help="password")
    arg_parser.add_argument("--num_queries",
                            help="Number of queries to generate per template", type=int)
    arg_parser.add_argument(
        "--server", help="The server to run sqlcmd from", default="localhost")
    arg_parser.add_argument(
        "--test_split", help="The percentage of templates to go into test set", default=0.2, type=float)
    arg_parser.add_argument("--showplan", action="store_true", default=True)
    args = arg_parser.parse_args()

    indices = list(range(1, NUM_TEMPLATES + 1))  # 22 query templates
    random.seed("167")
    random.shuffle(indices)
    test_split = int(args.test_split * NUM_TEMPLATES)
    test_indices = indices[:test_split]
    train_indices = indices[test_split:]
    # generate queries
    generate_queries(train_indices, args, "train")
    generate_queries(test_indices, args, "test")

    if args.showplan:
        # generate showplans
        generate_showplans(train_indices, args, "train")
        generate_showplans(test_indices, args, "test")
