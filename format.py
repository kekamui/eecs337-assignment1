import host, humor, nom, winners, award_names, sentiment_bestdressed, sentiment_hosts
# from presenters import extract_presenters
import sys, json, re
from operator import itemgetter
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from collections import Counter

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

###### ADD AWARD NAMES LIST HERE #########

OFFICIAL_AWARDS_1315 = [
'cecil b. demille award',
'best motion picture - drama',
'best performance by an actress in a motion picture - drama',
'best performance by an actor in a motion picture - drama',
'best motion picture - comedy or musical',
'best performance by an actress in a motion picture - comedy or musical',
'best performance by an actor in a motion picture - comedy or musical',
'best animated feature film',
'best foreign language film',
'best performance by an actress in a supporting role in a motion picture',
 'best performance by an actor in a supporting role in a motion picture',
 'best director - motion picture', 'best screenplay - motion picture',
 'best original score - motion picture', 'best original song - motion picture',
 'best television series - drama',
 'best performance by an actress in a television series - drama',
 'best performance by an actor in a television series - drama',
 'best television series - comedy or musical',
 'best performance by an actress in a television series - comedy or musical',
 'best performance by an actor in a television series - comedy or musical',
 'best mini-series or motion picture made for television',
 'best performance by an actress in a mini-series or motion picture made for television',
 'best performance by an actor in a mini-series or motion picture made for television',
 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
  'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


with open(sys.argv[1]) as json_file:
    data_final = json.load(json_file)

if sys.argv[1] == "gg2013.json" or "gg2015.json":
    award_list = OFFICIAL_AWARDS_1315
else:
    award_list = OFFICIAL_AWARDS_1819

final_dict = {}
award_dict = {}
humor_dict = {}
sent_bestdressed_dict = {}
sent_hosts_dict = {}

# json format
def json_format(data, award_data):
    final_dict["hosts"] = host.host(data)
    final_dict["award_data"] = {}

    winners_dict = winners.winners(data, award_data)
    nominees_dict = nom.nominees(data, award_data, winners_dict)
    # presenters_dict = extract_presenters(data, award_data)

    for award in award_list:
        #final_dict["award_data"][award] = {"presenters": presenters.extract_presenters(data, award_data)[award]}
        #final_dict["award_data"][award] = {"nominees": nom.nominees(data, award_data)[award], "presenters": presenters.extract_presenters(data, award_data)[award], "winner": winners.winners(data, award_data)[award]}
        final_dict["award_data"][award] = {"nominees": nominees_dict[award], "winner": winners_dict[award]}
    return final_dict

def json_output_awards(data):
    award_dict["awards"] = awards.awards(data)
    return award_dict

def json_jokes(data):
    humor_dict = humor.pres(data)
    return humor_dict

def json_sent_bestdressed(data):
    sent_bestdressed_dict = sentiment_bestdressed.pres(data)
    return sent_bestdressed_dict

def json_sent_hosts(data):
    sentiment_hosts_dict = sentiment_hosts.pres(data)
    return sentiment_hosts_dict

# human format
def human_format(json_format_result):
    for key in json_format_result:
        human_result = (str(key) + ": " + str(", ".join(json_format_result[key])))
    return human_result

def human_awards(json_format_result):
    for key in json_format_result:
        human_result = (str(key) + ": " + str(", ".join(json_format_result[key])))
    return human_result

def human_jokes(json_format_result):
    for key in json_format_result:
        human_result (str(key) + ": " + str(", ".join(json_format_result[key])))
    return human_result

def human_sent_bestdressed(json_format_result):
    for key in json_format_result:
        human_result (str(key) + ": " + str(", ".join(json_format_result[key])))
    return human_result

def human_sent_hosts(json_format_result):
    for key in json_format_result:
        human_result (str(key) + ": " + str(", ".join(json_format_result[key])))
    return human_result


# final = json_fordmat(data_final, award_list)
# awards = json_output_awards(data_final)
humor = json_jokes(data_final)
best_dressed = json_sent_bestdressed(data_final)
host_sentiment = json_sent_hosts(data_final)

# human_final = human_format(final)
# human_awards = human_format(awards)
human_jokes = human_format(humor)
human_best_dressed = human_format(best_dressed)
human_sent_hosts = human_format(host_sentiment)

# print (json.dumps(final))
# print (json.dumps(awards))
# print (json.dumps(humor))
# print (json.dumps(best_dressed))
# print (json.dumps(host_sentiment))

# print (human_final)
# print (human_awards)
print (human_jokes)
print (human_best_dressed)
print (human_sent_hosts)
