import nltk
import json
from nltk.probability import FreqDist
#import spacy

def awards(file_name):

    # nlp = spacy.load('en_core_web_sm')

    #file_data = open(file_name)

    #data = json.load(file_data)

    # Data from each tweet will be added to this array after that tweet is processed
    text_data = []

    # Good list of stop words but never currently utilized
    stop_words = ['the', 'of', 'and', 'a', 'in', 'to', 'it', 'is', 'was', 'i', 'I', 'for', 'you', 'he', 'be', 'with', 'on', 'that', 'by', 'at', 'are', 'not', 'this', 'but', "'s", 'they', 'his', 'from', 'had', 'she', 'which', 'or', 'we', 'an', "n't", 'were', 'been', 'have', 'their', 'has', 'would', 'what', 'will', 'there', 'if', 'can', 'all', 'her', 'as', 'who', 'do', 'one', 'said', 'them', 'some', 'could', 'him', 'into', 'its', 'then', 'two', 'when', 'up', 'time', 'my', 'out', 'so', 'did', 'about', 'your', 'now', 'me', 'no', 'more', 'other', 'just', 'these', 'also', 'people', 'any', 'first', 'only', 'new', 'may', 'very', 'should', 'like', 'than', 'how', 'well', 'way', 'our', 'between', 'years', 'er', 'many', 'those', "'ve", 'being', 'because', "'re"]

    join_char = " "
    punctuation = ['.', '!', '?', ';', ':', '#', '@', '(']
    award_words = ["Best"] # MIGHT NEED TO ADD "Song", "Video", "Record", "Album" TO award_words FOR MUSIC AWARDS
    prepositions = ['in', 'a', 'an', 'or', 'of', 'the', 'for']


    for tweet in data:
        tokenized_text = nltk.word_tokenize(tweet['text'])
        if award_words[0] in tokenized_text:
            final_text = []
            text_cache = []
            award_flag = False
            lowercase_tracker = 0
            non_award_words = 0
            dash_tracker = 0
            for word in tokenized_text:
                # If word in award_words, set flag to True to let loop know the current words are relevant to an award phrase
                if word in award_words:
                    award_flag = True
                if award_flag:
                    # If word is punctuation, stop
                    if word in punctuation:
                        award_flag = False
                        break
                    if word[0].isupper(): # If word is uppercase, most likely still part of the phrase
                        if text_cache:
                            for tkn in text_cache:
                                final_text.append(tkn)
                        final_text.append(word)
                        text_cache = []
                        lowercase_tracker = 0
                        non_award_words = 0
                    elif word in prepositions: # If word is an the (acceptable) prepositions list, continue and track
                        text_cache.append(word)
                        lowercase_tracker += 1
                    elif word == '-': # If word is a dash, continue and track
                        text_cache.append(word)
                        lowercase_tracker += 1
                        non_award_words += 1
                        dash_tracker += 1
                    else: # Else continue but track
                        text_cache.append(word)
                        lowercase_tracker += 1
                        non_award_words += 1

                    # If the number of words that indicate that the current phrase is non part of an award name or number of
                    # dashes exceeds 1, stop appending and delete the non award words from the phrase
                    if non_award_words > 1 or dash_tracker > 1:
                        award_flag = False
                        lowercase_tracker = 0
                        non_award_words = 0
                        dash_tracker = 0
            # If the length of the phrase is greater than 1, join the tokens of the phrase together and add to text_data
            if len(final_text) > 1:
                award_name = join_char.join(final_text)
                text_data.append(award_name)

    # Write text_data to gg20??output.json
    #with open('gg2013output.json', 'w') as output_file:
    #    json.dump(text_data, output_file)

    # Find frequency distribution of text_data
    freq_dist = FreqDist(text_data)

    # Find 20 most common phrases
    awards = [w for w, c in freq_dist.most_common(20)]

    # print(awards)

    return awards
