import twitter


def get_all_direct_messages(api=None, force_json=False):
    # GetDirectMessages(since_id=None, max_id=None, count=None, include_entities=True, skip_status=False, full_text=False, page=None, return_json=False)

    messages = api.GetDirectMessages(count=200,full_text=True, return_json=force_json)
    earliest_tweet = min(messages, key=lambda x: x.id).id
    while True:
        tweets = api.api.GetDirectMessages(count=200,full_text=True,return_json=force_json)(
                max_id=earliest_tweet, count=200
                )

        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            messages += tweets

    return messages


def usage():
    """
    twitter_direct_messages.py extracts all direct messages from the API application user on fult-text format
    usage: 
    python twitter_direct_messages.py --output-format OUTPUT_FORMAT [--append-category CATEGORY]  [--weka-friendly] [--include-retweets]
   
   Parameters:
    --output-format (optional): json (defult)

    CSV options (coming soon)
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
    from environment import build_api_from_environment
    from twitter_feed_exporter import direct_messages_to_json
    api = build_api_from_environment()

    messages = get_all_direct_messages(api=api, force_json=True)

    output_format_override = "--output-format" in sys.argv

    if output_format_override:
        output_format = sys.argv[output_format_override + 1]

        if output_format != "json":
            usage_and_fail(message='Unrecognized output format')
    
    # no other format than json for now
    sys.stdout.write(messages)
