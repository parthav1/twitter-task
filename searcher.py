import pandas as pd
import re
#import tweepy as tw
#from config.config import API_key, SecretAPI_key, access_token, secret_access_token

data = pd.read_csv('data/matches.csv')
target_col = data['fact_tweet']


fakes = re.findall(r'@\w+', target_col.to_string())
fake_accs = {}

for acc in fakes:
    fake_accs[acc] = fake_accs.get(acc, 0) + 1


# Are in descending order, first one being the most referenced.
# Threshold for being in the list is at least 5 references.
top_appearing = []
for key, value in sorted(fake_accs.items(), key=lambda kv: kv[1], reverse=True):
    if value > 5:
        print("%s: %s" % (key, value))
        top_appearing.append(key)

print(top_appearing)



