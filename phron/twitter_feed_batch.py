
def usage():
    """
    twitter_feed_batch.py extract all tweets from the specified user timelines on extended format
    usage: 
    python twitter_feed_batch.py --screen-names SCREEN_NAME_1 SCREEN_NAME_2 SCREEN_NAME_3 SCREEN_NAME_4 --output-format OUTPUT_FORMAT [--append-categories CATEGORY_1, CATEGORY_2, CATEGORY_3, CATEGORY_4]  [--weka-friendly] [--include-retweets]
   
   Parameters:
    
    --screen-names (mandatory): twitter screen_name values 
    --include-retweets (optional): if your output includes RTs
    --output-format (mandatory): json or csv


    CSV options
    ===========
    --append-category (optional): add category column with the given value on every record
    --weka-friendly (optional): sanitize text string for weka compatibility

    """
    print(usage.__doc__)

def usage_and_fail(message=None):
    if message: print(message)
    usage()
    import sys
    sys.exit(1)

if __name__ == "__main__":
    pass