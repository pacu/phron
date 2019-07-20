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


from aenum import Enum
class EnvironmentVariableKey(Enum):
    CONSUMER_KEY = 'TWITTER_CONSUMER_KEY'
    CONSUMER_SECRET = 'TWITTER_CONSUMER_SECRET'
    ACCESS_TOKEN = 'TWITTER_ACCESS_TOKEN'
    ACCESS_TOKEN_SECRET = 'TWITTER_ACCESS_TOKEN_SECRET'


from functools import wraps

class Error(Exception):
    pass

class EnvironmentError(Error):
    """Exception raised for errors in the environment settings.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
    

def validate_environment():
    import os
    
    try: 
        consumer_key = os.environ[EnvironmentVariableKey.CONSUMER_KEY.value]
        consumer_secret = os.environ[EnvironmentVariableKey.CONSUMER_SECRET.value]
        access_token = os.environ[EnvironmentVariableKey.ACCESS_TOKEN.value]
        access_token_secret = os.environ[EnvironmentVariableKey.ACCESS_TOKEN_SECRET.value]
    except KeyError as keyError:
        raise EnvironmentError(message=f'missing environment variable {str(keyError)}' )

    if not consumer_key : raise EnvironmentError(message='missing consumer key')
    if not consumer_secret: raise EnvironmentError(message='consumer_secret missing')
    if not access_token: raise EnvironmentError(message='access_token missing')
    if not access_token_secret: raise EnvironmentError(message='access_token_secret missing')


def environment_check(decorator):
    @wraps(decorator)
    def wrapped_decorator(*args, **kwargs):
        validate_environment()
        return decorator()

    return wrapped_decorator

@environment_check
def build_api_from_environment():
    import os
    consumer_key = os.environ[EnvironmentVariableKey.CONSUMER_KEY.value]
    consumer_secret = os.environ[EnvironmentVariableKey.CONSUMER_SECRET.value]
    access_token = os.environ[EnvironmentVariableKey.ACCESS_TOKEN.value]
    access_token_secret = os.environ[EnvironmentVariableKey.ACCESS_TOKEN_SECRET.value]

    return twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)


def usage():
    pass

def usage_and_fail(message=None):
    if message: print(message)
    usage()
    import sys
    sys.exit(1)


if __name__ == "__main__":
    import sys
    import json
    try: 
        api = build_api_from_environment()
        screen_name_index = sys.argv.index('--screen-name')
        if not screen_name_index: usage_and_fail(message='no screen name found')

        screen_name = sys.argv[screen_name_index + 1]

        if not screen_name: usage_and_fail(message='no screen name found')
        

        json.dump(get_all_tweets(api=api,screen_name=screen_name), sys.stdout, ensure_ascii=False)

    except EnvironmentError as err:
        usage_and_fail(message=err.message)
    

