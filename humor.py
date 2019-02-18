import nltk
import re
import json
from operator import itemgetter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

tknzr = TweetTokenizer()

def pres(data):
    host_dict = ["joke", "#joke"]
    stop_dict = set(stopwords.words('english'))
    stop_dict.update(["golden", "globes", "#goldenglobes", "awards", "tweet", "tweets", "award", "rt", "@", "best", "motion", "actress", "actor", "drama", "picture"])
    stop_dict.update(["funny", "sassy", "hilarious","best","terrible", "horrible","amazing","great","good","make","worst","last","presenters","presenters'","making"])

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
                nnp_list = [s[0] for s in tagged_tweet if s[1] == 'NNP' and s[0].lower() not in stop_dict]
                # print(nnp_list)
                for i in range(len(token_tweet)):
                    if token_tweet[i] == "joke" or token_tweet[i] == "joke." or token_tweet[i] == "jokes" or token_tweet[i] == "jokes.":
                        key = True
                        count = 1
                        while key:
                            if i-count >= 0 and token_tweet[i-count].lower() not in stop_dict:
                                temp_quote = token_tweet[i-count] + " " + temp_quote
                                count += 1
                            else:
                                key = False

                        temp_quote = temp_quote + "joke"

                        if temp_quote in final_dict and temp_quote != "joke":
                            prev_count = final_dict[temp_quote]
                            final_dict.update({temp_quote:prev_count+1})
                        else:
                            final_dict.update({temp_quote:1})

    sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
    final_ret = {"most talked about jokes":[]}
    count = 0
    for i in sorted_list:
        if count == 2:
            break
        lisst = final_ret["most talked about jokes"]
        lisst.append(i[0])
        final_ret.update({"most talked about jokes":lisst})
        count += 1
    return final_ret

    # print(sorted_list[0][0],sorted_list[1][0])
# print(pres(data))
