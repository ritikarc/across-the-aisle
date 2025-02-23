# Across the Aisle (across-the-aisle)
# July 2019

import nltk
import os
import re
import sys
import json
import requests

from newspaper import Article
from nltk.stem import PorterStemmer
from pprint import pprint
from BingNewsSearchAPI import bingsearchAPI
ps = PorterStemmer()

# initializing Azure Subscription
key_phrase_dict = {}
subscription_key = "090d7671c3b34482b8a2d2ccbc5d4dd2"
api_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.1/"
keyphrase_url = api_base_url + "keyPhrases"

# returns category of article
def topic(titleWords, articlePhrases) :

	articlePhrases = " ".join(articlePhrases)
	currKey = ""
	currVal = -1

	weights = {}

	# key = category
	for key, value in titleWords.items() :
		count = 0
		# key = title key words, value2 = 0
		for key2, value2 in value.items() :

			if key2 in articlePhrases :
				count += 1

		lenDict = len(value)

		#avoid division by 0 error
		if lenDict == 0 :
			lenDict = 1

		weights[key] = count/lenDict
		# print(key)
		# print(lenDict)
		# print("~~~~~~~~")

	for key, value in weights.items() :
		if value > currVal :
			currVal = value
			currKey = key

	# print(currKey)
	return currKey


# puts key words from files into a dictionary (recevied from Azure Text Analytics API)
def dictionary(folderName) :
	folderPath = os.path.abspath(folderName)
	wordsDict = {} # dictionary of dictionaries (outer key: topics, inner key: far left, far right, right, center, left)
	topicDict = {} # dictionary (key: categories, value: key words for a particular category)
	count = 0

	for tempFile in os.listdir(folderPath) :
		print(tempFile)
		pathName = os.path.join(folderPath, tempFile)
		keyWords = []
		currCategory = ""
		#
		with open(pathName, 'r', encoding='utf-8-sig') as json_file:
			data  = json.load(json_file)

			#key = articleNum
			for key, value in data.items() :
				# get category ex. 'Abortion'
				if value['category'] not in wordsDict.keys() :
					wordsDict[value['category']] = {}
					
				currCategory = value['category']

				# create nested dictionary for title key words
				if currCategory not in topicDict.keys() :
					topicDict[currCategory] = {}

				for word in value['title'] :
					if word not in topicDict[currCategory].keys() :
						stemmedWord = ps.stem(word)
						topicDict[currCategory][stemmedWord] = 0

				# create nested dictionary for text key words
				if tempFile not in wordsDict[currCategory].keys() :
					wordsDict[currCategory][tempFile] = {}

				for word in value['text'] :
					if word not in wordsDict[currCategory][tempFile].keys() :
						stemmedWord = ps.stem(word)
						wordsDict[currCategory][tempFile][stemmedWord] = 0
				

	return wordsDict, topicDict

# input: article URL, output: string (says political view of article) and list of key words from article
def interpretPage(url) :

	# Code to get training data
	#keyWords, titleWords = dictionary("test")

	# with open('keyWords.txt', 'w') as json_file :
	# 	json.dump(keyWords, json_file)

	# with open('titleWords.txt', 'w') as json_file :
	# 	json.dump(titleWords, json_file)

	with open('titleWords.txt', 'r', encoding='utf-8-sig') as json_file:
		titleWords = json.load(json_file)

	with open('keyWords.txt', 'r', encoding='utf-8-sig') as json_file:
		keyWords = json.load(json_file)

	# article that will be rated as Far Left, Left, Center, Right, or Far Right
	# url = sys.argv[1]
	#url = "https://www.foxnews.com/politics/trump-abortion-tax-dollar-planned-parenthood"
	art = Article(url, language="en")
	art.download()
	art.parse() 
	article = art.text

	# API
	if len(article) > 5120 :
		article = article[0:5120]

	documents = {"documents": [
		{"id": "text", "language": "en", "text": article}
	]}
	headers = {"Ocp-Apim-Subscription-Key": subscription_key}
	response = requests.post(keyphrase_url, headers=headers, json=documents)
	key_phrases = response.json()

	articlePhrases = key_phrases['documents'][0]['keyPhrases']

	# stem article phrases
	artLength = len(articlePhrases)
	for i in range(artLength) :
		articlePhrases[i] = ps.stem(articlePhrases[i])

	category = topic(titleWords, articlePhrases)
	print(category)


	# for key,value in keyWords.items() :
	# 	print(key)
	# 	print(value.keys())
		
	# 	# for key2, value2 in value.items() :
	# 	# 	print(key2)
	# 	# 	print(len(value2))
	
	# 	print("~~~~~~")

	currKey = ""
	currMax = -1
	currTotal = 0
	
	# keep count of key words in article for each category
	weights = {}
	points = {}

	for key, value in keyWords[category].items() :
		numPoints = 0
		
		for word in articlePhrases :
			if word in keyWords[category][key].keys() :
				numPoints += 1

		weights[key] = numPoints/len(value)
		points[key] = numPoints

		currTotal += numPoints

		# if numPoints > currMax :
		# 	currMax = numPoints
		# 	currKey = key

	for key, value in weights.items() :
		if value > currMax :
			currMax = value
			currKey = key

	currMax = points[currKey]

	keyList = []
	# put key words in array
	for key, value in keyWords[category][currKey].items() :	
		keyList += [key]

	if(currTotal != 0) :
		percent  = (currMax/currTotal) * 100
	else :
		percent = 0
	
	verdict = "error"

	if currKey == "WashingtonPost.json" :
		verdict = str(round(percent, 2)) + "% Leaning Left"
	elif currKey == "Reuters.json" :
		verdict = str(round(percent, 2)) + "% Center"
	elif currKey == "Fox.json" :
		verdict = str(round(percent, 2)) + "% Leaning Right"
	elif currKey == "InfoWars.json" :
		verdict = str(round(percent, 2)) + "% Right"
	elif currKey == "PalmerReport.json" :
		verdict = str(round(percent, 2)) + "% Left"

	links = bingsearchAPI(art.title)
	return [verdict, links]