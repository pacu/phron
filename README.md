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
id, screen_name, text, created_at
... rows
```

getting all tweets from TWITTER_USER timeline in a flattened CSV fromat and adding a category tag to each row. (useful for classifying)

``` python twitter_feed.py --screen-name {TWITTER_USER} --output-format csv --append-category {SOME_CATEGORY} ```

this will output a csv to stdout with the format 
``` 
id, screen_name, text, created_at, category
... rows
```

### Support for Weka 3.x importer

the module ```text_sanitizer.py``` allows you clean up text strings in order to match weka's
'requirements' regarding single and double quotes and separator characters appearing on a string
value of the CSV

``` Python
    def sanitize_weka(text: str, remove_newlines=True, escape_doublequote=True, escape_singlequote=True,remove_separator=None) -> str:
```
** Example **
``` Python
  def test_weka_sanitizer_quoting(self):
        """ given a text with quotes, remove them """
        given = '""No es posible que no le podamos garantizar dignidad a los que toda su vida trabajaron. Vamos a recomponer el ingreso de los jubilados. Y vamos a hacer una ley que diga que los jubilados no pagan los medicamentos y el Estado los va a subsidiar"'
        expect = "No es posible que no le podamos garantizar dignidad a los que toda su vida trabajaron. Vamos a recomponer el ingreso de los jubilados. Y vamos a hacer una ley que diga que los jubilados no pagan los medicamentos y el Estado los va a subsidiar"
        
        self.assertEqual(expect,text_sanitizer.sanitize_weka(given,escape_doublequote=False),"Sanitized string is not what weka would expect it to be")

    def test_weka_sanitizer_escape_double_quoting(self):
        """ given a text with quotes, escape them """
        given = '""No es posible que no le podamos garantizar dignidad a los que toda su vida trabajaron. Vamos a recomponer el ingreso de los jubilados. Y vamos a hacer una ley que diga que los jubilados no pagan los medicamentos y el Estado los va a subsidiar"'
        expect = "\\\"\\\"No es posible que no le podamos garantizar dignidad a los que toda su vida trabajaron. Vamos a recomponer el ingreso de los jubilados. Y vamos a hacer una ley que diga que los jubilados no pagan los medicamentos y el Estado los va a subsidiar\\\""
        
        self.assertEqual(expect,text_sanitizer.sanitize_weka(given),"Sanitized string is not what weka would expect it to be")
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