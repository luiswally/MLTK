# Author: Luis Wally Chavez Quiroz
# Email: lwchave2@illinois.edu
# Date: 12.8.2022
# Description: Script for running MLTK 

from twitterDocumentHarvester import TwitterDocumentHarvester
from sentiment import Sentiment

import sys
import os
import shutil
import subprocess
from datetime import datetime
import glob


directory_results = "results/"
str_date_time = ""
platform = ''
media_item = ''

# logs the date and time of query for use in output documents see /results folder
def time_log():
    current_time = datetime.now()
    time_stamp = current_time.timestamp()
    date_time = datetime.fromtimestamp(time_stamp)
    str_date_time = date_time.strftime("%d-%m-%Y_%H-%M-%S")
    return str_date_time

# cleans up /results directory and initializes time to log
def initialize_results():
    global str_date_time
    if (os.path.exists(directory_results)):
        shutil.rmtree(directory_results)
    os.makedirs(directory_results)
    str_date_time = time_log()

# prompts user for (1) social media platform AND (2) media item query 
def sentiment_request():
    greeting_message = "Welcome to MLTK, a social media sentiment analysis tool for media (books, movies, games, etc). Please provide a social media platform and media item."
    print(greeting_message)
    platform_in = input("Social media platform: ")
    media_item_in = input("Media item: ")
    sentiment_query = [platform_in, media_item_in]
    return sentiment_query

# retrieves documents of specified social media platform
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

# ranks documents via sub-process
def rank_documents():
    # run through scripted shell to allow for sub-process virtual environment 
    print("Ranking Twitter documents...")
    subprocess.run(["./rank.sh"], shell=True)

# peforms sentiment analysis of documents
def analyze_documents():
    ranked_file = ''
    for file in glob.glob(directory_results+"*.txt"):
        if "ranked_" in file:
            ranked_file = file

    analyzed_file = ranked_file
    scored_file = analyzed_file

    analyzed_file = analyzed_file.replace(directory_results + "ranked_", directory_results + "analyzed_")
    scored_file = analyzed_file.replace(directory_results + "analyzed_", directory_results + "scored_")

    analyzer = Sentiment()
    analyzer.generate_analyzed_file(ranked_file, analyzed_file)
    result = analyzer.generate_scored_file(analyzed_file, scored_file)
    print("{0} has a favoritibility of {1:.2f}/5 on {2}".format(media_item, result, platform))

def main():
    harvest_documents()
    rank_documents()
    analyze_documents()

if __name__ == "__main__":
    main()