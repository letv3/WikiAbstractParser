import os

from src.search_engine.retriever import Retriever
from src.search_engine.indexer import LuceneIndexer

import datetime, time, shutil, os.path as path
import lucene

# DATA_PATH = '../../data'
DATA_PATH = 'data'
DOCUMENT_DIR = "/document_base/combined_abstracts"


class CLI:
    def __init__(self):
        self.DOCUMENT_BASE_PATH = DATA_PATH + DOCUMENT_DIR
        self.INDEX_PATH = DATA_PATH + '/index_combined'
        lucene.initVM()
        if os.path.exists(self.DOCUMENT_BASE_PATH):
            self.indexer = LuceneIndexer(self.DOCUMENT_BASE_PATH, self.INDEX_PATH)
            self.retriever = Retriever(self.INDEX_PATH)



    def launch(self):
        print("Hello this is wiki abstract search engine :), to exit press 'x'")
        print("Want to launch index documents again? (It will take some time)[Y/N]")
        if parse:=self.__handle_response():
            start_index_time = time.time()
            self.__create_new_index()
            print(f"time elapsed for indexing: {time.time() - start_index_time}")
        # if not parse: lucene.initVM()
        while True:
            print(f"Enter the word you want to find abstract for ('X' for exit)")
            res = self.__handle_response()
            first_hit = self.retriever.perform_query(res)
        pass

    def __create_new_index(self):
        if path.exists(self.INDEX_PATH):
            # remove index if exists to write a new one
            shutil.rmtree(self.INDEX_PATH)
        self.indexer.create_index()

    # def __launch_parser(self, number_of_pages_to_parse):
    #     pass
    #
    # def __launch_indexer(self):
    #     self.indexer.create_index()


    def __handle_response(self):
        response = input()
        response = response.upper()
        if response == 'Y':
            return True
        elif response == 'N':
            return False
        elif response == 'X':
            print("Thats all, thank for using!")
            exit()
        else:
            return response


