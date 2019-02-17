import host, humor, nom, winners
import sys, json

with open(sys.argv[1]) as json_file:
    data = json.load(json_file)

final_dict ={}

def format(data):
    final_dict["hosts"] = host(data)
    final_dict["award_data"] = {}
    for key in nominees(data):
        final_dict["award_data"][key] = {"nominees": nom(data)[key], "winner": winners(data)[key]}
        # final_dict["award_data"][key] = {"nominees": nominees(data)[key], "presenters": presenters(data)[key], "winner": winners(data)[key]}
    return final_dict

final = format(data)
print (json.dumps(final))
