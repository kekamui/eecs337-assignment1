import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import os
import json
import re
from nltk.probability import FreqDist
import pprint


JSONPATH='gg2013.json'

pres_regex=r'(presented)(by)([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)'
pres_keyword='(pres|intro|announce|gave)'

name_special_regex = r'([A-Za-z]+\s[A-Z][a-z][A-Za-z]+)'

presenter_words = ["presenter", "present", "introduc", "announc"]
award_words = ["best"]
exception_words = ['host'] #todo: words to exclude?
text_data=[]

stop_words = ['the', 'of', 'and', 'a', 'in', 'to', 'it', 'is', 'was', 'i', 'I', 'for', 'you', 'he', 'be', 'with', 'on', 'that', 'by', 'at', 'are', 'not', 'this', 'but', "'s", 'they', 'his', 'from', 'had', 'she', 'which', 'or', 'we', 'an', "n't", 'were', 'been', 'have', 'their', 'has', 'would', 'what', 'will', 'there', 'if', 'can', 'all', 'her', 'as', 'who', 'do', 'one', 'said', 'them', 'some', 'could', 'him', 'into', 'its', 'then', 'two', 'when', 'up', 'time', 'my', 'out', 'so', 'did', 'about', 'your', 'now', 'me', 'no', 'more', 'other', 'just', 'these', 'also', 'people', 'any', 'first', 'only', 'new', 'may', 'very', 'should', 'like', 'than', 'how', 'well', 'way', 'our', 'between', 'years', 'er', 'many', 'those', "'ve", 'being', 'because', "'re"]
def read_tweets():
	cwd = os.getcwd()
	path = cwd + '/' + JSONPATH
	f = open(path)

	tweets_json = json.load(f)
	tweets = []
	for tweet in tweets_json:
		tweets.append(tweet['text'])
	return tweets

def remove_stopwords(text):
	for stop_word in stop_words:
		text = re.sub(r'\b' + stop_word + r'\b\s+', "", text)
	return text


def remove_punctuations(text):
	text = re.sub(r'\'s', "", text)
	return text

def get_name_portion(text):
	splitted = text.split(" ")
	#print(splitted)
	res = ""
	offset = -3
	if len(splitted) == 1:
		offset = -1
	elif len(splitted) == 2:
		offset = -2
	else:
		offset = -3

	indexcount=1
	for word in reversed(splitted):

		if word: #if word is empty, skip
			firstletter = word[0]
			if indexcount >= 3 and firstletter.lower() == firstletter:
				break
			else:
				if indexcount==1:
					res = word
				else:
					res = word + " " + res
				indexcount += 1

		# if firstletter.lower() != firstletter: #if first letter is capitalized

	return res

def search_tweet(queries,exclude):
	twts = read_tweets()
	for twt in twts:
		for query in queries:
			if query not in twt:
				break
		else:
			if exclude not in twt:
				print(twt)




nlp = en_core_web_sm.load()
doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
doc2 = nlp('Hello my name is Jimmy')


# print(get_name_portion("hi Jimmy Yook"))
# def isPresenterTweet(tweet):
# 	doc=nlp(tweet)
# 	for idx, tok in enumerate(doc):
# 		if tok.pos_ == "VERB" and tok.lemma_ in ("present","introduce","announce"):
# 			print(tweet)
# 			return True
# 	return False

def isPresenterTweet(tweet):
	doc=nlp(tweet)
	for idx, tok in enumerate(doc):
		if tok.pos_ == "VERB":
			if tok.lemma_ in ("present","introduce","announce"):
				return True
			if tok.lemma_ == "be" and "presenter" in tweet:
				# print("be verb case")
				# print(tweet)
				return True
	return False

def extract_nsubj(tweet):
	doc = nlp(tweet)
	sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj")]
	return sub_toks

def extract_subj_entities(doc):
	ents=list(doc.ents)
	person_ents = [ent for ent in ents if ent.label_=='PERSON']
	#print(person_ents)
	entityListCurrIndex=0
	subjEnts=[]
	if person_ents:
		for tok in doc:
			if tok.pos_=="VERB" or entityListCurrIndex == len(person_ents):
				return subjEnts
			else:
				#print(tok)
				#print(entityListCurrIndex)
				if tok.text in person_ents[entityListCurrIndex].text:
					subjEnts.append(person_ents[entityListCurrIndex].text)
					entityListCurrIndex+=1
	return subjEnts

def isFullName(name):
	if 'golden' in name or 'globes' in name:
		return False
	pattern = r'^[A-Z]\w+(?:\s[A-Z]\w+?)?\s(?:[A-Z]\w+?)?$'
	if re.match(pattern,name):
		return True
	return False
#######main
def extract_presenters():

	twts = read_tweets()
	# print([(X.text, X.label_) for X in doc2.ents])
	# print(twts[:10])

	for twt in twts:
		for presenter_word in presenter_words:
			if presenter_word in twt and 'RT' not in twt:
				if isPresenterTweet(twt):
					if "Best" in twt:
						print(twt)
				#if True:
				#print('--------')
					subjects = extract_nsubj(twt)
					#print(twt)
					twtdoc = nlp(twt)
					subjnames=extract_subj_entities(twtdoc)
					for subjname in subjnames:
						name = subjname
						# print('-------')
						# print(name)
						name=remove_punctuations(name)
						name=remove_stopwords(name)
						name=get_name_portion(name)
						# print(name)
						if isFullName(name):
							text_data.append(name)

					#text_data.extend(subjnames)
					# for X in subjnames:
					# 	if '@' not in X.text and len(X.text.split(" "))>1:
					# 	#todo: excluded one-word names for now. maybe find a way to add them to the count if match with the full names?
					# 	#todo: also, find a way to merge typos?
					# 		name=X.text
					# 		print('-------')
					# 		print(name)
					# 		name=remove_punctuations(name)
					# 		name=remove_stopwords(name)
					# 		name=get_name_portion(name)
					# 		print(name)

				break

	freq_dist = FreqDist(text_data)

	presenters = [(w,c) for w, c in freq_dist.most_common(70)]
	pprint.pprint(presenters)

extract_presenters()
#print(text_data)
#search_tweet(["Brolin"], "RT")





#if "best is in
