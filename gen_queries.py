import os
import numpy as np
import argparse
import subprocess


"""For TPC-H, we randomly sampled 80% of the templates into the training group, then put the remaining 20% of the templates into the test group (modulo rounding). Then we randomly sampled these templates with replacement until we'd reached the appropriate number of queries in each group."""


def generate_queries(indices, num_queries, args, split, count = 1, directory='.'):
    """Generate queries from the list of allowed templates"""
    num_queries += count
    while count < num_queries:
        template = indices[np.random.randint(0, len(indices))]
        file_path = './generated_queries/' + split + '/' + str(count) + '.sql'
        subprocess.call('touch ' + file_path, shell=True)
        shell_cmd = './qgen ' + str(template) + ' > ' + file_path
        count += 1
        subprocess.call(shell_cmd, shell=True)
        # print(shell_cmd)


if __name__ == "__main__":
    NUM_TEMPLATES = 22
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u", "--user", help="db administrator")
    arg_parser.add_argument("-p", "--password", help="password")
    arg_parser.add_argument("--num_queries_train",
                            help="Number of train queries to generate", type=int)
    arg_parser.add_argument("--num_queries_test",
                            help="Number of test queries to generate", type=int)
    args = arg_parser.parse_args()

    os.getcwd()
    os.chdir('./dbgen')
    indices = list(range(1, NUM_TEMPLATES + 1))  # 22 query templates
    np.random.shuffle(indices)
    test_split = int(0.2 * NUM_TEMPLATES)
    test_indices = indices[:test_split]
    train_indices = indices[test_split:]
    generate_queries(train_indices, 10, args.num_queries_train, "train")
    generate_queries(test_indices, 10, args.num_queries_test, "test")