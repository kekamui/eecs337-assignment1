import nltk
import re
import json
from operator import itemgetter
from nltk.tokenize import TweetTokenizer

def winners(data, list_of_awards):

    stop_dict = ["http","golden", "globes", "goldenglobes", "awards", "tweet",
                "tweets", "award", "rt", "@", "best", "motion", "actress",
                "actor", "drama", "picture","mtvnews","television","series",
                "foreign", "film","comedy","hbo","girlshbo", "|","|"]

    result = {}

    for award_name in list_of_awards:
        host_word = award_name

        final_dict = {}
        final_dict2 = {}

        for tweet_json in data:
            tweet = tweet_json["text"]
            tweet_lower = tweet_json["text"].lower()
            if host_word in tweet_lower:
                # print(host_word)

                sen1 = host_word.split()[-1]
                # print(sen1)
                token_split = tweet.split()
                token_tweet = nltk.word_tokenize(tweet)
                tagged_tweet = nltk.pos_tag(token_tweet)
                # print(tagged_tweet)

                token_tweet_l = nltk.word_tokenize(tweet_lower)
                # print("S")
                # print(token_tweet_l)

                if sen1 in token_tweet_l:
                    indexof = token_tweet_l.index(sen1)

                    temp_w = ""
                    count = 1

                    if indexof+count < len(tagged_tweet) and (tagged_tweet[indexof + count][0] == ":" or tagged_tweet[indexof + count][0] == "-" or tagged_tweet[indexof + count][0].lower() == "is"):
                        count += 1

                        while indexof + count < len(tagged_tweet):
                            if ((tagged_tweet[indexof + count][0] not in stop_dict and (tagged_tweet[indexof + count][1] == "NNP" or tagged_tweet[indexof + count][1] == "NN") and tagged_tweet[indexof + count][0] != "–")) or tagged_tweet[indexof + count][1] == "CD":
                                if temp_w == "":
                                    temp_w = tagged_tweet[indexof + count][0]
                                else:
                                    temp_w = temp_w + " " + tagged_tweet[indexof + count][0]
                                count += 1
                            else:
                                break

                    # print(temp_w)
                    temp_w = temp_w.lower()

                    if temp_w != "":
                        if temp_w[0] == "'":
                            temp_w = temp_w[1:]
                        if temp_w in final_dict2:
                            prev_count = final_dict2[temp_w]
                            final_dict2.update({temp_w:prev_count+1})
                        else:
                            final_dict2.update({temp_w:1})

                nnp_list = [s[0] for s in tagged_tweet if s[1] == 'NNP' and s[0].lower() not in stop_dict]

                for nnp_word in nnp_list:
                    if nnp_word in final_dict:
                        prev_count = final_dict[nnp_word]
                        final_dict.update({nnp_word:prev_count+1})
                    else:
                        final_dict.update({nnp_word:1})

        if len(final_dict2) == 0:
            sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
            # print(sorted_list)
            if len(sorted_list) >= 2:
                # print("1")
                result.update({host_word:sorted_list[0][0].lower()+" "+sorted_list[1][0].lower()})
            else:
                result.update({host_word:""})
        else:
            sorted_list = sorted(final_dict2.items(), key = itemgetter(1), reverse = True)
            # print("2")
            result.update({host_word:(sorted_list[0][0])})

    return result
