import csv
import time

PARSED_DBPEDIA_ABSTRACTS_PATH = '../../data/document_base/dbpedia_abstracts.csv'
PARSED_MEDIAWIKI_ABSTRACTS_PATH = '../../data/document_base/mediawiki_abstracts.csv'

class ReadyAbstractExtractor:
    """Extract abstract by name of article from prepared csv abstracts"""

    def __init__(self, path_to_dbpedia, path_to_mediawiki):
        self.path_to_dbpedia = path_to_dbpedia
        self.path_to_mediawiki = path_to_mediawiki

    def extract_abstracts(self, title_of_article:str, dbpedia=True, mediawiki=True) -> tuple[str, str]:

        dbpedia_abstract = self.__extract_abstract_from_csv(title_of_article=title_of_article.replace(' ', '_'),
                                                            path_to_dump=self.path_to_dbpedia) if dbpedia else None

        mediawiki_abstract = self.__extract_abstract_from_csv(title_of_article=title_of_article,
                                                              path_to_dump=self.path_to_mediawiki) if mediawiki else None
        abstracts = {'dbpedia':dbpedia_abstract,
                     'mediawiki':mediawiki_abstract}
        return abstracts

    def __extract_abstract_from_csv(self, title_of_article:str, path_to_dump):
        title_of_article = title_of_article.lower()
        with open(path_to_dump, 'r') as dbpedia:
            reader = csv.reader(dbpedia, delimiter='\t')
            for row in reader:
                abs_name = row[0].lower()
                if abs_name[0] == title_of_article[0]:
                    if abs_name == title_of_article:
                        return row[1]



if __name__ == '__main__':
    abst_extractor = ReadyAbstractExtractor(path_to_dbpedia=PARSED_DBPEDIA_ABSTRACTS_PATH,
                                            path_to_mediawiki=PARSED_MEDIAWIKI_ABSTRACTS_PATH)
    start_time = time.time()
    abss = abst_extractor.extract_abstracts('Alchemy')
    print(f"{abss['dbpedia']} \n{abss['mediawiki']}")

