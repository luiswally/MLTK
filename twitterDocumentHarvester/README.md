# Twitter Document Harvester

### Administrative
__Purpose__:

Implementation of document collector/harvester for twitter to support the MLTK group project for Fall 2022 Semester of CS410 - Text Information Systems at UoI-UC.

__Author(s):__
* Adam Michalsky (adamwm3@illinois.edu)

__Log__
* November 6, 2022 - _Initial Version_

### Overview
This python class utilizes `snscrape` and `pandas` to provide a simplified interface to harvest tweets or _documents_ from Twitter.

Configurable parameters include search criteria and filter critera.
#### Search Criteria

Search criteria is composed of the maximum amount of tweets to harvest and query to use during the document (or tweet) search.

#### Filter Criteria

Filter criteria is composed of minimum number of likes, minimum number of retweets, and a bool value indicating if each criterion (minimum likes or minimum retweets) is independent or dependent on the other. 

### Data Collection

The data is stored in a dataframe `TwitterDocumentHarvester.tweets` and can be access as required. This dataframe contains metadata as well as the tweet content harvest from Twitter.

#### Available Fields

* `id` - Unique system id of published tweet.
* `date` - Date of when tweet was published.
* `username` - Username of account that published the tweet.
* `hashtags` - List of hashtags associated with the tweet.
* `tweets` - Raw text content of published tweet scrubbed of `\n` characters.
* `likes` - Number of likes the published tweet received.
* `retweets` - Number of retweets the published tweet received.

## Runtime Information
### Python Environment
```commandline
Python 3.9.12 (main, Apr  5 2022, 01:53:17)
```
### Required Packages
 * `snscrape==0.4.3.20220106`
 * `pandas==1.5.1`

## TwitterDocumentHarvester.py
____
####  def \__init\__ self, query, limit=100, language='en', min_likes = -1, min_retweets=-1, independent_filters=False):
_Description:_
   Constructor function for the `TwitterDocumentHarvester` class. Initializes custom and static configurations.

_Parameters:_
* `query` - Mandatory `str` value to be used to search for documents on Twitter.
* `limit` - `int` value representing the maximum amount of documents to harvest.
  * Default is 100.
* `language` - _Optional_ `str` value representing the written language in documents to be harvested. 
  * Default value is  `'en'`. _All possible values can be found in Twitter's developer documentation [here](https://developer.twitter.com/en/docs/twitter-for-websites/supported-languages)._
* `min_likes` - _Optional_ `int` value representing the minimum amount of likes required on a document in order for it to be harvested. 
  * Default value is  -1. _Filter is not considered while harvesting._
* `min_retweets` - _Optional_ `int` value representing the minimum amount of likes required on a document in order for it to be harvested.
  * Default value is  -1. _Filter is not considered while harvesting._
* `independent_filters` - `bool` value that contains the logical operator in the filter clause of the final query.
  * Default value is `False`.
  * `True` indicates that both `min_likes AND min_retweets` criteria must be satisfied in order to be harvested.
  * `False` indicates that one of the filters `min_likes OR min_retweets` needs to be satisfied in order to be harvested. 
  * If either filter criteria has a value of -1, this parameter has no impact on the search.
    

_Usage:_
```python
import TwitterDocumentHarvester
query = 'God of War'
limit = 100
min_likes = 20

# Create document harvester
harvester = TwitterDocumentHarvester(query=query, limit=limit, min_likes=min_likes)
```

#### def update_config(self, language=None, query=None, limit=-1, min_likes=-1, min_retweets=-1, independent_filters=None):

_Description:_
Helper function that allows an update to any of the custom configurations that were specified during class instantiation. After updating the configuration, `harvest_tweets()` is invoked

_Parameters:_

_See parameters defined in function `__init__(self):` above._

_Usage:_
```python
import TwitterDocumentHarvester
query = 'God of War'
limit = 100
min_likes = 20

# Create document harvester.
harvester = TwitterDocumentHarvester(query=query, limit=limit, min_likes=min_likes)

# Update filter criteria and logical operator in filter clause.
harvester.update_config(min_retweets=27, independent_filters=True)
```
#### def harvest_tweets(self):
_Description:_
Function that works with `snscrape` Twitter module to fetch relevant tweets based on the `TwitterDocumentHarvester` configured filter and search criteria.

_Parameters:_

_None_

_Usage:_
```python
import TwitterDocumentHarvester
query = 'God of War'
limit = 100
min_likes = 20

# Create document harvester.
harvester = TwitterDocumentHarvester(query=query, limit=limit, min_likes=min_likes)

# Update filter criteria and logical operator in filter clause. 
# harvest_tweets() is automatically invoked at the end of update_config() method
harvester.update_config(min_retweets=27, independent_filters=True) 
```

#### def get_final_query(self):
_Description:_
Helper function used to compose the filter clause and combine it with the search clause prior to querying Twitter. This considers the `self.independent_filter` value when composing the filter clause with an __AND__ or an __OR__.

_Parameters:_

_None_

_Usage:_

```python
import TwitterDocumentHarvester
query = 'God of War'
limit = 100
min_likes = 100

# Create document harvester.
harvester = TwitterDocumentHarvester(query=query, limit=limit, min_likes=min_likes)

# Update filter criteria and logical operator in filter clause. 
# harvest_tweets() is automatically invoked at the end of update_config() method
harvester.update_config(min_retweets=50, independent_filters=True) 

# Print final query as string
print(harvester.get_final_query())
```
_Output_
```text
od of War AND (lang:en) AND (min_faves:100 OR min_retweets:50)
```


#### def generate_file(self, filepath='./documents.txt'):
_Description:_
Generates a text output file with the provided filename and path.
* Strongly recommended to use `.txt` file extension.

_Parameters:_
* `filepath` - The file path, including the filename with a `.txt` extension, where the tweets will be written seperated by `\n` characters.

_Usage_

```python
import TwitterDocumentHarvester
query = 'God of War'
limit = 100
min_likes = 100

# Create document harvester.
harvester = TwitterDocumentHarvester(query=query, limit=limit, min_likes=min_likes)

# Update filter criteria and logical operator in filter clause. 
# harvest_tweets() is automatically invoked at the end of update_config() method
harvester.update_config(min_retweets=50, independent_filters=True) 

# Produce output file
harvester.generate_file('./exports/my-twitter-documents.txt')
```