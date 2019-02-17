import host, humor, nom, winners
import sys, json

with open(sys.argv[1]) as json_file:
    data_final = json.load(json_file)

final_dict ={}

def format(data, award_data, awards_and_winners):
    final_dict["hosts"] = host.host(data)
    final_dict["award_data"] = {}
    for key in nom.nominees(data):
        final_dict["award_data"][key] = {"nominees": nom.nominees(awards_and_winners)[key], "winner": winners.winners(data, award_data)[key]}
        # final_dict["award_data"][key] = {"nominees": nominees(data)[key], "presenters": presenters(data)[key], "winner": winners(data)[key]}
    return final_dict

final = format(data_final, OFFICIAL_AWARDS_1315, winners(data,))
print (json.dumps(final))
