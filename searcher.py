from pandas import read_csv
import re
import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("data", help="Specify the filepath for the data file")
    parser.add_argument("-t", "--threshold", help="Specify minimum amount of mentions a user needs to be printed", type=int, default=-2)
    parser.add_argument("-u", "--users", help="Specify how many users to print", type=int, default=9223372036854775807)
    parser.add_argument("-o", "--output", help="Specifiy the filepath to save the full output to")
    parser.add_argument("-a", "--add", action="store_true", help="Specifications provided will be added to the output file")

    args = parser.parse_args()
    return args

def search(datapath, threshold=int, users=int, output=None, add=bool):
    data = read_csv(datapath)
    target_col = data['fact_tweet']

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

    stop = 1
    if output is not None:
        if add:
            with open(output, 'a') as f:
                for key, value in sorted(fake_accs.items(), key=lambda kv: kv[1], reverse=True):
                    if threshold == -2 or value > threshold:
                        if stop > users:
                            break
                        stop += 1
                        f.write("%s: %s\n" % (key, value))
                        top_appearing.append(key)
        else:
            with open(output, 'a') as f:
                for key, value in fake_accs.items():
                    f.write("%s: %s\n" % (key, value))

def main():
    search(parse_args().data, 
           parse_args().threshold, 
           parse_args().users,
           parse_args().output,
           parse_args().add)
    
if __name__ == "__main__":
    main()
