import unittest
import sys
from phron import twitter_feed_batch

class TestBatchExtraction(unittest.TestCase):
    def test_extract_arguments(self):
        """given a set of parameters extract them"""

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_3', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C','D', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value,twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value]

        expect = {
                    twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4'],
                    twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value : True,
                    twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value : True,
                    twitter_feed_batch._AcceptedArgumentKeys.append_categories.value : ['A', 'B','C','D'],
                    twitter_feed_batch._AcceptedArgumentKeys.output_format.value : 'csv'
                 }
        
        self.assertDictContainsSubset(twitter_feed_batch.extract_arguments(argv=given),expect)

    def test_no_categories(self):
        """given a set of parameters without explicit categories extract them"""

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_3', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value,twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value]

        expect = {
                    twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4'],
                    twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value : True,
                    twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value : True,
                    twitter_feed_batch._AcceptedArgumentKeys.output_format.value : 'csv'
                 }
        
        self.assertDictEqual(twitter_feed_batch.extract_arguments(argv=given),expect)

    def test_unmatching_categories(self):
        """given a set of parameters that don't match expect an exception"""

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_3', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value,twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value]
        
        self.assertRaises(twitter_feed_batch.InvalidArgument, lambda: twitter_feed_batch.extract_arguments(argv=given))
    
    def test_unmatching_names(self):
        """given a set of scren names that don't match expect an exception"""

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C','D', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value,twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value]
        
        self.assertRaises(twitter_feed_batch.InvalidArgument, lambda: twitter_feed_batch.extract_arguments(argv=given))
    
    def test_missing_names(self):
        """given a set of parameters missing the screen names expect an exception"""

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value,twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value]
        
        self.assertRaises(twitter_feed_batch.InvalidArgument, lambda: twitter_feed_batch.extract_arguments(argv=given))

    
    def test_weka_unfriendly(self):
        """given a set of parameters not including --weka-friendly, extract them"""

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_3', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C','D',twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value]

        expect = {
                    twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4'],
                    twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value : False,
                    twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value : True,
                    twitter_feed_batch._AcceptedArgumentKeys.append_categories.value : ['A', 'B','C','D'],
                    twitter_feed_batch._AcceptedArgumentKeys.output_format.value : 'csv'
                 }
        
        self.assertDictContainsSubset(twitter_feed_batch.extract_arguments(argv=given),expect)
    
    def test_exclude_retweets(self):
        """given a set of parameters extract them"""

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_3', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C','D', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value]

        expect = {
                    twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4'],
                    twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value : True,
                    twitter_feed_batch._AcceptedArgumentKeys.include_retweets.value : False,
                    twitter_feed_batch._AcceptedArgumentKeys.append_categories.value : ['A', 'B','C','D'],
                    twitter_feed_batch._AcceptedArgumentKeys.output_format.value : 'csv'
                 }
        
        self.assertDictContainsSubset(twitter_feed_batch.extract_arguments(argv=given),expect)
    
    ## private methods tests
    def test_extract_argument_array_after_key(self):
        """ given an array of arguments test if the trailing array is for key is parsed properly """

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_3', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C','D', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value]

        expect = ['name_1', 'name_2', 'name_3', 'name_4']

        self.assertEqual(twitter_feed_batch._extract_argument_array_after_key(twitter_feed_batch._AcceptedArgumentKeys.screen_names.value,argv=given),expect)
    
    def test_extract_argument_array_after_key_categories(self):
        """ given an array of arguments test if the trailing array is for key is parsed properly """

        given = [sys.path, twitter_feed_batch._AcceptedArgumentKeys.screen_names.value, 'name_1', 'name_2', 'name_3', 'name_4', twitter_feed_batch._AcceptedArgumentKeys.output_format.value, 'csv', twitter_feed_batch._AcceptedArgumentKeys.append_categories.value, 'A', 'B','C','D', twitter_feed_batch._AcceptedArgumentKeys.weka_friendly.value]

        expect = ['A', 'B','C','D']

        self.assertEqual(twitter_feed_batch._extract_argument_array_after_key(twitter_feed_batch._AcceptedArgumentKeys.append_categories.value,argv=given),expect)
    
    def test_valid_screen_names(self):
        """ given an argument dict test that the screen names are valid """
        
        given_valid = {twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4']}

        given_invalid = {}

        self.assertTrue(twitter_feed_batch._valid_screen_names_count(dict=given_valid))

        self.assertFalse(twitter_feed_batch._valid_screen_names_count(dict=given_invalid))
    
    def test_screen_name_and_categories_consistency(self):
        """ given an argument dictionary test that appending categories match the screen names count """

        given_valid = {
                        twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4'],
                        twitter_feed_batch._AcceptedArgumentKeys.append_categories.value : ['A', 'B','C','D']
        }
        
        self.assertTrue(twitter_feed_batch._valid_categories_screen_name(dict=given_valid))
        
        given_invalid_count = {
            twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_2', 'name_3', 'name_4'],
            twitter_feed_batch._AcceptedArgumentKeys.append_categories.value : ['A','C','D']
        }

        self.assertFalse(twitter_feed_batch._valid_categories_screen_name(dict=given_invalid_count))
        
        given_invalid_count_names = {
            twitter_feed_batch._AcceptedArgumentKeys.screen_names.value : ['name_1', 'name_3', 'name_4'],
            twitter_feed_batch._AcceptedArgumentKeys.append_categories.value : ['A', 'B','C','D']
        }
        
        self.assertFalse(twitter_feed_batch._valid_categories_screen_name(dict=given_invalid_count_names))

        