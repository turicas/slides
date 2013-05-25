# coding: utf-8

import unittest
from tokenizer import tokenize


class TestTokenize(unittest.TestCase):
    def test_should_receive_string_and_return_a_list_of_words(self):
        result = tokenize('this is a test')
        expected = ['this', 'is', 'a', 'test']
        self.assertEquals(result, expected)

    def test_should_not_remove_punctuaion(self):
        result = tokenize('this is a test.')
        self.assertIn('.', result[-1])

    def test_should_split_punctuation_of_words(self):
        result = tokenize('this is a test.')
        expected = ['this', 'is', 'a', 'test', '.']
        self.assertEquals(result, expected)
