# Author: Luis Wally Chavez Quiroz
# Email: lwchave2@illinois.edu
# Date: 12.8.2022
# Description: Testing sentiment analysis results

import os
import glob


# declare constants
DIRECTORY_RESULTS_PATH = "/results"
DIRECTORY_TESTING_PATH = "/testing"
MEDIA_ITEM_TEST = 'Genshin Impact'
GOOGLE_PLAY_RATING = 4.2 # rating for 'Genshin Impact' as of 12/08/2022 08:30PM
APPLE_APP_STORE_RATING = 4.4 # rating for 'Genshin Impact' as of 12/08/2022 08:30PM
NUMBER_OF_TESTS = 4 # total number of tests

# global variables
scored_file = ''
passed_tests = 0

# retrieve scored file to perform tests on
def get_scored_file():
    global scored_file
    testing_path = os.path.dirname(os.path.realpath(__file__))
    results_path = testing_path.replace(DIRECTORY_TESTING_PATH, DIRECTORY_RESULTS_PATH)

    for file in glob.glob(results_path+"/*.txt"):
        if "scored_" in file:
            scored_file = file

# retrieve score rating from file
def get_score_rating():
    with open(scored_file, "r") as rf:
        scored_file_lines = rf.readlines()
        for line in scored_file_lines:
            processed_line = line.split(" ")
            rating = float(processed_line[9])
            return rating

# test to verify 'Genshin Impact' is the tested media item
def test_media_item(scored_file):
    global passed_tests
    media_item = scored_file.split("/scored_", 1)[1]
    media_item = media_item.split("---", 1)[0]
    
    if media_item.casefold() == MEDIA_ITEM_TEST.casefold():
        passed_tests += 1
        print("test_media_item...PASSED")
    else:
        raise TypeError("test_media_item..FAIL")
    pass

# test to ensure rating is within expected range [1, 5]
def test_rating_range(rating):
    global passed_tests
    if 1 <= rating <= 5:
        passed_tests += 1
        print("test_rating_range...PASSED")
    else:
        raise TypeError("test_rating_range..FAIL")
    pass

# test to verify sentiment analysis rating is within accetapble range of +/- 1
def test_rating_score(rating, REFERENCE_RATING):
    global passed_tests
    if abs(REFERENCE_RATING - rating) <= 1:
        passed_tests += 1
        print("test_rating_score...PASSED for {0}".format(REFERENCE_RATING))
    else:
        raise Exception("test_rating_range..FAIL for {0}".format(REFERENCE_RATING))
    pass

# run all tests and output number of tests passed
def main():
    get_scored_file()
    rating = get_score_rating()

    test_media_item(scored_file)
    test_rating_range(rating)
    test_rating_score(rating, GOOGLE_PLAY_RATING)
    test_rating_score(rating, APPLE_APP_STORE_RATING)

    print("------------------------------------------------------------------------------------------------------------")
    print("{0}/{1} tests passed".format(passed_tests, NUMBER_OF_TESTS))

if __name__ == "__main__":
    main()