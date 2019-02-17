import nltk
import re
import json
from winners import winners
from operator import itemgetter
from nltk.tokenize import TweetTokenizer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

with open('gg2013.json') as json_file:
    data = json.load(json_file)


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


big_dict = [
["best performance by an actress in a motion picture - drama"],
["best performance by an actor in a motion picture - drama"],
["best performance by an actress in a motion picture - musical or comedy"],
["best performance by an actor in a motion picture - musical or comedy"],
["best motion picture - drama"],
["best motion picture - musical or comedy"],
["best performance by an actress in a supporting role in any motion picture","best performance by an actress in a supporting role in a motion picture"],
["best performance by an actor in a supporting role in any motion picture","best performance by an actor in a supporting role in a motion picture"],
["best director - motion picture"],
["best screenplay - motion picture"],
["best motion picture - animated", "best animated feature film", "best animated feature"],
["best motion picture - foreign language", "best foreign film", "best foreign language"],
["best original score - motion picture"],
["best original song - motion picture"],
["best television series - drama"],
["best television series - musical or comedy"]
]

important_list = ["beat", "but", "better", "contenders", "contender", "over", "upset", "lost", "liked", "wish", "doesn't win", "please", "robbed"]

stop_dict_nominees = ["golden", "globes", "goldenglobes", "awards", "tweet",
            "tweets", "award", "rt", "@", "best", "motion", "actress",
            "actor", "drama", "picture","mtvnews","television","series",
            "foreign", "film","comedy","hbo","girlshbo", "pixar", "best", "actress", "actor"]

# find all tweets with winner in it
# if tweet has winner, find tweet with a key_dict word in it
# if so, find NNPs in the tweet, count the NNPs

# def winners(data, award_data):
#     # {award:(winner, [nominee1, nominee2]), }
#     award_winner_dict ={}
#     host_dict = award_data
#     stop_dict = ["golden", "globes", "goldenglobes", "awards", "tweet",
#                 "tweets", "award", "rt", "@", "best", "motion", "actress",
#                 "actor", "drama", "picture","mtvnews","television","series",
#                 "foreign", "film","comedy","hbo","girlshbo", "pixar"]
#
#     final_dict = {}
#     final_dict2 = {}
#
#     for tweet_json in data:
#         # gets the text part of a tweet data
#         tweet = tweet_json["text"]
#         # lowercases tweet text
#         tweet_lower = tweet_json["text"].lower()
#         # for each award in award dictionary
#         for host_word in host_dict:
#             # if the award is in the tweet
#             if host_word in tweet_lower:
#                 # split award on space to get last word
#                 sen1 = host_word.split()[-1]
#                 # splits data by tweet
#                 token_split = tweet.split()
#                 # splits tweets by word
#                 token_tweet = nltk.word_tokenize(tweet)
#                 # tags each token
#                 tagged_tweet = nltk.pos_tag(token_tweet)
#                 # splits lowercase tweets by word
#                 token_tweet_l = nltk.word_tokenize(tweet_lower)
#                 # if award is in lowercase tweet
#                 if sen1 in token_tweet_l:
#                     # find index of award in tokenized word (lowercase)
#                     indexof = token_tweet_l.index(sen1)
#
#                     temp_w = ""
#                     count = 1 + indexof
#
#                     # looking for award: winner or award - winner or award is winner
#                     if count < len(tagged_tweet) and (tagged_tweet[count][0] == ":" or tagged_tweet[ count][0] == "-" or tagged_tweet[count][0].lower() == "is"):
#                         count += 1
#                         while count < len(tagged_tweet):
#                             # find pronouns
#                             if (tagged_tweet[count][1] == "NNP" and tagged_tweet[count][0] != "–") or tagged_tweet[count][1] == "CD":
#                                 # if title is one word
#                                 if temp_w == "":
#                                     temp_w = tagged_tweet[count][0]
#                                 else:
#                                     # if title is multiple words
#                                     temp_w = temp_w + " " + tagged_tweet[count][0]
#                                 count += 1
#                             else:
#                                 break
#
#                     temp_w = temp_w.lower()
#
#                     if temp_w != "":
#                         if temp_w[0] == "'":
#                             temp_w = temp_w[1:]
#                         if temp_w in final_dict2:
#                             prev_count = final_dict2[temp_w]
#                             final_dict2.update({temp_w:prev_count+1})
#                         else:
#                             final_dict2.update({temp_w:1})
#
#                 nnp_list = [s[0] for s in tagged_tweet if s[1] == 'NNP' and s[0].lower() not in stop_dict]
#
#                 for nnp_word in nnp_list:
#                     if nnp_word in final_dict:
#                         prev_count = final_dict[nnp_word]
#                         final_dict.update({nnp_word:prev_count+1})
#                     else:
#                         final_dict.update({nnp_word:1})
#
#     if len(final_dict2) == 0:
#         sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
#         if len(sorted_list) >= 2:
#             award_winner_dict[tuple(award_data)] = (sorted_list[0][0],sorted_list[1][0])
#
#     else:
#         sorted_list = sorted(final_dict2.items(), key = itemgetter(1), reverse = True)
#         award_winner_dict[tuple(award_data)] = (sorted_list[0][0])
#     return award_winner_dict
#
#     # print(awards_and_winners)

