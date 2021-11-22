import os.path
import glob, re, time

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
    def __init__(self, path_to_document_base, index_path):
        lucene.initVM()
        self.INDEX_PATH = index_path
        indexDir = SimpleFSDirectory(Paths.get(self.INDEX_PATH))
        self.analyzer = StandardAnalyzer()
        config = IndexWriterConfig(self.analyzer)
        self.writer = IndexWriter(indexDir, config)
        self.text_processor = TextProcessor(self.analyzer)

        self.path_to_document_base = path_to_document_base
        self.retrieved_documents = 0

    # todo read batch - write batch
    # make function for index creation on 3 folders (document_base, dbpedia, default_wiki)
    # use this fucntion

    def create_index(self, only_parsed=False):
        folders = {
            'parsed_abstract': "parsed_abstracts",
            'default': "default_wiki",
            'dbpedia': "dbpedia"
        }
        whole_start = time.time()
        for mode, folder in folders.items():
            path_to_files = self.path_to_document_base + "/" + folder
            files_to_parse = self.__get_csv_filenames(path_to_files)
            start_time = time.time()
            num_of_docs = self.__add_files_to_index(file_names=files_to_parse, type=mode)
            self.retrieved_documents += num_of_docs
            print(f"------------------ FOLDER {folder} FINISHED ------------------")
            print(f"added: {num_of_docs} docs | finished for {(time.time() - start_time):.4f}")
            print(f"------------------ ------------------------ ------------------")
            if only_parsed: break
        print(f"SUMMARY:  added: {self.retrieved_documents} | elapsed: {(time.time() - whole_start):.4f}")
        self.commit_and_close()

    def __add_files_to_index(self, file_names, type):
        num_of_docs = 0
        for idx, file_name in enumerate(file_names):
            docs = self.__retrieve_documents_from_single_csv(file_name)
            self.add_batch_documents(documents=docs, type=type)
            num_of_docs += len(docs)
            print(f"{idx} document retrieved: {len(docs)}")
        return num_of_docs

    def __get_csv_filenames(self, path):
        all_files = glob.glob(f"{path}/*.csv")
        csv_files = []
        for file_name in all_files:
            if re.match(r"(.*)(?=(\.csv))", file_name):
                csv_files.append(file_name)
            else:
                continue
        return csv_files

    def __retrieve_documents_from_single_csv(self, filename):
        retrieved_docs = []
        with open(filename, 'r') as file:
            for line in file:
               retrieved_docs.append(line.split('\t'))
        return retrieved_docs

    def add_batch_documents(self, documents, type='parsed_abstract'):
        for document in documents:
            doc = self.__create_one_document(document, type=type)
            self.writer.addDocument(doc)
        # print(f"{self.writer.numRamDocs()} docs RAM")

    def __create_one_document(self, document, type='parsed_abstract'):
        doc = Document()
        # doc.add(Field('id', document[0], StringField.TYPE_STORED))
        doc.add(Field('title', document[0],  TextField.TYPE_STORED))
        abstract = self.text_processor.process_text(document[1])
        doc.add(Field('abstract', abstract, TextField.TYPE_STORED))
        doc.add(Field('type', type,  StringField.TYPE_STORED))
        # doc.add(Field('default_wiki_abstract', '', TextField.TYPE_STORED))
        # doc.add(Field('dbpedia_abstract', '', TextField.TYPE_STORED))
        return doc



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


if __name__ == '__main__':
    DEFAULT_DIR = "../../data"
    DOCUMENT_DIR = "/document_base"
    DOCUMENT_BASE_PATH = DEFAULT_DIR + DOCUMENT_DIR
    INDEX_PATH = DEFAULT_DIR + '/index'

    if os.path.exists(DOCUMENT_BASE_PATH):
        lucene_indexer = LuceneIndexer(DOCUMENT_BASE_PATH, INDEX_PATH)
        # retrieved_docs = lucene_indexer.create_initial_index()
        # lucene_indexer.add_preparsed_abstracts_to_index(DEFAULT_DIR + DOCUMENT_DIR)
        lucene_indexer.create_index()
        # print(f"all docs: {lucene_indexer.retrieved_documents}")
        # lucene_indexer.commit_and_close()



    # lucene_indexer.add_batch_documents()
    # lucene_indexer.commit_and_close()