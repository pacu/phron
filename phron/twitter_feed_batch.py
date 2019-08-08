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

def __no_argument_array_trailing_after_key(key):
    return InvalidArgument(message=f'No argument array trailing after key {key}')

def _extract_argument_array_after_key(key,argv):
    if not key in argv: raise InvalidArgument(message=f'Argument \'{key}\' not present in argument array')
    arg_array = []
    stop_words = _AcceptedArgumentKeys.key_list()
    argv_count = len(argv)
    start_index = argv.index(key) + 1
    if start_index >= argv_count: raise __no_argument_array_trailing_after_key(key)

    for i in range(start_index, argv_count):
        if argv[i] in stop_words: break
        arg_array.append(argv[i])
    
    if len(arg_array) == 0: raise __no_argument_array_trailing_after_key(key)

    return arg_array

def __extract_screen_names(argv):
    return _extract_argument_array_after_key(_AcceptedArgumentKeys.screen_names.value,argv)

def __extract_categories(argv):
    return _extract_argument_array_after_key(_AcceptedArgumentKeys.append_categories.value,argv)

def __validate_argument_dict(dict):
    return dict

def extract_arguments(argv=None):
    """ Extract arguments for this call """
    dict = {}
    
    # extract screen names or fail
    dict[_AcceptedArgumentKeys.screen_names.value] = __extract_screen_names(argv)
    
    if _AcceptedArgumentKeys.append_categories in argv:
        dict[_AcceptedArgumentKeys.append_categories.value] = __extract_categories(argv)
    
    dict[_AcceptedArgumentKeys.weka_friendly.value] = _AcceptedArgumentKeys.weka_friendly.value in argv
    dict[_AcceptedArgumentKeys.include_retweets.value] = _AcceptedArgumentKeys.include_retweets.value in argv

    if _AcceptedArgumentKeys.output_format.value in argv:
        idx = argv.index(_AcceptedArgumentKeys.output_format.value)
        fmt = argv[idx + 1]
        if not environment.OutputFormat.is_valid_format(fmt): raise InvalidArgument(message=f'Invalid output format: \'{fmt}\'')
    else:
        dict[_AcceptedArgumentKeys.output_format.value] = environment.OutputFormat.CSV.value
      
    return __validate_argument_dict(dict)

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
    
if __name__ == "__main__":
    pass

