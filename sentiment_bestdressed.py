import nltk
import re
import json
from operator import itemgetter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

tknzr = TweetTokenizer()

def pres(data):
    host_dict = ["beautiful", "best dressed","gorgeous"]
    stop_dict = ["#","beautiful", "gorgeous", "ran","golden", "globes", "globe", "it's", "red","#goldenglobes", "#goldenglobes!!!", "awards", "tweet", "tweets", "award", "rt", "@", "best", "motion", "actress", "actor", "drama", "picture"]

    final_dict = {}
    final_dict2 = {}

    for tweet_json in data:
        tweet = tweet_json["text"]
        tweet_lower = tweet_json["text"].lower()
        count = 0
        for host_word in host_dict:
            if host_word in tweet_lower:
                # print(tweet)
                token_tweet = tweet.split()
                temp_quote = ""
                tagged_tweet = nltk.pos_tag(token_tweet)


                nnp_list = []
                temp_w = ""

                for s in tagged_tweet:
                    count = 0
                    lit = True
                    while count < len(stop_dict):
                        if stop_dict[count] in s[0].lower():
                            lit = False
                        count += 1
                    if lit and s[1] == "NNP":
                        temp_w += s[0] + " "
                    elif lit:
                        nnp_list.append(temp_w)
                        temp_w = ""

                # print(nnp_list)
                for nnp_word in nnp_list:
                    nnp_word = nnp_word.lower()
                    if nnp_word in final_dict and nnp_word != "":
                        prev_count = final_dict[nnp_word]
                        final_dict.update({nnp_word:prev_count+1})
                    else:
                        final_dict.update({nnp_word:1})

    sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
    final_ret = {"best dressed":[]}
    count = 0
    for i in sorted_list:
        if count == 8:
            break
        lisst = final_ret["best dressed"]
        lisst.append(i[0])
        final_ret.update({"best dressed":lisst})
        count += 1
    return final_ret

    # print(sorted_list[0][0],sorted_list[1][0])
# print(pres(data))