def nominees(awards_and_winners):
    value = ""
    for keys,values in awards_and_winners.items():
        key = keys
        value = values

    checkfor = ["beat", "beats", "beating", "better than", "over", "upset", "liked", "wish", "robbed"]
    final_dict = {}
    final_dict2 = {}
    stop_dict = ["golden", "globes", "goldenglobes", "awards", "tweet",
                "tweets", "award", "rt", "@", "best", "motion", "actress",
                "actor", "drama", "picture","mtvnews","television","series",
                "foreign", "film","comedy","hbo","girlshbo", "pixar","everyone"]
    if awards_and_winners:
        for tweet_json in data:
            # gets the text part of a tweet data
            tweet = tweet_json["text"]
            # lowercases tweet text
            tweet_lower = tweet_json["text"].lower()




                #print(winner)
            # get_value = ""
            # for key, value in awards_and_winners.items():
            #     get_value = value
            # print (get_value)
            # if the award is in the tweet
            # print (tweet_lower)

            # if isinstance(get_value,str) and get_value in tweet_lower:
            for checkword in checkfor:
                if checkword in tweet_lower and value in tweet_lower:
                    # print(tweet)
                    # print ("hi hi")
                    # split award on space to get last word

                    # splits data by tweet
                    token_split = tweet.split()
                    # splits tweets by word
                    token_tweet = nltk.word_tokenize(tweet)
                    # tags each token
                    tagged_tweet = nltk.pos_tag(token_tweet)
                    # splits lowercase tweets by word
                    token_tweet_l = nltk.word_tokenize(tweet_lower)
                    # # if award is in lowercase tweet
                    # for important_word in important_list:
                    #
                    #     # print ("hello")
                    #     if tweet_lower.find(important_word) > -1:
                    #         # print ("found something")



                    if checkword in token_tweet_l:
                        indexof = token_tweet_l.index(checkword)

                        temp_w = ""
                        count = 0
                        # print(tagged_tweet)

                        if indexof+count < len(tagged_tweet):
                            count += 1
                            while indexof + count < len(tagged_tweet):
                                if (tagged_tweet[indexof + count][0] not in stop_dict and (tagged_tweet[indexof + count][1] == "NNP" or tagged_tweet[indexof + count][1] == "NN")) or tagged_tweet[indexof + count][1] == "CD":
                                    if temp_w == "":
                                        temp_w = tagged_tweet[indexof + count][0]
                                    else:
                                        temp_w = temp_w + " " + tagged_tweet[indexof + count][0]
                                    count += 1
                                else:
                                    break

                        temp_w = temp_w.lower()

                        if temp_w != "" and temp_w != value:
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
                            # for word in tagged_tweet:
                            #     if word[1] == "NNP" and word[0] not in stop_dict_nominees:
                            #         if word[0] in final_dict and word[0] not in stop_dict_nominees:
                            #             prev_count = final_dict[word[0]]
                            #             final_dict.update({word[0]:prev_count+1})
                            #         else:
                            #             final_dict.update({word[0]:1})

        #sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
        sorted_list = sorted(final_dict2.items(), key = itemgetter(1), reverse = True)
        # print(sorted_list)
        count = 0
        final_ret = {"nominees":[]}
        for i in sorted_list:
            if count == 4:
                break
            lisst = final_ret["nominees"]
            lisst.append(i[0])
            final_ret.update({"nominees":lisst})
            count += 1
        return {key:final_ret}
    return {"":[{"nominees":""}]}

for award in OFFICIAL_AWARDS_1315:
    awards_and_winners = winners(data,award)
    nominees1 = nominees(awards_and_winners)
    print(nominees1)
    # for item in nominees1:
    #     print(item)
