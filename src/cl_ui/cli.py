import os

from src.parser.wikipage_parser import AbstractExtractor, write_abstracts_to_csv
from src.text_processor.text_processor import TextProcessor
from src.search_engine.retriever import Retriever
from src.search_engine.indexer import LuceneIndexer
from src.comparator.abstract_exractor import ReadyAbstractExtractor
from src.comparator.comparator import TextSimilarityComparator

import datetime, time, shutil, os.path as path
import lucene

# DATA_PATH = '../../data'
DATA_PATH = 'data'
DOCUMENT_DIR = "/document_base"


class CLI:
    def __init__(self):
        self.DOCUMENT_BASE_PATH = DATA_PATH + DOCUMENT_DIR
        self.INDEX_PATH = DATA_PATH + '/index'
        lucene.initVM()
        if os.path.exists(self.DOCUMENT_BASE_PATH):
            self.indexer = LuceneIndexer(self.DOCUMENT_BASE_PATH, self.INDEX_PATH)
            self.retriever = Retriever(self.INDEX_PATH)



    def launch(self):
        print("Hello this is wiki abstract search engine :), to exit press 'x'")
        print("Want to launch parser again and index new documents? (It will take some time)[Y/N]")
        if parse:=self.__handle_response():
            start_index_time = time.time()
            self.__create_new_index()
            print(f"time elapsed for indexing: {time.time() - start_index_time}")
        # if not parse: lucene.initVM()
        retriever = Retriever(self.INDEX_PATH)
        similarity_comparator = TextSimilarityComparator()
        while True:
            print(f"Enter the word you want to find abstract for ('X' for exit)")
            res = self.__handle_response()
            first_hit = retriever.perform_query(res)
            print("Do u want to display similarity with dbpedia and mediawiki abstract for the first query?[Y/N]")
            if res:= self.__handle_response() and first_hit is not None:
                    self.__display_similarity(first_hit, similarity_comparator)
            else:
                continue
        pass

    def __display_similarity(self, first_hit, similarity_comparator):


        print(f"Similarity with dbpedia abstract: {orig_dbpedia_similarity}\n"
              f"Similarity with mediawiki abstract: {orig_mediawiki_similarity}")
        print(f"time elapsed: {time.time() - start_time}")


    def __create_new_index(self):
        if path.exists(self.INDEX_PATH):
            # remove index if exists to write a new one
            shutil.rmtree(self.INDEX_PATH)
        num_of_pages = int(input("enter the number of pages to parse, integer pls: "))
        self.__launch_parser(num_of_pages)
        self.__launch_indexer()

    def __launch_parser(self, number_of_pages_to_parse):
        parser = AbstractExtractor(path_to_wiki_articles=self.MEDIAWIKI_ARTICLES_DUMPFILE_PATH,
                                   path_to_wiki_abstracts=self.MEDIAWIKI_ABSTRACTS_DUMPFILE_PATH,
                                   path_to_dbpedia_abstracts=self.DBPEDIA_ABSTRACTS_DUMPFILE_PATH)
        print(f"started parsing: {datetime.datetime.now()}")
        selfparsed_abstracts = parser.parse_abstracts_from_wiki_articles()
        write_abstracts_to_csv(selfparsed_abstracts, self.PARSED_ABSTRACTS_PATH)
        mediawiki_parsed_abstracts = parser.parse_abstracts_from_wiki_abstracts()
        write_abstracts_to_csv(mediawiki_parsed_abstracts, self.PARSED_MEDIAWIKI_ABSTRACTS_PATH)

    def __launch_indexer(self):
        indexer = LuceneIndexer(path_to_abstracts_csv=self.PARSED_ABSTRACTS_PATH,
                                index_path=self.INDEX_PATH)
        indexer.create_index()


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


