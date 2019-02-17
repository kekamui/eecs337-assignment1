import nltk
import re
import json
from operator import itemgetter
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

with open('gg2013.json') as json_file:
    data = json.load(json_file)

def host(file_name):

<<<<<<< HEAD
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
	    # print({"hosts":[sorted_list[0][0].lower(),sorted_list[1][0].lower()]})
	    return {"hosts":[sorted_list[0][0].lower(),sorted_list[1][0].lower()]}

	else:
	    sorted_list = sorted(final_dict.items(), key = itemgetter(1), reverse = True)
	    # print(sorted_list)
	    # print({"hosts":sorted_list[0][0].lower() + " " + sorted_list[1][0].lower()})
	    return {"hosts":sorted_list[0][0].lower() + " " + sorted_list[1][0].lower()}
=======
    host_dict = ["host", "hosting", "hosts"]
    stop_dict = ["golden", "globes", "goldenglobes", "awards", "tweet", "tweets", "award", "rt", "@"]

    single_data = [
    {
    "text":"The only thing wrong with Ricky hosting the #goldenglobes is there is not enough Ricky!"
    },
    {"text":"I'm watching Golden Globe Awards with #Shazam. Ricky Gervais is killing it as hosts! #funny #GoldenGlobes"},
    {"text":"Who else is loving Ricky Gervais hosting the #GoldenGlobes?"},
    {"text":"Can Ricky Gervais just host everything forever and ever from now on?"},
    {"text":"Ricky Gervais need to host EVERY awards show, birthday party and doctors appt I participate in from now on"},
    {"text":"Ricky Gervais hosting the Golden Globes... Funny ass bitches"},
    {"text":"Tina Fey and Amy Poehler hosting the Golden Globes... Funny ass bitches"},
    {"text":"Tina Fey and Amy Poehler hosting the Golden Globes... Funny ass bitches"}

    ]

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
                    nnp_word = nnp_word.lower()
                    if nnp_word in final_dict:
                        prev_count = final_dict[nnp_word]
                        final_dict.update({nnp_word:prev_count+1})
                    else:
                        final_dict.update({nnp_word:1})


    showcount = Counter()
    for item in two_host_list:
        showcount.update(item)

        sorted_list = sorted(showcount.items(), key = itemgetter(1), reverse = True)
        sorted_final_dict = sorted(final_dict.items(), key = itemgetter(1), reverse = True)

        most_appeared_double_name = sorted_list[0][0].split()
        check_appeared_double_name =  most_appeared_double_name[0]

        if len(sorted_list) > 0 and not(final_dict[check_appeared_double_name] < sorted_final_dict[0][1]):
            print({"hosts":[sorted_list[0][0].lower(),sorted_list[1][0].lower()]})
            return {"hosts":[sorted_list[0][0].lower(),sorted_list[1][0].lower()]}

        else:
            #eeeee
            print({"hosts":sorted_final_dict[0][0].lower() + " " + sorted_final_dict[1][0].lower()})
            return {"hosts":sorted_final_dict[0][0].lower() + " " + sorted_final_dict[1][0].lower()}

host(data)
>>>>>>> ddfe5cb6c18c5b5b233e4f9b933eff3a7547b857
