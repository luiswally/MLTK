import TwitterDocumentHarvester as harvester_factory

# Example of TwitterDocumentHarvester
if __name__ == '__main__':
    #Define query string
    query = 'God of War'

    #Instantiate harvester
    harvester = harvester_factory.TwitterDocumentHarvester(query=query, limit=200, min_likes=100)

    #Update configuration
    harvester.update_config(min_retweets=50, independent_filters=True)

    #Produce file
    harvester.generate_file('./twitter-documents.txt')