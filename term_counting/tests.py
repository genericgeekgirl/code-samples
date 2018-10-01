from word_count import get_counter, get_top_words, get_json
import unittest
from collections import Counter, OrderedDict
import json

class TestUnit(unittest.TestCase):

    counter = Counter({'to': 5, 'he': 4, 'a': 4, 'and': 3, 'some': 3, 'out': 3, 'get': 3, 'his': 3, 'hand': 3, 'you': 3, 'not': 2, 'at': 2, 'have': 2, 'filberts': 2, 'boy': 2, 'once': 2, 'all': 1, 'there': 1, 'stood': 1, 'give': 1, 'into': 1, 'them': 1, 'single': 1, 'satisfied': 1, 'yet': 1, 'again': 1, 'given': 1, 'said': 1, 'fistful': 1, 'much': 1, 'perhaps': 1, 'with': 1, 'began': 1, 'nuts': 1, 'your': 1, 'that': 1, 'unable': 1, 'too': 1, 'then': 1, 'taken': 1, 'unwilling': 1, 'was': 1, 'more': 1, 'be': 1, 'draw': 1, 'may': 1, 'do': 1, 'permission': 1, 'easily': 1, 'time': 1, 'pitcher': 1, 'took': 1, 'but': 1, 'half': 1, 'put': 1, 'such': 1, 'disappointed': 1, 'the': 1, 'filbert': 1, 'great': 1, 'attempt': 1, 'could': 1, 'cry': 1, 'up': 1, 'will': 1, 'mother': 1, 'vexed': 1, 'other': 1, 'my': 1})
    

    def test_get_counter(self):
        filename = 'aesop.txt'
        counter = get_counter(filename)
        self.assertEqual(counter, self.counter)


    def test_get_top_words(self):
        results = get_top_words(self.counter)
        expected_results = ("to - 5\nhe - 4\na - 4\nhis - 3\nand - 3\nsome - 3\nout - 3\nget - 3\nyou - 3\nhand - 3")
        self.assertEqual(results, expected_results)


    def test_get_json(self):
        results = get_json(self.counter)
        expected_results = {"a": 4, "again": 1, "all": 1, "and": 3, "at": 2, "attempt": 1, "be": 1, "began": 1, "boy": 2, "but": 1, "could": 1, "cry": 1, "disappointed": 1, "do": 1, "draw": 1, "easily": 1, "filbert": 1, "filberts": 2, "fistful": 1, "get": 3, "give": 1, "given": 1, "great": 1, "half": 1, "hand": 3, "have": 2, "he": 4, "his": 3, "into": 1, "may": 1, "more": 1, "mother": 1, "much": 1, "my": 1, "not": 2, "nuts": 1, "once": 2, "other": 1, "out": 3, "perhaps": 1, "permission": 1, "pitcher": 1, "put": 1, "said": 1, "satisfied": 1, "single": 1, "some": 3, "stood": 1, "such": 1, "taken": 1, "that": 1, "the": 1, "them": 1, "then": 1, "there": 1, "time": 1, "to": 5, "too": 1, "took": 1, "unable": 1, "unwilling": 1, "up": 1, "vexed": 1, "was": 1, "will": 1, "with": 1, "yet": 1, "you": 3, "your": 1}
        self.assertEqual(json.loads(results), expected_results)
        

        
if __name__ == '__main__':
    unittest.main()
