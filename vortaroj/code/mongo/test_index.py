# coding: utf-8

import unittest

import pymongo

from index import Index


class TestIndex(unittest.TestCase):
    def setUp(self):
        connection = pymongo.Connection(safe=True)
        database = connection['index_db']
        database.drop_collection('index')

    def test_should_add_documents_with_name_and_content(self):
        index = Index()
        index.add_document('test', 'this is my first document')
        index.add_document('test2', 'this is my second document')
        self.assertEquals(len(index), 2)
        self.assertEquals(index._documents, set(['test', 'test2']))

    def test_should_automatically_index_when_add_documents(self):
        index = Index()
        index.add_document('test', 'this is my first document')
        index.add_document('test2', 'this is my second document')
        expected_tokens = set(['this', 'is', 'my', 'first', 'second',
                               'document'])
        expected_index = {'this': ['test', 'test2'],
                          'is': ['test', 'test2'],
                          'my': ['test', 'test2'],
                          'first': ['test'],
                          'second': ['test2'],
                          'document': ['test', 'test2'],}
        self.assertEquals(index.tokens(), expected_tokens)
        index_mongo = {d['_id']: d['documents'] for d in index._index.find()}
        self.assertEquals(index_mongo, expected_index)

    def test_should_store_tokens_lowercase(self):
        index = Index()
        index.add_document('doc', 'This IS mY firsT DoCuMeNt')
        expected_tokens = set(['this', 'is', 'my', 'first', 'document'])
        expected_index = {'this': ['doc'],
                          'is': ['doc'],
                          'my': ['doc'],
                          'first': ['doc'],
                          'document': ['doc'],}
        self.assertEquals(index.tokens(), expected_tokens)
        index_mongo = {d['_id']: d['documents'] for d in index._index.find()}
        self.assertEquals(index_mongo, expected_index)

    def test_should_be_able_to_find_by_term(self):
        index = Index()
        index.add_document('doc1', 'this is my first document')
        index.add_document('doc2', 'this is my second document')
        index.add_document('doc3', 'another document')
        self.assertEquals(index.find_by_term('document'),
                          set(['doc1', 'doc2', 'doc3']))
        self.assertEquals(index.find_by_term('DOCUMENT'),
                          set(['doc1', 'doc2', 'doc3']))
        self.assertEquals(index.find_by_term('this'), set(['doc1', 'doc2']))
        self.assertEquals(index.find_by_term('is'), set(['doc1', 'doc2']))
        self.assertEquals(index.find_by_term('my'), set(['doc1', 'doc2']))
        self.assertEquals(index.find_by_term('first'), set(['doc1']))
        self.assertEquals(index.find_by_term('second'), set(['doc2']))
        self.assertEquals(index.find_by_term('another'), set(['doc3']))

    def test_should_be_able_to_find_using_more_than_one_term(self):
        index = Index()
        index.add_document('doc1', 'this is my first document')
        index.add_document('doc2', 'this is my second document')
        index.add_document('doc3', 'another document')
        self.assertEquals(index.find('this document'), set(['doc1', 'doc2']))
        self.assertEquals(index.find('this another'), set())
        self.assertEquals(index.find('a b'), set())
        self.assertEquals(index.find('another'), set(['doc3']))
        self.assertEquals(index.find('first another'), set([]))
