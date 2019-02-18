import host, humor, nom, winners, award_names
import sys, json, re
from operator import itemgetter
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from collections import Counter

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

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

if sys.argv[1] == "gg2013.json":
    award_list = OFFICIAL_AWARDS_1315
elif sys.argv[1] == "gg2015.json":
    award_list = OFFICIAL_AWARDS_1819
else:
    award_list = OFFICIAL_AWARDS_1315

######### MODIFY IF STATEMENT HERE TO TEST OTHER GOLDEN GLOBE YEARS ##########
# if sys.argv[1] == ".json":
#     award_list =


final_dict = {}
award_dict = {}

def format(data, award_data):
    final_dict["hosts"] = host.host(data)
    final_dict["award_data"] = {}

    print(final_dict)

    winners_dict = winners.winners(data, award_data)
    nominees_dict = nom.nominees(data, award_data, winners_dict)

    print("Finished compile")

    for award in award_list:
        final_dict["award_data"][award] = nominees_dict[award] #winners_dict[award]
        print(final_dict)
        # , "winner":
        # final_dict["award_data"][key] = {"nominees": nominees(data)[key], "presenters": presenters(data)[key], "winner": winners(data)[key]}
    return final_dict

# def output_awards(data):
#     award_dict["awards"] = awards.awards(data)

final = format(data_final, award_list)
#awards = output_awards(data)

print (json.dumps(final))
print (json.dumps(output_awards))
