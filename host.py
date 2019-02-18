import nltk
import re
import json
from operator import itemgetter
from collections import Counter

def host(data):

	host_dict = ["host", "hosting", "hosts"]
	stop_dict = ["golden", "globes", "goldenglobes", "awards", "tweet", "tweets", "award", "rt", "@"]

	final_dict = {}
	two_host_list = []
	two_host_dict = {}

	for tweet_json in data:
	    tweet = tweet_json["text"]
	    tweet_lower = tweet_json["text"].lower()
	    for host_word in host_dict:
	        if host_word in tweet_lower:
	            # print(tweet)
	            token_tweet = nltk.word_tokenize(tweet)
	            tagged_tweet = nltk.pos_tag(token_tweet)
	            for w in range(len(tagged_tweet)):
	                if w < len(tagged_tweet) - 4:
	                    if tagged_tweet[w][1] == "NNP" and tagged_tweet[w+1][1] == "NNP" and tagged_tweet[w+2][1] == "CC" and tagged_tweet[w+3][1] == "NNP" and tagged_tweet[w+4][1] == "NNP":
	                        two_host_list.append([tagged_tweet[w][0].lower() + " " + tagged_tweet[w+1][0].lower(), tagged_tweet[w+3][0].lower() + " " + tagged_tweet[w+4][0].lower()])


	            nnp_list = [s[0] for s in tagged_tweet if s[1] == 'NNP' and s[0].lower() not in stop_dict]
	            for nnp_word in nnp_list:
	                if nnp_word in final_dict:
	                    prev_count = final_dict[nnp_word]
	                    final_dict.update({nnp_word:prev_count+1})
	                else:
	                    final_dict.update({nnp_word:1})


	showcount = Counter()
	for item in two_host_list:
	    showcount.update(item)

	sorted_list = sorted(showcount.items(), key = itemgetter(1), reverse = True)
	if sorted_list[0][1] - sorted_list[1][1] < 100:
	    #print({"hosts":[sorted_list[0][0].lower(),sorted_list[1][0].lower()]})
	    return [sorted_list[0][0].lower(),sorted_list[1][0].lower()]

	else:
	    sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
	    #print(sorted_list)
	    #print({"hosts":sorted_list[0][0].lower() + " " + sorted_list[1][0].lower()})
	    return [sorted_list[0][0].lower() + " " + sorted_list[1][0].lower()]

# print(host(data))
