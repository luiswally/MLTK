# MLTK - Modern Language Tool Kit

MLTK will ntegrate MeTA with NLTK to provide a sentiment analysis of any media shared on social media. The application is aimed at social media owners, however for the sake of showcasing the application will be developed such that social media users can also utilize it to the extent provided.

__Presentation:__ [MLTK Presentation and Demonstration](https://mediaspace.illinois.edu/media/t/1_1u75k8a6)

_Contact adamwm3@illinois.edu if there is a problem accessing the media._

# Getting Started
Ensure you have two Python virtual environments (3.7 and 3.9).
## Python 3.7 Environment
```bash
# Ensure you have the following dependencies up-to-date
pip install --upgrade pip
pip install metapy pytoml pandas
```
Update header of rankerScript.py to use any python 3.7 environment (example shown below):
```python
#!/Users/wally/opt/anaconda3/envs/python=3.7/bin/python
```
## Python 3.9 Environment
```bash
# Ensure you have the following dependencies up-to-date
pip install --upgrade pip
pip install nltk numpy snscrape pandas
```
# Using MLTK
## Command-line with Python 3.9 environment
```bash
# Run the main python script from the root directory
> python main.py
Welcome to MLTK, a social media sentiment analysis tool for media (books, movies, games, etc). Please provide a social media platform and media item.
Social media platform: [] # 'twitter' is the only supported platform at this time
Media item: [] # e.g. 'God of War'
Harvesting Twitter documents...
Ranking Twitter documents...
{} has a favoritibility of {}/5 on twitter
```
The main.py script will utilize three packages (twitterDocumentHarvester, ranker, sentiment), as shown below.
```mermaid
graph LR
A[twitterDocumentHarvester] --> B[ranker]
B --> C[sentiment]
C --> D[results]
```

The results will be stored in four *.txt files as shown below.
```
project
│   README.md
│   main.py    
│
└───results
│   │   analyzed_media_item---%d-%m-%Y_%H-%M-%S.txt
│   │   harvested_media_item---%d-%m-%Y_%H-%M-%S.txt
│   │   ranked_media_item---%d-%m-%Y_%H-%M-%S.txt
│   │   scored_media_item---%d-%m-%Y_%H-%M-%S.txt
│   │
│   ...
```
