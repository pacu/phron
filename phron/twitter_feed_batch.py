from aenum import Enum
from phron import environment

class InvalidArgument(environment.Error):
    """ 
    Exception raised for errors in the environment settings.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
    
        
class _AcceptedArgumentKeys(Enum):
    screen_names = "--screen-names"
    include_retweets = "--include-retweets"
    output_format = "--output-format"
    append_categories = "--append-categories"
    weka_friendly = "--weka-friendly"
   
    @classmethod
    def key_list(cls):
        return [
                    _AcceptedArgumentKeys.screen_names.value, 
                    _AcceptedArgumentKeys.include_retweets.value,
                    _AcceptedArgumentKeys.output_format.value,
                    _AcceptedArgumentKeys.append_categories.value,
                    _AcceptedArgumentKeys.weka_friendly.value
                ]


def _no_argument_array_trailing_after_key(key):
    return InvalidArgument(message=f'No argument array trailing after key {key}')

def _extract_argument_array_after_key(key,argv):
    if not key in argv: raise InvalidArgument(message=f'Argument \'{key}\' not present in argument array')
    arg_array = []
    stop_words = _AcceptedArgumentKeys.key_list()
    argv_count = len(argv)
    start_index = argv.index(key) + 1
    if start_index >= argv_count: raise _no_argument_array_trailing_after_key(key)

    for i in range(start_index, argv_count):
        if argv[i] in stop_words: break
        arg_array.append(argv[i])
    
    if len(arg_array) == 0: raise _no_argument_array_trailing_after_key(key)

    return arg_array

def _extract_screen_names(argv):
    return _extract_argument_array_after_key(_AcceptedArgumentKeys.screen_names.value,argv)

def _extract_categories(argv):
    return _extract_argument_array_after_key(_AcceptedArgumentKeys.append_categories.value,argv)

# validations
def _valid_screen_names_count(dict):   
    return  _AcceptedArgumentKeys.screen_names.value in dict and len(dict[_AcceptedArgumentKeys.screen_names.value]) > 0 

def _valid_categories_screen_name(dict):
    if not _AcceptedArgumentKeys.append_categories.value in dict: return False
    if not _AcceptedArgumentKeys.screen_names.value in dict: return False 

    return len(dict[_AcceptedArgumentKeys.append_categories.value]) == len(dict[_AcceptedArgumentKeys.screen_names.value])

def _valid_output_format(dict):
    return _AcceptedArgumentKeys.output_format.value in dict and environment.OutputFormat.is_valid_format(dict[_AcceptedArgumentKeys.output_format.value])

def _validate_argument_dict(dict):
    if not _valid_screen_names_count(dict): raise InvalidArgument('Invalid screen names argument count')
    if _AcceptedArgumentKeys.append_categories.value in dict and not _valid_categories_screen_name(dict): raise InvalidArgument('Invalid argument count between screen names and appended categories')
    if not _valid_output_format(dict): raise InvalidArgument('Invalid or missing output format')
    if not _AcceptedArgumentKeys.weka_friendly.value in dict: raise InvalidArgument(f'{_AcceptedArgumentKeys.weka_friendly.value} not specified')
    if not _AcceptedArgumentKeys.include_retweets.value in dict: raise InvalidArgument(f'{_AcceptedArgumentKeys.include_retweets.value} not specified')
    return dict

    
# argument extraction 

def extract_arguments(argv=None):
    """ Extract arguments for this call """
    dict = {}
    
    # extract screen names or fail
    dict[_AcceptedArgumentKeys.screen_names.value] = _extract_screen_names(argv)
    
    if _AcceptedArgumentKeys.append_categories in argv:
        dict[_AcceptedArgumentKeys.append_categories.value] = _extract_categories(argv)
    
    dict[_AcceptedArgumentKeys.weka_friendly.value] = _AcceptedArgumentKeys.weka_friendly.value in argv
    dict[_AcceptedArgumentKeys.include_retweets.value] = _AcceptedArgumentKeys.include_retweets.value in argv

    if _AcceptedArgumentKeys.output_format.value in argv:
        idx = argv.index(_AcceptedArgumentKeys.output_format.value)
        fmt = argv[idx + 1]
        if not environment.OutputFormat.is_valid_format(fmt): raise InvalidArgument(message=f'Invalid output format: \'{fmt}\'')
        dict[_AcceptedArgumentKeys.output_format.value] = fmt
    else:
        dict[_AcceptedArgumentKeys.output_format.value] = environment.OutputFormat.CSV.value
      
    return _validate_argument_dict(dict)

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
    --append-categories (optional): add category column with the given value on every record
    --weka-friendly (optional): sanitize text string for weka compatibility

    """
    print(usage.__doc__)

def usage_and_fail(message=None):
    if message: print(message)
    usage()
    import sys
    sys.exit(1)

def batch_extract_tweets(api, 
                        screen_names, 
                        append_categories=None, 
                        include_retweets=False, 
                        output_format=environment.OutputFormat.CSV, 
                        string_transform=None):

    usage_and_fail(message='unimplemented') 

def _batch_extract_tweets(api, parameters):
    """
        batch extract a list of timelines from a twitter account.
        convenience method to invoke from __main__

        Parameters: 
            api(twitter_api): an Initialized python-twitter api object

            parameters(dict): a dictionary with the extracted parameters
            in the form of: 

            {
                twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4'],
                twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value : False,
                twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value : True,
                twitter_feed_batch._AcceptedArgumentKeys.append_categories.value : ['A', 'B','C','D'],
                twitter_feed_batch._AcceptedArgumentKeys.output_format.value : 'csv'
            }

            see tests for more examples
    """
    
    from text_sanitizer import sanitize_weka

    weka_friendly = parameters[_AcceptedArgumentKeys.weka_friendly.value]
    include_retweets = parameters[_AcceptedArgumentKeys.include_retweets]
    output_format = parameters[_AcceptedArgumentKeys.output_format.value]
    
    screen_names = parameters[_AcceptedArgumentKeys.output_format.value]
    append_categories = None
    if _AcceptedArgumentKeys.append_categories.value in parameters:
        append_categories = parameters[_AcceptedArgumentKeys.append_categories.value]
    
    transform_lambda = None

    if weka_friendly:
        transform_lambda = lambda x: sanitize_weka(x, escape_doublequote=False, escape_singlequote=False, remove_separator=",")
    
    return batch_extract_tweets(api=api,
                                screen_names=screen_names,
                                append_categories=append_categories,
                                include_retweets=include_retweets,
                                output_format=output_format,
                                string_transform=transform_lambda
                                )

if __name__ == "__main__":
    import sys
    from environment import build_api_from_environment
    try:
        arguments = extract_arguments(sys.argv)
    except InvalidArgument as ive:
        usage_and_fail(message=ive.message)
    
    _batch_extract_tweets(build_api_from_environment(),arguments)
    


