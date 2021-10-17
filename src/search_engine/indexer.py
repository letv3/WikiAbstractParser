import lucene
from text_processor.text_processor import TextProcessor

from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
# from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import (IndexOptions, IndexWriter, IndexWriterConfig)
from java.nio.file import Paths



class LuceneIndexer():
    def __init__(self, path_to_abstracts_csv, index_path):
        lucene.initVM()
        self.INDEX_PATH = index_path
        indexDir = SimpleFSDirectory(Paths.get(self.INDEX_PATH))
        self.analyzer = StandardAnalyzer()
        config = IndexWriterConfig(self.analyzer)
        self.writer = IndexWriter(indexDir, config)
        self.path_to_abstracts_csv = path_to_abstracts_csv
        self.text_processor = TextProcessor(self.analyzer)
        self.retrieved_documents = []

    def retrieve_documents_from_csv(self):
        with open(self.path_to_abstracts_csv, 'r') as file:
            for line in file:
                self.retrieved_documents.append(line.split('\t'))
        print(self.retrieved_documents[0])
        return self.retrieved_documents

    def __create_one_document(self, document):
        doc = Document()
        doc.add(Field('id', document[0], StringField.TYPE_STORED))
        doc.add(Field('title', document[1],  StringField.TYPE_STORED))
        abstract = self.text_processor.process_text(document[2])
        doc.add(Field('abstract', abstract, TextField.TYPE_STORED))
        return doc


    def add_all_documents(self):
        for document in self.retrieved_documents:
            doc = self.__create_one_document(document)
            self.writer.addDocument(doc)
        print(f"{self.writer.numRamDocs()} docs found in index")
        self.writer.commit()
        self.writer.close()


if __name__ == '__main__':
    DATA_PATH = '../../data'
    DOCUMENT_BASE_PATH = DATA_PATH + '/document_base/parsed_abstracts.csv'
    INDEX_PATH = DATA_PATH + '/index'

    lucene_indexer = LuceneIndexer(DOCUMENT_BASE_PATH, INDEX_PATH)
    retrieved_docs = lucene_indexer.retrieve_documents_from_csv()
    lucene_indexer.add_all_documents()