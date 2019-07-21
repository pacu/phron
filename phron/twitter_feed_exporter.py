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


def flattened_timeline_to_csv(timeline, fileobj, append_category=None, tweet_mode='extended'):
    """ 
        A flattened timeline is the result of a python-twitter 
        api.GetUserTimeLine() call to a flat CSV file
        with the following structure
        screen_name, text, created_at
        
        Optionally, a default value can be added as a 'category' for classifying purposes
        screen_name, text, created_at, category
        when the append_category parameter is passed with a value different to None
    """
    is_full_text = tweet_mode == 'extended'
    csv.register_dialect('twitter', delimiter=',', quoting=csv.QUOTE_ALL)
    
    writer = csv.writer(fileobj,'twitter')
    if append_category == None:
        writer.writerow(['screen_name', 'text', 'created_at'])
    else:
        writer.writerow(['screen_name', 'text', 'created_at', 'category'])
    
    for tweet in timeline:
        text = tweet.full_text if is_full_text else tweet.text
        if append_category == None:
            writer.writerow([tweet.user.screen_name, 
                             text,
                             tweet.created_at])
        else:
            writer.writerow([tweet.user.screen_name, 
                             text,
                             tweet.created_at,
                             append_category])

    