import os.path
import glob

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
    def __init__(self, path_to_abstracts_dir, index_path):
        lucene.initVM()
        self.INDEX_PATH = index_path
        indexDir = SimpleFSDirectory(Paths.get(self.INDEX_PATH))
        self.analyzer = StandardAnalyzer()
        config = IndexWriterConfig(self.analyzer)
        self.writer = IndexWriter(indexDir, config)
        self.text_processor = TextProcessor(self.analyzer)

        self.path_to_abstracts_dir = path_to_abstracts_dir
        self.csv_file_names = self.__get_csv_filenames()
        self.retrieved_documents = 0

    # todo read batch - write batch
    # after finished all parsed_abstracts continue to default_wiki_abstracts and dbpedia_abstracts
    # get title of abstract, retrive parsed abstract as document, add as a new text field

    def create_initial_index(self):
        for file_name in self.csv_file_names:
            # path = self.path_to_abstracts_dir + '/' + file_name
            docs = self.retrieve_documents_from_single_csv(file_name)
            self.add_batch_documents(documents=docs)
            self.retrieved_documents += len(docs)
        return self.retrieved_documents

    def retrieve_documents_from_single_csv(self, filename):
        retrieved_docs = []
        with open(filename, 'r') as file:
            for line in file:
               retrieved_docs.append(line.split('\t'))
        # print(self.retrieved_documents[0])
        return retrieved_docs

    def __create_one_document(self, document):
        doc = Document()
        # doc.add(Field('id', document[0], StringField.TYPE_STORED))
        doc.add(Field('title', document[0],  StringField.TYPE_STORED))
        abstract = self.text_processor.process_text(document[1])
        doc.add(Field('abstract', abstract, TextField.TYPE_STORED))
        doc.add(Field('default_wiki_abstract', '', TextField.TYPE_STORED))
        doc.add(Field('dbpedia_abstract', '', TextField.TYPE_STORED))
        return doc


    def add_batch_documents(self, documents):
        for document in documents:
            doc = self.__create_one_document(document)
            self.writer.addDocument(doc)
        print(f"{self.writer.numRamDocs()} docs found in index")

    def commit_and_close(self):
        self.writer.commit()
        self.writer.close()

    # def add_all_documents(self):
    #     # todo save id to memory to not update 2 time index
    #     for document in self.retrieved_documents:
    #         doc = self.__create_one_document(document)
    #         self.writer.addDocument(doc)
    #     print(f"{self.writer.numRamDocs()} docs found in index")
    #     self.writer.commit()
    #     self.writer.close()

    def __get_csv_filenames(self):
        csv_files = glob.glob(f"{self.path_to_abstracts_dir}/*.csv")
        return csv_files


if __name__ == '__main__':
    DEFAULT_DIR = "../../data"
    DOCUMENT_DIR = "/document_base"
    PARSED_CSV_DIR = "/parsed_abstracts"
    DOCUMENT_BASE_PATH = DEFAULT_DIR + DOCUMENT_DIR + PARSED_CSV_DIR
    INDEX_PATH = DEFAULT_DIR + '/index'

    if os.path.exists(DOCUMENT_BASE_PATH):
        lucene_indexer = LuceneIndexer(DOCUMENT_BASE_PATH, INDEX_PATH)
        retrieved_docs = lucene_indexer.create_initial_index()
        print(f"all docs: {lucene_indexer.retrieved_documents}")
        lucene_indexer.commit_and_close()



    # lucene_indexer.add_batch_documents()
    # lucene_indexer.commit_and_close()