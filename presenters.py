import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import os
import json
import re
from nltk.probability import FreqDist
import pprint
import winners

presenter_words = ["presenter", "present", "announc"]
award_words = ["best"]
exception_words = ['host']
text_data=[]
stop_words = ['win', 'wins', 'best', 'the', 'of', 'and', 'a', 'in', 'to', 'it', 'is', 'was', 'i', 'I', 'for', 'you', 'he', 'be', 'with', 'on', 'that', 'by', 'at', 'are', 'not', 'this', 'but', "'s", 'they', 'his', 'from', 'had', 'she', 'which', 'or', 'we', 'an', "n't", 'were', 'been', 'have', 'their', 'has', 'would', 'what', 'will', 'there', 'if', 'can', 'all', 'her', 'as', 'who', 'do', 'one', 'said', 'them', 'some', 'could', 'him', 'into', 'its', 'then', 'two', 'when', 'up', 'time', 'my', 'out', 'so', 'did', 'about', 'your', 'now', 'me', 'no', 'more', 'other', 'just', 'these', 'also', 'people', 'any', 'first', 'only', 'new', 'may', 'very', 'should', 'like', 'than', 'how', 'well', 'way', 'our', 'between', 'years', 'er', 'many', 'those', "'ve", 'being', 'because', "'re"]



# winnerslist = [winners.winners(data, award) for award in OFFICIAL_AWARDS_1315]
#
# # pprint.pprint(winnerslist)
#
# winnersonlylist = []
#
#
#
# for winner in winnerslist:
# 	for key,value in winner.items():
# 		winnersonlylist.append(value)
#
# awardWinnerPresenterList=[]
#
# for winnerdict in winnerslist:
# 	for award,winner in winnerdict.items():
# 		awardWinnerPresenterList.append({'award':award, 'winner': winner, 'presenters':[]})

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

def isPresenterTweet(tweet): ##check if sentence structure is 'X present/introduce/announce' or 'X is presenter'
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

def extract_subj_entities(doc): ##extract names of people that come before the verb
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

def WinnerisinTwt(twt,winnersonlylist):
	for winner in winnersonlylist:
		if re.search(winner, twt , re.IGNORECASE):
			return True,winner
	return False,0

def AwardisinTwt(twt):
	for award in OFFICIAL_AWARDS_1315:
		if re.search(award, twt, re.IGNORECASE):
			return True, award
	return False,0

def addPresenterByWinner(presenter,winner,awardWinnerPresenterList):
	for awp_dict in awardWinnerPresenterList:
		if awp_dict["winner"] == winner:
			if not re.match(presenter, winner,re.IGNORECASE): #if presenter and winner is not same person
				awp_dict["presenters"].append(presenter)

def addPresenterByAward(presenter,award,awardWinnerPresenterList):
	for awp_dict in awardWinnerPresenterList:
		if awp_dict["award"] == award:
			awp_dict["presenters"].append(presenter)

#######main

#twts = read_tweets()
def extract_presenters(data):
	winnerslist = [winners.winners(data, award) for award in OFFICIAL_AWARDS_1315]

	# pprint.pprint(winnerslist)

	winnersonlylist = []

	for winner in winnerslist:
		for key, value in winner.items():
			winnersonlylist.append(value)

	awardWinnerPresenterList = []

	for winnerdict in winnerslist:
		for award, winner in winnerdict.items():
			awardWinnerPresenterList.append({'award': award, 'winner': winner, 'presenters': []})


	# print([(X.text, X.label_) for X in doc2.ents])
	# print(twts[:10])

	for tweet in data:
		twt=tweet[u'text']
		for presenter_word in presenter_words:
			if presenter_word in twt and 'RT' not in twt:
				winnerRes = WinnerisinTwt(twt,winnersonlylist)
				hasWinner = winnerRes[0]
				awardRes = AwardisinTwt(twt)
				hasAward = awardRes[0]
				twtdoc = nlp(twt)
				for X in twtdoc.ents:
					if X.label_ == 'PERSON':
						name = X.text
						# print('-------')
						# print(name)
						name=remove_punctuations(name)
						name=remove_stopwords(name)
						name=get_name_portion(name)
						# print(name)
						if isFullName(name):
							text_data.append(name)
							if hasAward:
								#print('---award in twt', awardRes[1])
								#print(twt)
								addPresenterByAward(name,awardRes[1],awardWinnerPresenterList)
							elif hasWinner:
								#print('----winner in twt : ', winnerRes[1])
								#print(twt)
								addPresenterByWinner(name,winnerRes[1],awardWinnerPresenterList)

				break

	freq_dist = FreqDist(text_data)

	presenters = [(w,c) for w, c in freq_dist.most_common(70)]
	pprint.pprint(presenters)

	res_dict = {}
	###make presenters into FreqDist
	for awardWinnerPresenterDict in awardWinnerPresenterList:
		presenterfreqdist = FreqDist(awardWinnerPresenterDict["presenters"])
		res_dict[awardWinnerPresenterDict["award"]]=[p for p,c in presenterfreqdist.most_common(2)]


	###return
	return res_dict
