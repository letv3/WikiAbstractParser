import os, re, sys, lucene
# from lucene import SimpleFSDirectory

from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
# from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import (IndexOptions, IndexWriter,
                                     IndexWriterConfig)
from java.nio.file import Paths
# from org.apache.lucene.analysis.standard import StandardAnalyzer
# from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# from org.apache.lucene.document import Document, Field, StringField, TextField, IntField
# from org.apache.lucene.store import SimpleFSDirectory

class LuceneIndexer():
    def __init__(self, path_to_abstracts_csv, writer):
        self.path_to_abstracts_csv = path_to_abstracts_csv
        self.writer = writer
        self.retrived_documents = []


    def retrive_documents(self):
        with open(self.path_to_abstracts_csv, 'r') as file:
            for line in file:
                self.retrived_documents.append(line.split('\t'))
        print(self.retrived_documents[0])
        return self.retrived_documents

    def __create_one_document(self, document):
        doc = Document()
        doc.add(Field('id', document[0], StringField.TYPE_STORED))
        doc.add(Field('title', document[1],  StringField.TYPE_STORED))
        doc.add(Field('abstract', document[2], TextField.TYPE_STORED))
        return doc


    def add_all_documents(self):
        for document in self.retrived_documents:
            doc = self.__create_one_document(document)
            self.writer.addDocument(doc)
        print(f"{writer.numRamDocs()} docs found in index")
        self.writer.commit()
        self.writer.close()


if __name__ == '__main__':
    DATA_PATH = '../../data'
    DOCUMENT_BASE_PATH = DATA_PATH + '/document_base/parsed_abstracts.csv'
    INDEX_PATH = DATA_PATH + '/index'
    # DIRECTORY_PATH = '../../data/search_engine_dir'


    lucene.initVM()
    indexDir = SimpleFSDirectory(Paths.get(INDEX_PATH))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(indexDir, config)

    lucyne_indexer = LuceneIndexer(DOCUMENT_BASE_PATH, writer)
    retrived_docs = lucyne_indexer.retrive_documents()

    lucyne_indexer.add_all_documents()
    # print(f"{writer.numRamDocs()} docs found in index")