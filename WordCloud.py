#!/usr/bin/env python3
'''
Author			: Rohit Farmer
Type 			: Script
Description		: Analyse tweet database and generate wordcloud
License			: GNU GPL V3.0
Contact			: rohitfarmer@protonmail.com
None core module: nltk, wordcloud
'''

import string
import re
import datetime, time
import sqlite3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from wordcloud import WordCloud
from collections import OrderedDict
import json

# Establish connection to Sqlite3 database
conn = sqlite3.connect('../bioinfotweet.db')
c = conn.cursor()

def tweetClean(text):
	"Function to remove unwanted text/words from tweets. This is independent of nltk stopwords method."
	# Remove hyperlinks
	text = re.sub('https:\/\/\S+', '', text)
	text = re.sub('http:\/\/\S+', '', text)
	text = re.sub('\&amp','',text)
	# Remove hashtags
	text = re.sub('\#\w+', '', text)
	text = re.sub('\#', ' ',text)
	# Remove citations
	text = re.sub('\@\w+', '', text)
	# Remove tickers
	text = re.sub('\$\w+', '', text)
	# Remove punctuation
	text = re.sub('[' + string.punctuation + ']+', '', text)
	# # Remove quotes
	text = re.sub('\&*[amp]*\;|gt+', '', text)
	# Remove RT and CT
	text = re.sub('rt\s+', '', text)
	text = re.sub('ct\s+', '', text)
	# Remove linebreak, tab, return
	text = re.sub('[\n\t\r]+', '', text)
	# Remove via with blank
	text = re.sub('via+\s', '', text)
	# Remove multiple whitespace
	text = re.sub('\s+\s+', ' ', text)
	# Remove anything that is not a unicode character
	text = re.sub('\W',' ',text)
	# Remove digits
	text = re.sub('\d+','',text)
	return text

# Extract tweets' text from the database followed by filtering and tokenizing
filteredText = []
rowCount = 0
totalHash = []
totalUsers =[]
totalTweetID = []
for row in c.execute('SELECT * FROM tweetscapture ORDER BY Date DESC'):
		creationDate = row[0]
		if '2017-05' in creationDate:
			rowCount += 1
			screenName = row[1]
			totalUsers.append(screenName)
			userID = row[2]
			tweetID = row[3]
			tweetText = tweetClean(row[4].lower())
			stopWords = list(stopwords.words("english"))
			myStopWords = ['also','cant','dont','hear','here','ive','im','like','latest','new','news','oh','see','top',
						   'th','twitter','thats','thanks','us','x']
			stopWords = stopWords + myStopWords
			words = word_tokenize(tweetText)
			fileteredSentence = [w for w in words if w not in stopWords]
			filteredText += fileteredSentence			
			#print(screenName,fileteredSentence)
			hashMatch = re.findall('\#\w+', row[4].lower())
			if hashMatch == []:
				continue
			else:
				totalHash += hashMatch
		#else :
			#break

totalWords = len(filteredText)
#print(totalWords)
freq = FreqDist(filteredText)
uniqueWords = len(freq)
#print(uniqueWords)
del filteredText

stopHash =['#twitter','#tweeted'] # Hastags of no interest
totalHash[:] = [h for h in totalHash if h not in stopHash] # Get ride of any cell with stop hashtags
hashFreq = FreqDist(totalHash)
usersFreq = FreqDist(totalUsers)

# Generate a word cloud image
wordcloud = WordCloud(font_path='Actor-Regular.ttf', width = 1500, height=500,  
			max_words=500,	stopwords=None, background_color='whitesmoke', 
			max_font_size=None, font_step=1, mode='RGB', 
			collocations=True, colormap=None, normalize_plurals=True).generate_from_frequencies(freq)
imageName = '2017-05.png'
imagePath = "images/"+imageName # Put the actual path of the word cloud image produced in the previous step
wordcloud.to_file(imagePath)
imageUrl = "https://bioinfobot.github.io/"+imagePath


def dictValueSortReturnTop (dict,max):
	"Sort the dictionary according to values and return a list of top n elements"	
	dictSorted=OrderedDict(sorted(dict.items(), key=lambda t: t[1], reverse=True))
	# Store top values in an array
	# Change maxCount value to extract top n elements
	count = 0
	maxCount = 20 
	topElements = []
	for k,v in dictSorted.items():
		# Key and value pairs are stored in the form of a tuple in the topWords array
		# Another dictionary is not created here in order to preserve the sorted order
		topElements.append((k,v))
		count += 1
		if count >=maxCount:
			break
	return topElements

# Sort and store top n elements in an array
topWords=dictValueSortReturnTop(freq,20)
del freq # Delete freq variable to free memory space
hashFreqSorted=dictValueSortReturnTop(hashFreq,20)
del hashFreq
usersFreqSorted=dictValueSortReturnTop(usersFreq,20)
del usersFreq

# Create a json file
# The top level data structure of a json file or object is a dictionary
# Variable to store data for json dump
mainJsonDump = {"ImageURL":imageUrl,"TopWords":topWords,"TweetCount":rowCount, "TotalWords":totalWords, "UniqueWords":uniqueWords,'HashFreq':hashFreqSorted,'UsersFreq':usersFreqSorted}
# ImageURL contains the path to the wordcloud image produced in the previous block in string format
# TopWords contains the top words arranged in descending order in 
# an array. Each array element is a tuple/array with two entries, word (index 0) and frequency (index 1)
# TweetCount contains the total no of tweets read from the database
# TotalWords contains the total no of filtered words used in the analysis
# UniqueWords contains the total no of unique words in the frequency dictionary
# HashFreq contains top n hashtags
# UsersFreq contains top n users

# Write a json file
jsonPath = 'data/2017-05.json'
with open(jsonPath, 'w') as wcd:
	json.dump(mainJsonDump, wcd)

# Load the above created json file and read the elements from dictionary and arrays 
# This code is a template to reproduce it in JavaScript for the website
# It shows how the elements are stored in the json file
with open(jsonPath, 'r') as rwcd:
	obj = json.load(rwcd)
	print(json.dumps(obj, indent='\t'))
	# print('ImageURL:',obj['ImageURL'])
	# print('TopWords:')
	# for i in range(0,19):
	# 	print(obj['TopWords'][i][0],'(',obj['TopWords'][i][1],')')
	# print('TweetCount:',obj['TweetCount'])
	# print('TotalWords:',obj['TotalWords'])
	# print('UniqueWords:',obj['UniqueWords'])
