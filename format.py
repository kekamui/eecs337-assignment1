import host, humor, nom, winners
import sys, json

with open(sys.argv[1]) as json_file:
    data_final = json.load(json_file)

final_dict ={}

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


def format(data, award_data, awards_and_winners):
    final_dict["hosts"] = host.host(data)
    final_dict["award_data"] = {}
    for key in nom.nominees(data):
        final_dict["award_data"][key] = {"nominees": nom.nominees(awards_and_winners)[key], "winner": winners.winners(data, award_data)[key]}
        # final_dict["award_data"][key] = {"nominees": nominees(data)[key], "presenters": presenters(data)[key], "winner": winners(data)[key]}
    return final_dict

final = format(data_final, OFFICIAL_AWARDS_1315, winners(data,))
print (json.dumps(final))
