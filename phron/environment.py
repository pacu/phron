import twitter
from aenum import Enum
import os
class EnvironmentVariableKey(Enum):
    CONSUMER_KEY = 'PHRON_TWITTER_CONSUMER_KEY'
    CONSUMER_SECRET = 'PHRON_TWITTER_CONSUMER_SECRET'
    ACCESS_TOKEN = 'PHRON_TWITTER_ACCESS_TOKEN'
    ACCESS_TOKEN_SECRET = 'PHRON_TWITTER_ACCESS_TOKEN_SECRET'


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

    return twitter.Api(
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token_key=access_token, 
                        access_token_secret=access_token_secret,
                        tweet_mode='extended')

