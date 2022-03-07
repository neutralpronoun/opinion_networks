# %%

import graphviz
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import cython
import tweepy
import json
import requests
import inspect
import re
from tqdm import tqdm
from time import time, sleep
import networkx as nx

from ast import literal_eval


def load_data(extras=True):
    data = pd.read_csv("politicians_connections_two.csv")
    data["Following"] = data["Following"].apply(literal_eval)

    print(data.head())

    usernames = data["Username"].tolist()
    ids = data["ids"].tolist()

    return data, usernames, ids





def get_client():
    with open("dev_keys_json.json", "r") as f:
        keys = json.load(f)
    client = tweepy.Client(bearer_token=keys["Bearer_token"],
                           access_token=keys["API_key"],
                           access_token_secret=keys["API_secret_key"],
                           wait_on_rate_limit=True)
    return client


def decompose_tweet(self, tweet):
    try:
        retweeted_status = tweet.retweeted_status
        is_retweet = True
        # print(self.count,is_retweet)
        # print(retweeted_status.user.id)
        # print(tweet.user.id)
    except:
        is_retweet = False
        # print(dir(tweet))
        # print("\n")
        self.decompose_tweet(tweet)
        pass
    if is_retweet:
        retweet = tweet
        tweet = tweet.retweeted_status
        # self.decompose_tweet(original)

    user = tweet.user
    username = user.screen_name
    id = user.id
    text = tweet.text
    print(username, text)


class Listener(tweepy.Stream):
    def __init__(self, keys, ids):
        os.chdir("./stream_out")

        print("\n")
        print("Found tweet from:")

        self.count = 0

        super().__init__(keys["API_key"], keys["API_secret_key"],
                         keys["Access_token"], keys["Access_token_secret"])

    def report(self, tweet):
        width, height = os.get_terminal_size()
        username = tweet.user.screen_name
        text = tweet.text

        printed_item = f"{username}: {text}"[:width - 5] + "..."

        print(printed_item, end='\r')

    def on_status(self, tweet):
        # self.decompose_tweet(tweet)
        #print(tweet._json)
        self.report(tweet)
        tweet_id = tweet.id

        with open(f"{tweet_id}.json", "w") as f:
            json.dump(tweet._json, f, indent=6)

        self.count += 1


def get_stream(ids):
    with open("dev_keys_api_one.json", "r") as f:
        keys = json.load(f)

    client = Listener(keys, ids)

    return client

if __name__ == "__main__":
    data, usernames, ids = load_data()

    stream = get_stream(ids)

    stream.filter(languages=["en"], follow=ids, filter_level="low")




