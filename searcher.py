from pandas import read_csv
import re
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--true", action="store_true", help="Output contains statements verified to be true" )
    group.add_argument("--false", action="store_true", help="Output contains statements verified to be false")

    parser.add_argument("data", help="Specify the filepath for the data file")
    parser.add_argument("-t", "--threshold", help="Specify minimum amount of mentions a user needs to be printed", type=int, default=-2)
    parser.add_argument("-u", "--users", help="Specify how many users to print", type=int, default=9223372036854775807)

    parser.add_argument("--include-partly-true", action="store_true", help="Output contains statements that are mostly true")
    parser.add_argument("--include-mostly-false", action="store_true", help="Output contains statements that are mostly false")


    parser.add_argument("-o", "--output", help="Specifiy the filepath to save the full output to")
    parser.add_argument("-f", "--force", action="store_true", help="Force write output into a file even if file already exists")

    args = parser.parse_args()
    return args

def search(datapath, 
           threshold=int, 
           users=int, 
           truth=bool, false=bool, partly_true=bool, mostly_false=bool, 
           output=None, force=bool):
    
    data = read_csv(datapath)
    target_col = data['fact_tweet']
    truth_col = data['Truth Score']

    truths = [str for str in truth_col if str == "True"]
    falses = [str for str in truth_col if str == "False"]
    mostly_truths = [str for str in truth_col if str == "Mostly true"] 
    mostly_falses = [str for str in truth_col if str == "Mostly false"]

    fakes = re.findall(r'@\w+', target_col.to_string())
    fake_accs = {}

    for acc in fakes:
        fake_accs[acc] = fake_accs.get(acc, 0) + 1

    top_appearing = []
    stop = 1
    for key, value in sorted(fake_accs.items(), key=lambda kv: kv[1], reverse=True):
        if threshold == -2 or value > threshold:
            if stop > users:
                break
            stop += 1
            print("%s: %s" % (key, value))
            top_appearing.append(key)

    if output is not None:
        mode = 'a' if force else 'w'
        with open(output, mode) as f:
            for key, value in fake_accs.items():
                f.write("%s: %s\n" % (key, value))

def main():
    search(parse_args().data, 
           parse_args().threshold, 
           parse_args().users,
           parse_args().true,
           parse_args().false,
           parse_args().include_partly_true,
           parse_args().include_mostly_false,
           parse_args().output,
           parse_args().force)
    
if __name__ == "__main__":
    main()
