# Author: Luis Wally Chavez Quiroz
# Email: lwchave2@illinois.edu
# Date: 12.6.2022
# Description: Script for running MLTK 

from twitterDocumentHarvester import TwitterDocumentHarvester

import sys
import os
import shutil
import subprocess
from datetime import datetime


#temp holder for sentiment
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import glob
#temp holder for sentiment


directory_results = "results/"
str_date_time = ""
platform = ''
media_item = ''

def time_log():
    current_time = datetime.now()
    time_stamp = current_time.timestamp()
    date_time = datetime.fromtimestamp(time_stamp)
    str_date_time = date_time.strftime("%d-%m-%Y_%H-%M-%S")
    return str_date_time

def initialize_results():
    global str_date_time
    if (os.path.exists(directory_results)):
        shutil.rmtree(directory_results)
    os.makedirs(directory_results)
    str_date_time = time_log()

def sentiment_request():
    greeting_message = "Welcome to MLTK, a social media sentiment analysis tool for media (books, movies, games, etc). Please provide a social media platform and media item."
    print(greeting_message)
    platform_in = input("Social media platform: ")
    media_item_in = input("Media item: ")
    sentiment_query = [platform_in, media_item_in]
    return sentiment_query

def harvest_documents():
    global platform, media_item
    sentiment_query = sentiment_request()
    platform = sentiment_query[0]
    media_item = sentiment_query[1]
    prefix = "harvested_"

    if platform.casefold() == 'twitter'.casefold():
        print("Harvesting Twitter documents...")
        harvester = TwitterDocumentHarvester(query=media_item, limit=200, min_likes=100, min_retweets=50, independent_filters=True)
    else:
        raise TypeError("The social media platform(s) available for MLTK at this time are: Twitter")

    initialize_results()
    results_file = directory_results + prefix + media_item + "---" + str_date_time + ".txt"
    harvester.generate_file(results_file)

def rank_documents():
    # run through scripted shell to allow for sub-process virtual environment 
    print("Ranking Twitter documents...")
    subprocess.run(["/Users/wally/Documents/School/Courses/FA2022/CS410/MLTK/rank.sh"], shell=True)

# TEMP place holder for SENTIMENT segment
def analyze_documents():
    ranked_file = ''
    for file in glob.glob(directory_results+"*.txt"):
        if "ranked_" in file:
            ranked_file = file

    analyzed_file = ranked_file
    analyzed_file = analyzed_file.replace(directory_results + "ranked_", directory_results + "analyzed_")

    with open(ranked_file, "r") as rf, open(analyzed_file, "w") as wf:
        ranked_file_lines = rf.readlines()
        counter = 0
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
            counter += 1

def report_results():
    analyzed_file = ''
    for file in glob.glob(directory_results+"*.txt"):
        if "analyzed_" in file:
            analyzed_file = file

    scored_file = analyzed_file
    scored_file = analyzed_file.replace(directory_results + "analyzed_", directory_results + "scored_")

    with open(analyzed_file, "r") as rf, open(scored_file, "w") as wf:
        analyzed_file_lines = rf.readlines()
        rating_list = []
        for line in analyzed_file_lines:
            ratings = line.replace('compound: ', '')
            ratings_split = ratings.split(', ')
            rating_list.append(float(ratings_split[0]))
        avg_rating = sum(rating_list) / len(rating_list)

        result = normalize([avg_rating], {'actual': {'lower': -1, 'upper': 1}, 'desired': {'lower': 0, 'upper': 5}})
        to_write = "average rating = {0} range:(-1, 1), normalized rating = {1} range:(0, 5)".format(avg_rating, result)
        wf.write(to_write)

        print("{0} has a favoritibility of {1:.2f}/5 on {2}".format(media_item, result[0], platform))

def normalize(values, bounds):
    return [bounds['desired']['lower'] + (x - bounds['actual']['lower']) * (bounds['desired']['upper'] - bounds['desired']['lower']) / (bounds['actual']['upper'] - bounds['actual']['lower']) for x in values]

# TEMP place holder for SENTIMENT segment

def main():
    harvest_documents()
    rank_documents()
    analyze_documents()
    report_results()

if __name__ == "__main__":
    main()