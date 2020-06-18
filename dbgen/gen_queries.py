import os
# import numpy as np
import random
import argparse
import subprocess
import random
from pathlib import Path


"""For TPC-H, we randomly sampled 80% of the templates into the training group, then put the remaining 20% of the templates into the test group (modulo rounding). Then we randomly sampled these templates with replacement until we'd reached the appropriate number of queries in each group."""


def generate_queries(indices, num_queries, args, split, count = 1, directory='.'):
    """Generate queries from the list of allowed templates"""
    num_queries += count
    
    while count < num_queries:
        dice = random.randint(0, len(indices) - 1)
        print(dice, len(indices))
        template = indices[dice]
        directory = './generated_queries/' + split + '/'
        file_path = directory + str(count) + '.sql'
        Path(directory).mkdir(parents=True, exist_ok=True)
        # os.remove(file_path)
        subprocess.call('touch ' + file_path, shell=True)
        shell_cmd = './qgen ' + str(template) + ' > ' + file_path
        count += 1
        subprocess.call(shell_cmd, shell=True)
        # print(shell_cmd)

def generate_showplans(num_queries, args, split, count = 1, directory='.'):
    """Generate showplans from the list of queries"""
    num_queries += count
    while count < num_queries:
        input_path = './generated_queries/' + split + '/' + str(count) + '.sql'
        directory = './generated_showplans/' + split + '/'
        output_path = directory + str(count) + '.txt'
        Path(directory).mkdir(parents=True, exist_ok=True)
        subprocess.call('touch ' + output_path, shell=True)
        shell_cmd = f'sqlcmd -S {args.server} -U {args.user} -P {args.password} -d TPCH -i {input_path} -o {output_path}'
        count += 1
        subprocess.call(shell_cmd, shell=True)
        # print(shell_cmd)


if __name__ == "__main__":
    # os.chdir('./dbgen')
    print(os.getcwd())
    NUM_TEMPLATES = 22

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u", "--user", help="db administrator", default="SA")
    arg_parser.add_argument("-p", "--password", help="password")
    arg_parser.add_argument("--num_queries_train",
                            help="Number of train queries to generate", type=int)
    arg_parser.add_argument("--num_queries_test",
                            help="Number of test queries to generate", type=int)
    arg_parser.add_argument("--server", help="The server to run sqlcmd from", default="localhost")
    args = arg_parser.parse_args()

    indices = list(range(1, NUM_TEMPLATES + 1))  # 22 query templates
    random.seed("167")
    random.shuffle(indices)
    test_split = int(0.2 * NUM_TEMPLATES)
    test_indices = indices[:test_split]
    train_indices = indices[test_split:]
    # generate queries
    generate_queries(train_indices, args.num_queries_train, args, "train")
    generate_queries(test_indices, args.num_queries_test, args, "test")
    # generate showplans
    generate_showplans(args.num_queries_train, args, "train")
    generate_showplans(args.num_queries_test, args, "test")