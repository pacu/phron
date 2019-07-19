import twitter 
import datetime

def get_all_tweets(api=None, screen_name=None, include_rts=True):
    timeline = api.GetUserTimeline(screen_name=screen_name,include_rts=include_rts, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


def get_tweets(api=None, screen_name=None, include_rts=True, from_timestamp=None, until_timestamp=None):
    timeline = []
    earliest_tweet = None
    print("getting tweets before:", from_timestamp)
    
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
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline