import nltk
import json
from nltk.probability import FreqDist
#from nltk.tag.stanford import StanfordNERTagger

file_data = open("gg2013.json")

data = json.load(file_data)

'''
DATA FORMAT
text: str; Text of tweet, including hashtags
user: tuple (2 values)
    screen_name: str; Username
    id: int; UserID
id: int; ID number of tweet
timestamp_ms: int; Timestamp in milliseconds?
'''

text_data = []

stop_words = ['the', 'of', 'and', 'a', 'in', 'to', 'it', 'is', 'was', 'i', 'I', 'for', 'you', 'he', 'be', 'with', 'on', 'that', 'by', 'at', 'are', 'not', 'this', 'but', "'s", 'they', 'his', 'from', 'had', 'she', 'which', 'or', 'we', 'an', "n't", 'were', 'been', 'have', 'their', 'has', 'would', 'what', 'will', 'there', 'if', 'can', 'all', 'her', 'as', 'who', 'do', 'one', 'said', 'them', 'some', 'could', 'him', 'into', 'its', 'then', 'two', 'when', 'up', 'time', 'my', 'out', 'so', 'did', 'about', 'your', 'now', 'me', 'no', 'more', 'other', 'just', 'these', 'also', 'people', 'any', 'first', 'only', 'new', 'may', 'very', 'should', 'like', 'than', 'how', 'well', 'way', 'our', 'between', 'years', 'er', 'many', 'those', "'ve", 'being', 'because', "'re"]

join_char = " "
punctuation = ['.', '!', '?', ';', ':', '#', '@']
award_words = ["Best"]
"""
MIGHT NEED TO ADD "Song", "Video", "Record", "Album" FOR MUSIC AWARDS
"""
prepositions = ['in', 'a', 'an', 'or', 'of', 'the', 'for']
dash = ["-"]
"""
snert = StanfordNERTagger('C:/Program Files (x86)/Python3/Lib/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                          'C:/Program Files (x86)/Python3/Lib/stanford-ner-2018-10-16/stanford-ner.jar',
                          encoding='utf-8')
"""
for tweet in data:
    tokenized_text = nltk.word_tokenize(tweet['text'])
    final_text = []
    award_flag = False
    lowercase_tracker = 0
    non_award_words = 0
    dash_tracker = 0
    for word in tokenized_text:
        if word in award_words:
            award_flag = True
        if award_flag:
            #person_checker = snert.tag(word)
            if word in punctuation: # or person_checker[1] == 'PERSON':
                award_flag = False
                break
            if word[0].isupper():
                final_text.append(word)
                lowercase_tracker = 0
                non_award_words = 0
            elif word in prepositions:
                final_text.append(word)
                lowercase_tracker += 1
            elif word in dash:
                final_text.append(word)
                lowercase_tracker += 1
                non_award_words += 1
                dash_tracker += 1
            else:
                final_text.append(word)
                lowercase_tracker += 1
                non_award_words += 1

            if non_award_words > 1 or dash_tracker > 1:
                award_flag = False
                lc_index = -1 * lowercase_tracker
                del final_text[lc_index:]
                lowercase_tracker = 0
                non_award_words = 0
                dash_tracker = 0
            """
            if word[0].isupper():
                final_text.append(word)
            else:
                final_text.append(word)
                lowercase_tracker += 1
            if lowercase_tracker > 3:
                award_flag = False
                lowercase_tracker = 0
                del final_text[-3:]
            """

        """
        if word not in stop_words:
            clean_text.append(word)
        """
    if len(final_text) > 1:
        award_name = join_char.join(final_text)
        text_data.append(award_name)

with open('gg2013output.json', 'w') as output_file:
    json.dump(text_data, output_file)

freq_dist = FreqDist(text_data)

awards = [w for w, c in freq_dist.most_common(20)]

print(awards)