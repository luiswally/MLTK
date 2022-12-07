import metapy
import pytoml
import math
import pandas as pd

class Ranker:
    # Constructor method of Ranker
    def __init__(self, filePath, k = 50):
        self.filePath = filePath
        self.k = k
        self.startRanker() # starts the ranker function
    
    def startRanker(self):
        self.tweets = []
        self.dictionary = {}
        self.doc_count = {}
        self.avg_dl = 0.0
        self.tf = {}
        self.idf = {}
        self.tweet_score_dump = {}

        self.readFromHarvester()    # Reads input from the previous module's output
        self.populateDictionary()   # Converts the documents into variables that can be readily used by the subsequent functions
        self.calcTf()               # Calculates the Term Frequency of all words in the collection
        self.calcIdf()              # Calculates the Inverse Document Frequency of all words in the collection
        self.scoreAndDump()         # Calculates the scores of each tweet and dumps them onto a storage
        self.writeFile()            # Writes the top k tweets into the output file
    
    def readFromHarvester(self):
        # Reads input from the previous module's output

        #f = pd.read_csv("../results/HarvesterOut.txt")
        #f = open("../results/HarvesterOutput.txt", "r", errors="ignore")
        f = open(self.filePath, "r", errors="ignore")
        line = f.readline()
        tweets = []
        while(line):
            tweets.append(line.lower())
            line = f.readline()
        f.close()
        self.tweets = tweets
    
    def populateDictionary(self):
        # Converts the documents into variables that can be readily used by the subsequent functions
        tweets = self.tweets
        dictionary = {}
        count = 0
        doc_count = {}
        for tweet in tweets:
            tweet = tweet.split(' ')
            checked = []
            for word in tweet:
                count = count + 1
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
        self.avg_dl = count/len(tweets)

    def calcTf(self):
        # Calculates the Term Frequency of all words in the collection
        '''Note that TF is generally calculated with respect to a query and a document. But, here we are doing it for the entire collection (i.e.) TF of a word to be 
        the same irrespective of which doc it occurs in. This is due to difference in the actual meaning of TF in this use case. Normally the query is an insight to 
        match relevant docs and therefore, the TF can vary across docs. However, in our case, the query itself is not very insightful. Therefore, the context has to be 
        built from within the set of documents retrieved by the harvester. This explains the need to maintain a similar TF to a word with logarthmic penalty. And this 
        is why we should write our definition of TF and not just extend MetaPy's calculator.
        '''
        tf = {}
        for i in self.dictionary:
            tf[i] = math.log(self.dictionary[i] + 1)
        self.tf = tf

    def calcIdf(self):
        # Calculates the Inverse Document Frequency of all words in the collection
        idf ={}
        for i in self.dictionary:
            idf[i] = math.log((len(self.tweets) + 1)/self.doc_count[i])
        self.idf = idf
    
    def scoreAndDump(self):
        # Calculates the scores of each tweet and dumps them onto a storage
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
        # Writes the top k tweets into the output file
        self.k = min(self.k, len(self.tweet_score_dump)) # Can not output more tweets than what is scored
        rankedFilePath = self.filePath.replace("results/harvested_", "results/ranked_")
        # f = open('results/RankerOutput.txt', 'w')
        f = open(rankedFilePath, 'w')
        for i in self.tweet_score_dump[0:self.k]:
            f.write(str(i[1][1]) + " *** " + i[0])
        f.close()

#Ranker("filepath", 20) - This is the way to call this class, the parameter to the constructor being the results filepath and the number of top tweets you would like to retrieve.