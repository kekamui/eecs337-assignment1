import nltk
import re
import json
from winners import winners
from operator import itemgetter
from nltk.tokenize import TweetTokenizer

def nominees_helper(awards_and_winners,data):
    important_list = ["beat", "but", "better", "contenders", "contender", "over", "upset", "lost", "liked", "wish", "doesn't win", "please", "robbed"]

    stop_dict_nominees = ["golden", "globes", "goldenglobes", "awards", "tweet",
                "tweets", "award", "rt", "@", "best", "motion", "actress",
                "actor", "drama", "picture","mtvnews","television","series",
                "foreign", "film","comedy","hbo","girlshbo", "pixar", "best", "actress", "actor"]

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

        sorted_list = sorted(final_dict2.items(), key = itemgetter(1), reverse = True)
        #print(sorted_list)
        
        nom_list = []
        count = 0
        final_ret = []
        for i in sorted_list:
            if count == 4:
                break
            nom_list.append(i[0])
            count += 1
        """
        sl_len = len(sorted_list)
        if sl_len > 4:
        	sl_len = 3
        else:
        	sl_len = sl_len - 1
        nom_list = sorted_list[:sl_len]
        """
        #print(nom_list)
        return {key:nom_list}
    return {key:[]}

def nominees(data, award_list, winners_dict):
	nom_dict = {}

	for award in award_list:
		if award in winners_dict:
		    award_winner_pair = {award:winners_dict[award]}

		    list_of_nominees = nominees_helper(award_winner_pair,data)
		    # print(list_of_nominees)
		    nom_dict.update(list_of_nominees)
		else:
			nom_dict.update({award:[]})

	return(nom_dict)
