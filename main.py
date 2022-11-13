# Author: Luis Wally Chavez Quiroz
# Email: lwchave2@illinois.edu
# Date: 11.12.2022
# Description: Script for running MLTK 

from twitterDocumentHarvester import TwitterDocumentHarvester

import sys
import os
import shutil
from datetime import datetime


directory_results = "results/"

def initialize_results():
	if (os.path.exists(directory_results)):
		shutil.rmtree(directory_results)
	os.makedirs(directory_results)

def time_log():
    current_time = datetime.now()
    time_stamp = current_time.timestamp()
    date_time = datetime.fromtimestamp(time_stamp)
    str_date_time = date_time.strftime("%d-%m-%Y_%H-%M-%S")
    return str_date_time

def sentiment_request():
    greeting_message = "Welcome to MLTK, a social media sentiment analysis tool for media (books, movies, games, etc). Please provide a social media platform and media item."
    print(greeting_message)
    platform = input("Social media platform: ")
    media_item = input("Media item: ")
    sentiment_query = [platform, media_item]
    return sentiment_query

def harvest_documents():
    sentiment_query = sentiment_request()
    platform = sentiment_query[0]
    media_item = sentiment_query[1]

    if platform.casefold() == 'twitter'.casefold():
        print("Harvesting Twitter documents...")
        harvester = TwitterDocumentHarvester(query=media_item, limit=200, min_likes=100, min_retweets=50, independent_filters=True)
    else:
        raise TypeError("The social media platform(s) available for MLTK at this time are: Twitter")

    initialize_results()
    str_date_time = time_log()
    results_file = directory_results + media_item + "---" + str_date_time + ".txt"
    harvester.generate_file(results_file)


def main():
    harvest_documents()
    # rank_documents()
    # analyze_documents()
    # report_results()

if __name__ == "__main__":
    main()