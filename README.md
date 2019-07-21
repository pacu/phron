# phron
Phronesis is Practical Wisdom

Get tweets from feed and transform to various formats like CSV and JSON for Machine Learning purposes.

# Requirements
phron requires a twitter developer application to run. All Twitter API limitations apply to it. 

# Usage

## console application

### Setting up the API
twitter_feed.py uses the python-twitter library to get the user's timeline. 

to passing secrets thru the command line, the API object is initialized with Environment Variables

On UNIX systems just add these to your bash or other terminal environtment of your liking

**On .bash_profile**
```` bash
export PHRON_TWITTER_CONSUMER_KEY="someconsumerkey"
export PHRON_TWITTER_CONSUMER_SECRET="someconsumersecret"
export PHRON_TWITTER_ACCESS_TOKEN="appaccesstoken"
export PHRON_TWITTER_ACCESS_TOKEN_SECRET="appaccesstokensecret"
````

## Supported output formats

### Comma Separated Values
getting all tweets from TWITTER_USER timeline in a flattened CSV fromat
``` python twitter_feed.py --screen-name {TWITTER_USER} --output-format csv```

this will output a csv to stdout with the format 
``` 
screen_name, text, created_at
... rows
```

getting all tweets from TWITTER_USER timeline in a flattened CSV fromat and adding a category tag to each row. (useful for classifying)

``` python twitter_feed.py --screen-name {TWITTER_USER} --output-format csv --append-category {SOME_CATEGORY} ```

this will output a csv to stdout with the format 
``` 
screen_name, text, created_at, category
... rows
```
### JSON

getting all tweets from TWITTER_USER timeline in a JSON array of tweets. [This corresponds to python-twitter's Status Model](https://python-twitter.readthedocs.io/en/latest/twitter.html#twitter.models.Status)

``` python twitter_feed.py --screen-name {TWITTER_USER} --output-format json ```

# Dependencies

* [Python Twitter](https://python-twitter.readthedocs.io)
* [Advanced Enumerations](https://bitbucket.org/stoneleaf/aenum)

# Contributing
Just Send a Pull Request :) all help and enhancements are welcome!


# Licence
Apache License Version 2.0