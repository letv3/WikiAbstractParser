from src.parser.wikipage_parser import AbstractExtractor, write_abstracts_to_csv
from src.text_processor.text_processor import TextProcessor
from src.search_engine.retriever import Retriever
from src.search_engine.indexer import LuceneIndexer

import datetime, shutil, os.path as path

DATA_PATH = '../../data'

class CLI:
    def __init__(self):

        self.PARSED_ABSTRACTS_PATH = DATA_PATH + '/document_base/parsed_abstracts.csv'
        self.PARSED_MEDIAWIKI_ABSTRACTS_PATH = DATA_PATH + '/document_base/mediawiki_abstracts.csv'
        self.INDEX_PATH = DATA_PATH + '/index'
        pass

    def launch(self):
        print("Hello this is wiki abstract search engine :), to exit press 'x'")
        print("Want to launch parser and index new documents?[Y/N]")
        if self.__handle_response():
            if path.exists(self.INDEX_PATH):
                # remove index if exists to write a new one
                shutil.rmtree(self.INDEX_PATH)
            num_of_pages = int(input("enter the number of pages to parse, integer pls: "))
            self.__launch_parser(num_of_pages)
            self.__launch_indexer()
        while True:

        pass

    def __launch_parser(self, number_of_pages_to_parse):
        parser = AbstractExtractor(number_of_abstracts=number_of_pages_to_parse)
        print(f"started parsing: {datetime.datetime.now()}")
        selfparsed_abstracts = parser.parse_abstracts_from_wiki_articles()
        write_abstracts_to_csv(selfparsed_abstracts, self.PARSED_ABSTRACTS_PATH)
        mediawiki_parsed_abstracts = parser.parse_abstracts_from_wiki_abstracts()
        write_abstracts_to_csv(mediawiki_parsed_abstracts, self.PARSED_MEDIAWIKI_ABSTRACTS_PATH)

    def __launch_indexer(self):
        indexer = LuceneIndexer(path_to_abstracts_csv=self.PARSED_ABSTRACTS_PATH,
                                index_path=self.INDEX_PATH)
        retrieved_docs = indexer.retrieve_documents_from_csv()
        indexer.add_all_documents()

    def __launch_retriever(self):
        return Retriever(self.INDEX_PATH)


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


