import nltk
import re
import json
from operator import itemgetter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

tknzr = TweetTokenizer()

def pres(data):
    host_dict = ["host","hosting","hosted"]
    stop_dict = ["now:","next","ran","golden", "globes", "#goldenglobes", "#goldenglobes!!!", "awards", "tweet", "tweets", "award", "rt", "@", "motion", "actress", "actor", "drama", "picture"]

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
                # print(tagged_tweet)

                # print(nnp_list)

                nnp_list = [s[0] for s in tagged_tweet if (s[1] == 'JJ' or s[1] == "JJS" )and s[0].lower() not in stop_dict]
                # print(nnp_list)
                for nnp_word in nnp_list:
                    nnp_word = nnp_word.lower()
                    if nnp_word in final_dict and nnp_word != "":
                        prev_count = final_dict[nnp_word]
                        final_dict.update({nnp_word:prev_count+1})
                    else:
                        final_dict.update({nnp_word:1})

    sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
    final_ret = {"sentiment about the hosts":[]}
    count = 0
    for i in sorted_list:
        if count == 8:
            break
        lisst = final_ret["sentiment about the hosts"]
        lisst.append(i[0])
        final_ret.update({"sentiment about the hosts":lisst})
        count += 1
    return final_ret

    # print(sorted_list[0][0],sorted_list[1][0])
# print(pres(data))
