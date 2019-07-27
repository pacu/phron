import unittest

from phron import text_sanitizer

class TestSanitizer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_weka_sanitizer_quoting(self):
        """ given a text with quotes, escape them """
        given = '""No es posible que no le podamos garantizar dignidad a los que toda su vida trabajaron. Vamos a recomponer el ingreso de los jubilados. Y vamos a hacer una ley que diga que los jubilados no pagan los medicamentos y el Estado los va a subsidiar"'
        expect = "No es posible que no le podamos garantizar dignidad a los que toda su vida trabajaron. Vamos a recomponer el ingreso de los jubilados. Y vamos a hacer una ley que diga que los jubilados no pagan los medicamentos y el Estado los va a subsidiar"
        
        self.assertEqual(expect,text_sanitizer.sanitize_weka(given),"Sanitized string is not what weka would expect it to be")

    def test_weka_sanitizer_grave_accent(self):
        """ given a text with a grave accent, escape them """
        given = "that sweater is Chris'" 
        expect = "that sweater is Chris"
        self.assertEqual(expect,text_sanitizer.sanitize_weka(given),"Sanitized string is not what weka would expect it to be")

    def test_weka_sanitizer_newline(self):
        """given a text with new lines replace them with blank spaces"""

        given = "this is\na text\nwith many\n lines"
        expect = "this is a text with many  lines"
        self.assertEqual(expect,text_sanitizer.sanitize_weka(given),"Sanitized string is not what weka would expect it to be")
    
    def test_weka_sanitizer_replace_separator(self):
        """given a text with a separator char, replace its occurrences with blank spaces"""

        given = "this is, a text, with many, lines"
        expect = "this is  a text  with many  lines"        
        self.assertEqual(expect,text_sanitizer.sanitize_weka(given, remove_separator=","),"Sanitized string is not what weka would expect it to be")
        
if __name__ == '__main__':
    unittest.main
