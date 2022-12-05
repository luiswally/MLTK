#import metapy
#import pytoml
import math
import pandas as pd

class Ranker:
    # Constructor method of Ranker
    def __init__(self, tempInput):
        self.tempInput = tempInput
        self.readFromHarvester()
        self.populateDictionary()
        self.calcTF(self.dictionary)
        self.calcIDF(self.dictionary)
        self.scoreAndDump()
        self.writeFile()
    
    def readFromHarvester(self):
        #f = pd.read_csv("../results/HarvesterOut.txt")
        f = open("../results/HarvesterOutput.txt", "r", errors="ignore")
        line = f.readline()
        tweets = []
        while(line):
            tweets.append(line.lower())
            line = f.readline()
        f.close()
        self.tweets = tweets
    
    def populateDictionary(self):
        tweets = self.tweets
        dictionary = {}
        count = 0
        doc_count = {}
        for tweet in tweets:
            tweet = tweet.split(' ')
            checked = []
            for word in tweet:
                if word not in checked:
                    try:
                        doc_count[word] = doc_count[word] + 1
                    except KeyError:
                        doc_count[word] = 1
                checked.append(word)
                count = 1
                try:
                    dictionary[word] = dictionary[word] + 1
                except KeyError:
                    dictionary[word] = 1
        self.dictionary = dictionary
        self.doc_count = doc_count
    
    def calcTF(self, map):
        tf = {}
        for i in map:
            tf[i] = math.log(map[i] + 1)
        self.tf = tf

    def calcIDF(self, map):
        idf ={}
        for i in map:
            idf[i] = math.log(len(self.tweets)/self.doc_count[i])
        self.idf = idf
    
    def scoreAndDump(self):
        score = []
        tweet_score_dump = []
        for tweet in self.tweets:
            tweet = tweet.split(' ')
            running_score = 0.0
            for word in tweet:
                num = self.tf[word] * self.idf[word]
                running_score = running_score + num
            score.append([running_score, running_score/len(tweet)])
            tweet_score_dump.append([' '.join(tweet), score[-1]])
        self.tweet_score_dump = sorted(tweet_score_dump, reverse = True, key = lambda x: x[1][1])

    def writeFile(self):
        f = open('../results/RankerOutput.txt', 'w')
        for i in self.tweet_score_dump[0:50]:
            f.write(str(i[1][1]) + " *** " + i[0])
        f.close()

Ranker(None)