# Author: Adam Michalsky
# Email: adamwm3@illinois.edu
# Date: 11.06.2022
# Description: Twitter scrapper that produces a file that can be leveraged by MeTaPY

import snscrape.modules.twitter as sntwitter
import pandas as pd

class TwitterDocumentHarvester:
    # Constructor method of harvester
    # Parameters query(str), limit(int), language(str), min_likes(int), min_retweets(int), independent_filters(bool)
    def __init__(self, query, limit=100, language='en', min_likes = -1, min_retweets=-1, independent_filters=False):
        self.limit = limit
        self.query = query
        self.language = language
        self.min_likes = min_likes
        self.min_retweets = min_retweets
        self.independent_filters = independent_filters
        self.columns = ['id', 'date', 'username', 'hashtag', 'tweet', 'likes', 'retweets']
        self.tweets = None
        self.harvest_tweets()

    # Update the configuration of the harvester. If a parameter is not specified it remains unaffected. Tweets are updated
    # after the configuration updates are applied. Parameter definition is the same as the above.
    def update_config(self, language=None, query=None, limit=-1, min_likes=-1, min_retweets=-1, independent_filters=None):
        if language is not None:
            self.language = language
        if query is not None:
            self.query = query
        if limit > 0:
            self.limit = limit
        if min_likes > 0:
            self.min_likes = min_likes
        if min_retweets > 0:
            self.min_retweets = min_retweets
        if independent_filters is not None:
            self.independent_filters = independent_filters

        self.harvest_tweets()

    # Construct final query containing the search clause AND filter clause.
    def get_final_query(self):
        filter = '(lang:' + self.language + ')'
        logic_operator = ' OR ' if self.independent_filters else ' AND '

        if self.min_retweets < 0 and self.min_likes >= 0:
            filter = filter + ' AND (min_faves:' + str(self.min_likes) + ')'
        elif self.min_retweets >= 0 and self.min_retweets < 0:
            filter = filter + ' AND (min_retweets:' + str(self.min_retweets) + ')'
        elif self.min_retweets >= 0 and self.min_retweets >= 0:
            filter = filter + ' AND (min_faves:' + str(self.min_likes) + str(logic_operator) + 'min_retweets:' + str(self.min_retweets) + ')'

        return self.query + ' AND ' + filter

    #Fetch tweets and update the internal dataframe containing tweet data.
    def harvest_tweets(self):
        tweets = []
        final_query = self.get_final_query()

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(final_query).get_items()):
            if i > self.limit:
                break
            else:
                tweets.append([tweet.id, tweet.date, tweet.user, tweet.hashtags, tweet.content.replace('\n',' '), tweet.likeCount, tweet.retweetCount])
        self.tweets = pd.DataFrame(tweets, columns=self.columns)

    #Generate file with the provided file name and path
    def generate_file(self, filepath='./documents.txt'):
        with open(filepath, "w") as f:
            for index, row in self.tweets.iterrows():
                f.write(row['tweet'] + '\n')