import pandas as pd
import re
import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("data", help="Specify the filepath for the data file")
    parser.add_argument("threshold", help="Minimum amount of mentions a user needs to be printed", type=int)
    parser.add_argument("-u", "--users", help="Specify how many users to print", type=int, default=-1)
    parser.add_argument("-o", "--output", help="Specifiy the filepath to save the output to")

    args = parser.parse_args()
    return args

def search(datapath, threshold=int, users=int, output=None):
    data = pd.read_csv(datapath)
    target_col = data['fact_tweet']

    fakes = re.findall(r'@\w+', target_col.to_string())
    fake_accs = {}

    for acc in fakes:
        fake_accs[acc] = fake_accs.get(acc, 0) + 1

    top_appearing = []
    stop = 1
    for key, value in sorted(fake_accs.items(), key=lambda kv: kv[1], reverse=True):
        if value > threshold:
            if stop > users:
                break
            stop += 1
            print("%s: %s" % (key, value))
            top_appearing.append(key)

    if output is not None:
        with open(output, 'w') as f:
            for key, value in fake_accs.items():
                f.write("%s: %s\n" % (key, value))

def main():
    search(parse_args().data, 
           parse_args().threshold, 
           parse_args().users,
           parse_args().output)

if __name__ == "__main__":
    main()
