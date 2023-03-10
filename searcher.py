import pandas as pd
import re
import argparse
import configparser
import sys

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--create-config", action="store_true", help="Write a list of all the different truth scores")
    group.add_argument("--config", help="If using a config file and specify its path")

    parser.add_argument("data", help="Specify the filepath for the data file")
    parser.add_argument("--list-users", action="store_true", help="Produces the regular output of each user")
    parser.add_argument("-t", "--threshold", help="Specify minimum amount of mentions a user needs to be printed", type=int, default=-2)
    parser.add_argument("-u", "--users", help="Specify how many users to print", type=int, default=9223372036854775807)
    
    parser.add_argument("-o", "--output", help="Specifiy the filepath to save the full output to; having a config will affect the output that goes to the file")
    parser.add_argument("-f", "--force", action="store_true", help="Force write output into a file even if file already exists")

    args = parser.parse_args()
    return args

def search(datapath, 
           threshold=int, 
           users=int, list_users=bool,
           config_path=str, create_config=bool,
           output=None, force=bool):
    
    data = pd.read_csv(datapath)
    target_col = data['fact_tweet']
    truth_col = data['Truth Score'].apply(lambda x: (str(x)).strip().lower())
    
    truth_col = truth_col.str.replace('false, ', '')
    truth_col = truth_col.str.replace('labelled ', '')
    truth_col = truth_col.str.replace('labeled ', '')

    unique_strings = truth_col.value_counts().to_dict()
    config_dict = {}
    if config_path is not None:
        config = configparser.ConfigParser()
        config.read(config_path)
        for k, v in unique_strings.items():
            if config.has_option('truth', k) and config.getboolean('truth', k):
                 unique_strings[k] = True

        config_dict = {}
        for k in unique_strings:
            config_dict[k] =  unique_strings[k]

    elif create_config:
        for k in unique_strings:
            config_dict[k] = True
        with open('config.ini', 'w') as f:
            f.write('[truth]\n')
            for k, v in config_dict.items():
                f.write(f"{k} = {v}\n")
        print("Config created. Filename is config.ini")
        sys.exit()

    accounts = []
    for index, row in target_col.items():
        fake = re.findall(r'@\w+', str(row))
        for acc in fake:
            accounts.append((acc, index, truth_col.iloc[index]))

    out = []
    if config_path is not None:
        for key, value in config_dict.items():
            for acc, row, truth in accounts:
                if key == truth and config_dict[key] == True:
                    out.append(acc)
    else:
        for index, row in target_col.items():
            fake = re.findall(r'@\w+', str(row))
            for acc in fake:
                out.append(acc)

    fake_accs = {}
    for acc in out:
        fake_accs[acc] = fake_accs.get(acc, 0) + 1

    sorted_fakes = sorted(fake_accs.items(), key=lambda kv: kv[1], reverse=True)

    stop = 1
    for key, value in sorted_fakes:
        if (threshold == -2 or value > threshold):
            if stop > users:
                break
            stop += 1
            print("%s: %s" % (key, value)) if not list_users else print(key)
    
    if output is not None:
        mode = 'a' if force else 'w'
        with open(output, mode) as f:
            for key, value in fake_accs.items():
                f.write("%s: %s\n" % (key, value)) 

def main():
    search(parse_args().data, 
           parse_args().threshold, 
           parse_args().users,
           parse_args().list_users,
           parse_args().config,
           parse_args().create_config,
           parse_args().output,
           parse_args().force)
    
if __name__ == "__main__":
    main()
