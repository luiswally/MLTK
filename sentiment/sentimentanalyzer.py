# Author: Luis Wally Chavez Quiroz
# Email: lwchave2@illinois.edu
# Date: 12.8.2022
# Description: Sentiment module

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Sentiment:
    # Constructor method of Sentiment
    def __init__(self):
        self.rankedFile = None
        self.analyzedFile = None
        self.scoredFile = None
    
    # implement Vader out-of-box sentiment analyzer then try training or hardcoding emojis for positive
    def generate_analyzed_file(self, rankedFile, analyzedFile):
        with open(rankedFile, "r") as rf, open(analyzedFile, "w") as wf:
            ranked_file_lines = rf.readlines()
            for line in ranked_file_lines:
                processed_line = line.split(" *** ")
                clean_line = processed_line[1]
                sid = SentimentIntensityAnalyzer()
                ss = sid.polarity_scores(clean_line)
                to_write = ''
                for k in sorted(ss):
                    to_write += '{0}: {1}, '.format(k, ss[k])
                to_write = to_write + "\n"
                wf.write(to_write)

    # trasforming rating rating range from [-1, 1] to any range [1, 5] by default in 'generate_scored_file' section
    def normalize(self, sourceLowerBound, sourceUpperBound, destinationLowerBound, destinationUpperBound, sourceValue):
        deltaLower = destinationLowerBound - sourceLowerBound
        rangeSource = sourceUpperBound - sourceLowerBound
        rangeDestination = destinationUpperBound - destinationLowerBound
        magnification = rangeDestination / rangeSource
        translatedX = sourceValue + deltaLower
        start = destinationLowerBound - magnification * (sourceLowerBound + deltaLower)
        destinationValue = magnification * translatedX + start

        return destinationValue

    # generate overall sentiment score of user query using a [1, 5] range (typical for Google Rating, Apple Store, etc)
    def generate_scored_file(self, analyzedFile, scoredFile):
        with open(analyzedFile, "r") as rf, open(scoredFile, "w") as wf:
                analyzed_file_lines = rf.readlines()
                rating_list = []
                for line in analyzed_file_lines:
                    ratings = line.replace('compound: ', '')
                    ratings_split = ratings.split(', ')
                    rating_list.append(float(ratings_split[0]))
                avg_rating = sum(rating_list) / len(rating_list)
                result = self.normalize(sourceLowerBound=-1, sourceUpperBound=1, destinationLowerBound=1, destinationUpperBound=5, sourceValue=avg_rating)

                to_write = "average rating = {0} range:(-1, 1), normalized rating = {1} range:(1, 5)".format(avg_rating, result)
                wf.write(to_write)

                return result
