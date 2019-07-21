# phron
Phronesis is Practical Wisdom

Get tweets from feed and transform to various formats like CSV and JSON for Machine Learning purposes.

# Usage

## console application

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