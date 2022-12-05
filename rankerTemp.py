#!/Users/wally/opt/anaconda3/envs/python=3.7/bin/python


import nltk
import metapy
import glob
import os
import shutil

# nltk.download('vader_lexicon')
# from nltk.sentiment.vader import SentimentIntensityAnalyzer


directory_results = "results/"

class InL2Ranker(metapy.index.RankingFunction):

    def __init__(self, some_param=1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()

    def score_one(self, sd):
        c = self.param
        tfn = sd.doc_term_count*math.log(1+(sd.avg_dl/sd.doc_size), 2)
        score = (tfn/(tfn+c))*math.log((sd.num_docs+1)/(sd.corpus_term_count+0.5), 2)
        return score
# def initialize_results():
# 	if (os.path.exists(directory_results)):
# 		shutil.rmtree(directory_results)
# 	os.makedirs(directory_results)



#Generate file with the provided file name and path
def generate_file():
    txtFile = []
    for file in glob.glob(directory_results+"*.txt"):
        txtFile.append(file)
    sourcePath = txtFile[0]
    fileName = txtFile[0]
    fileName = fileName.replace(directory_results, "ranked_")
    filePath = directory_results + fileName

    # All files and directories ending with
    shutil.copy(sourcePath, filePath)


def main():
    generate_file()


if __name__ == "__main__":
    main()