import host, humor, nom, winners, award_names, sentiment_bestdressed, sentiment_hosts, awards
from presenters import extract_presenters
import sys, json, re
from operator import itemgetter
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

###### ADD AWARD NAMES LIST HERE #########
"""
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
"""

# json format
def json_format(data, award_data):
	final_dict = {}

	final_dict["hosts"] = host.host(data)
	final_dict["award_data"] = {}

	winners_dict = winners.winners(data, award_data)
	nominees_dict = nom.nominees(data, award_data, winners_dict)
	presenters_dict = extract_presenters(data, award_data, winners_dict)

	for award in award_data:
		final_dict["award_data"][award] = {"nominees": nominees_dict.get(award), "presenters": presenters_dict.get(award), "winners": winners_dict.get(award)}

	# print(final_dict)
	return final_dict

def json_output_awards(data):
	award_dict = {}
	award_dict["awards"] = awards.awards(data)
	return award_dict

def json_jokes(data):
	humor_dict = {}
	humor_dict = humor.pres(data)
	return humor_dict

def json_sent_bestdressed(data):
	sent_bestdressed_dict = {}
	sent_bestdressed_dict = sentiment_bestdressed.pres(data)
	return sent_bestdressed_dict

def json_sent_hosts(data):
	sentiment_hosts_dict = {}
	sentiment_hosts_dict = sentiment_hosts.pres(data)
	return sentiment_hosts_dict

# human format
def human_format(json_format_result):
	print("\nHosts: " + str(", ".join(json_format_result["hosts"])) + "\n")
	for key in json_format_result["award_data"]:
		print ("Award: " + str(key))
		print ("Nominees: " + str(", ".join(json_format_result["award_data"][key]["nominees"])))
		print ("Presenters: " + str(", ".join(json_format_result["award_data"][key]["presenters"])))
		print ("Winner: " + str(json_format_result["award_data"][key]["winners"] + "\n"))
	return

def human_awards(json_format_result):
	for key in json_format_result:
		human_result = (str(key) + ": " + str(", ".join(json_format_result[key])))
	return human_result

def human_jokes(json_format_result):
	for key in json_format_result:
		human_result = (str(key) + ": " + str(", ".join(json_format_result[key])))
	return human_result

def human_sent_bestdressed(json_format_result):
	for key in json_format_result:
		human_result = (str(key) + ": " + str(", ".join(json_format_result[key])))
	return human_result

def human_sent_hosts(json_format_result):
	for key in json_format_result:
		human_result = (str(key) + ": " + str(", ".join(json_format_result[key])))
	return human_result

def final_output(gg_file, award_list, year):
	json_final = json_format(gg_file, award_list)
	awards_final = json_output_awards(gg_file)
	humor = json_jokes(gg_file)
	best_dressed = json_sent_bestdressed(gg_file)
	host_sentiment = json_sent_hosts(gg_file)

	human_final = human_format(json_final)
	human_awardz = human_awards(awards_final)
	human_jokez = human_jokes(humor)
	human_best_dressed = human_sent_bestdressed(best_dressed)
	human_sent_hostz = human_sent_hosts(host_sentiment)

	print (str(human_awardz) + "\n")
	print (str(human_jokez) + "\n")
	print (str(human_best_dressed) + "\n")
	print (str(human_sent_hostz) + "\n")

	print (json.dumps(json_final))
	print (json.dumps(awards_final))

	json_data = {
	"nominees, presenters, and winners for each award" : json_final,
	"generated awards" : awards_final
	}

	with open('results%s.json' % year, 'w') as outfile:
		json.dump(json_data, outfile)
