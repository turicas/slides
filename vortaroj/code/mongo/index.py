# coding: utf-8

import pymongo

from tokenizer import tokenize


class Index(object):
    def __init__(self, filename='index.dbm'):
        self._documents = set([])
        connection = pymongo.Connection(safe=True)
        self._index = connection['index_db']['index']

    def __len__(self):
        return len(self._documents)

    def tokens(self):
        return set([d['_id'] for d in self._index.find({}, {'_id': 1})])

    def add_document(self, name, contents):
        self._documents.update([name])
        for token in tokenize(contents):
            token = token.lower()
            result = self._index.find_one({'_id': token}, {'documents': 1})
            if not result:
                documents = [name]
            else:
                documents = set(result['documents'])
                documents.add(name)
            self._index.remove({'_id': token})
            self._index.insert({'_id': token, 'documents': list(documents)})

    def find_by_term(self, term):
        term = term.lower()
        result = self._index.find_one({'_id': term}, {'documents': 1})
        if result is not None:
            return set(result['documents'])
        else:
            return set()

    def find(self, terms):
        results = self._documents.copy()
        for term in tokenize(terms):
            results &= set(self.find_by_term(term))
        return results
