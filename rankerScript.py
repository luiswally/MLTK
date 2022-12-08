#!/Users/wally/opt/anaconda3/envs/python=3.7/bin/python

from ranker import Ranker

import nltk
import metapy
import glob
import os
import shutil

directory_results = "results/"

# Generate file with the provided file name and path
def generate_file():
    harvested_file = ''
    # Filter out the 'harvested_' file for use with Ranker() constructor
    for file in glob.glob(directory_results+"*.txt"):
        if "harvested_" in file:
            harvested_file = file

    ranks = Ranker(harvested_file)

def main():
    generate_file()

if __name__ == "__main__":
    main()