import unittest
import sys
from phron import twitter_feed_batch

class TestSanitizer(unittest.TestCase):
    def test_extract_arguments(self):
        """given a set of parameters extract them"""

        given = [sys.path, '--screen-names', 'name_1', 'name_2', 'name_3', 'name_4', '--output-format', 'csv', '--append-categories', 'A', 'B','C','D', '--weka-friendly','--include-retweets']

        expect = {
                    '--screen-names' : ['name_1', 'name_2', 'name_3', 'name_4'],
                    '--weka-friendly' : True,
                    '--include-retweets' : True,
                    '--append-categories' : ['A', 'B','C','D'],
                    '--output-format' : 'csv'
                 }
        
        self.assertDictEqual(twitter_feed_batch.extract_arguments(argv=given),expect)

    def test_no_categories(self):
        """given a set of parameters without explicit categories extract them"""

        given = [sys.path, '--screen-names', 'name_1', 'name_2', 'name_3', 'name_4', '--output-format', 'csv', '--weka-friendly','--include-retweets']

        expect = {
                    '--screen-names' : ['name_1', 'name_2', 'name_3', 'name_4'],
                    '--weka-friendly' : True,
                    '--include-retweets' : True,
                    '--output-format' : 'csv'
                 }
        
        self.assertDictEqual(twitter_feed_batch.extract_arguments(argv=given),expect)

    def test_unmatching_categories(self):
        """given a set of parameters that don't match expect an exception"""

        given = [sys.path, '--screen-names', 'name_1', 'name_2', 'name_3', 'name_4', '--output-format', 'csv', '--append-categories', 'A', 'B','C', '--weka-friendly','--include-retweets']
        
        self.assertRaises(twitter_feed_batch.extract_arguments(argv=given))
    
    def test_unmatching_names(self):
        """given a set of scren names that don't match expect an exception"""

        given = [sys.path, '--screen-names', 'name_1', 'name_2', 'name_4', '--output-format', 'csv', '--append-categories', 'A', 'B','C','D', '--weka-friendly','--include-retweets']
        
        self.assertRaises(twitter_feed_batch.extract_arguments(argv=given))
    
    def test_missing_names(self):
        """given a set of parameters missing the screen names expect an exception"""

        given = [sys.path, '--output-format', 'csv', '--append-categories', 'A', 'B','C', '--weka-friendly','--include-retweets']
        
        self.assertRaises(twitter_feed_batch.extract_arguments(argv=given))
    
    def test_weka_unfriendly(self):
        """given a set of parameters extract them"""

        given = [sys.path, '--screen-names', 'name_1', 'name_2', 'name_3', 'name_4', '--output-format', 'csv', '--append-categories', 'A', 'B','C','D','--include-retweets']

        expect = {
                    '--screen-names' : ['name_1', 'name_2', 'name_3', 'name_4'],
                    '--weka-friendly' : False,
                    '--include-retweets' : True,
                    '--append-categories' : ['A', 'B','C','D'],
                    '--output-format' : 'csv'
                 }
        
        self.assertDictEqual(twitter_feed_batch.extract_arguments(argv=given),expect)
    
    def test_exclude_retweets(self):
        """given a set of parameters extract them"""

        given = [sys.path, '--screen-names', 'name_1', 'name_2', 'name_3', 'name_4', '--output-format', 'csv', '--append-categories', 'A', 'B','C','D', '--weka-friendly']

        expect = {
                    '--screen-names' : ['name_1', 'name_2', 'name_3', 'name_4'],
                    '--weka-friendly' : True,
                    '--include-retweets' : False,
                    '--append-categories' : ['A', 'B','C','D'],
                    '--output-format' : 'csv'
                 }
        
        self.assertDictEqual(twitter_feed_batch.extract_arguments(argv=given),expect)