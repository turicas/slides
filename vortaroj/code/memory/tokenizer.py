# coding: utf-8

import string
import re


regexp_split = re.compile('([ \t\r\n{}])'.format(re.escape(string.punctuation)))

def tokenize(text):
    #TODO: add option to specify stopwords
    splitted_text = regexp_split.split(text)
    return [token for token in splitted_text if token.strip()]
