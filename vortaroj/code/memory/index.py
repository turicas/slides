# coding: utf-8

from tokenizer import tokenize


class Index(object):
    def __init__(self):
        self._documents = set([])
        self._index = {}

    def __len__(self):
        return len(self._documents)

    def tokens(self):
        return set(self._index.keys())

    def add_document(self, name, contents):
        self._documents.update([name])
        for token in tokenize(contents):
            token = token.lower()
            if token not in self._index:
                self._index[token] = set([name])
            else:
                # these 3 lines are not needed when using `dict`
                documents = self._index[token]
                documents.add(name)
                self._index[token] = documents

    def find_by_term(self, term):
        term = term.lower()
        try:
            return self._index[term]
        except KeyError:
            return set()

    def find(self, terms):
        results = self._documents.copy()
        for term in tokenize(terms):
            results &= self.find_by_term(term)
        return results
