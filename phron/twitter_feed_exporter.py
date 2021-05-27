import json
import twitter
import csv

def timeline_to_json(timeline):
    """ dump a python-twitter UserTimeline to a json array of Status Models """
    s = '['
    for i in range(len(timeline) - 1):
        s += json.dumps(timeline[i]._json, ensure_ascii=False)
        s +=','
    s+= json.dumps(timeline[-1]._json, ensure_ascii=False)
    s += ']'
    return s

def timeline_to_json_file(timeline, fileobj=None, partial=False,start=True, end=True):
    """ 
        dump a python-twitter UserTimeline to a JSON file containing array of Status Models

        Parameters:
            timeline(list): a sequence of Status items from python-twitter

            fileobj(file): any object that supports the file API

            partial(Boolean): whether this is a partial print, meaning that's either
            the beginning of the array, (partial=True, start=True, end=False), the 
            middle of it (partial=True, start=False, end=True), or the end of it
            (partial=True, start=False, end=True).  If the given timeline list 
            represents the whole array, pass partial=False and 'start' and 'end'
            parameters will be ignored

            start(Boolean): when partial is True, indicates whether this timeline
            list is the beginning of the JSON array.

            end(Boolean): when partial is True, indicates whether this timeline
            list is the end of the JSON array.

    """
    pass

def flattened_timeline_to_csv(timeline, fileobj, append_category=None, tweet_mode='extended', string_transform=None):
    """ 
        A flattened timeline is the result of a python-twitter 
        api.GetUserTimeLine() call to a flat CSV file
        with the following structure:

        id, screen_name, text, created_at

        Optionally, a default value can be added as a 'category' for classifying purposes
        idn screen_name, text, created_at, category

        when the append_category parameter is passed with a value different to None

        the created_at date format is 'E MMM d HH:mm:ss Z YYYY'

        additionally the string 'string_transform' lambda can be passed to apply any transformations
        you might find suitable for your purposes, for example

        Parameters: 
            timeline(list): a sequence of Status items from python-twitter

            fileobj(file): any object that supports the file API

            append_category(str): a string to hardcode as category of each record

            tweet_mode(str): 'extended' or 'compat' 

            string_transform(lambda): a lambda that takes a string and returns a string.  

    """
    is_full_text = tweet_mode == 'extended'
    csv.register_dialect('twitter', escapechar='\\', doublequote=False, quoting=csv.QUOTE_NONE)
    
    writer = csv.writer(fileobj,'twitter')
    if append_category == None:
        writer.writerow(['id','screen_name', 'text', 'created_at'])
    else:
        writer.writerow(['id','screen_name', 'text', 'created_at', 'category'])
    
    for tweet in timeline:
        text = tweet.full_text if is_full_text else tweet.text

        if string_transform != None:
            text = string_transform(text)

        if append_category == None:
            writer.writerow([str(tweet.id),
                             tweet.user.screen_name, 
                             text,
                             tweet.created_at])
        else:
            writer.writerow([str(tweet.id),
                             tweet.user.screen_name, 
                             text,
                             tweet.created_at,
                             append_category])

def direct_messages_to_json(messages):
    """ dump a python-twitter GetDirectMessages to a json array of DirectMessage Models """
    s = '['
    for i in range(len(messages) - 1):
        s += json.dumps(messages[i]._json, ensure_ascii=False)
        s +=','
    s+= json.dumps(messages[-1]._json, ensure_ascii=False)
    s += ']'
    return s