import twitter 
import datetime
import os
import environment

def get_all_tweets(api=None, screen_name=None, include_rts=True):
    timeline = api.GetUserTimeline(screen_name=screen_name,include_rts=include_rts, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            timeline += tweets

    return timeline


def get_tweets(api=None, screen_name=None, include_rts=True, from_timestamp=None, until_timestamp=None):
    timeline = []
    earliest_tweet = None
    
    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        filtered_tweets = filter(lambda x: x.created_at > from_timestamp and x.created_at < until_timestamp, tweets)
        timeline += filtered_tweets
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or tweets[-1].created_at > from_timestamp:
            break
        else:
            earliest_tweet = new_earliest
            timeline += tweets
    return timeline


def usage():
    """
    twitter_feed.py extract all tweets from user timeline on extended format
    usage: 
    python twitter_feed.py --screen-name SCREEN_NAME --output-format OUTPUT_FORMAT [--append-category CATEGORY]  [--weka-friendly] [--include-retweets]
   
   Parameters:
    
    --screen-name (mandatory): twitter screen_name value
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
    import sys
    import json
    from twitter_feed_exporter import timeline_to_json
    from twitter_feed_exporter import flattened_timeline_to_csv
    from environment import build_api_from_environment
    try: 
        if '-h' in sys.argv or '--help' in sys.argv:
            usage()
            exit()

        api = build_api_from_environment()
        screen_name_index = sys.argv.index('--screen-name')    

        screen_name = sys.argv[screen_name_index + 1]
        
        format = sys.argv[sys.argv.index('--output-format') + 1]

        include_rts = '--include-retweets' in sys.argv
        timeline = get_all_tweets(api=api,screen_name=screen_name, include_rts=include_rts)
        
        if format == 'json':
            sys.stdout.write(timeline_to_json(timeline))
        if format == 'csv':
            string_transform = None

            if '--weka-friendly' in sys.argv:
                from text_sanitizer import sanitize_weka
                string_transform = lambda x: sanitize_weka(x, escape_doublequote=False, escape_singlequote=False, remove_separator=",")

            category = None
            if '--append-category' in sys.argv:
                category = sys.argv[sys.argv.index('--append-category') + 1]
            
            flattened_timeline_to_csv(timeline,sys.stdout, append_category=category, string_transform=string_transform)

    except EnvironmentError as err:
        usage_and_fail(message=err.message)
    except ValueError as valueErr:
        usage_and_fail(message=f'missing argument. {valueErr}')
