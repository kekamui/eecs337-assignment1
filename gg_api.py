'''Version 0.35'''
import results_assembler, sys, json

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    with open('results%s.json' % year, 'r') as f:
                result_file = json.load(f)

    hosts = result_file["nominees, presenters, and winners for each award"]["hosts"]

    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    with open('results%s.json' % year, 'r') as f:
                result_file = json.load(f)

    awards = result_file["generated awards"]["awards"]

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    with open('results%s.json' % year, 'r') as f:
                result_file = json.load(f)


    npw_dict = result_file["nominees, presenters, and winners for each award"]["award_data"]
    nominees = {}
    for award_key in npw_dict.keys():
        nominees[award_key] = npw_dict[award_key]["nominees"]

    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    with open('results%s.json' % year, 'r') as f:
                result_file = json.load(f)

    npw_dict = result_file["nominees, presenters, and winners for each award"]["award_data"]
    winners = {}
    for award_key in npw_dict.keys():
       winners[award_key] = npw_dict[award_key]["winners"]

    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    with open('results%s.json' % year, 'r') as f:
                result_file = json.load(f)
    
    npw_dict = result_file["nominees, presenters, and winners for each award"]["award_data"]
    presenters = {}
    for award_key in npw_dict.keys():
       presenters[award_key] = npw_dict[award_key]["presenters"]

    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here

    year_list = []

    for y in sys.argv[1:]:
        year_list.append(y)

    #print(year_list)

    for year in year_list:
        print("\nProcessing year " + year + "\n")
        if  year == "2013" or year == "2015":
            print("Fetching OFFICIAL_AWARDS_1315 awards list\n")
            award_list = OFFICIAL_AWARDS_1315
        else:
            print("Fetching OFFICIAL_AWARDS_1819 awards list\n")
            award_list = OFFICIAL_AWARDS_1819

        with open('gg%s.json' % year, 'r') as f:
                gg_file = json.load(f)
        print("Successfully opened corpus file\n")

        results_assembler.final_output(gg_file,award_list,year)
        print("\nFinished processing year " + year + "\n")

    return

if __name__ == '__main__':
    main()
