import sys
import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

# from src.comparator.comparator import TextSimilarityComparator


class Retriever:
    def __init__(self, index_path):
        self.INDEX_PATH = index_path
        self.analyzer = StandardAnalyzer()
        self.indir = SimpleFSDirectory(Paths.get(self.INDEX_PATH))
        self.searcher = IndexSearcher(DirectoryReader.open(self.indir))

    def __display_results(self, hits, query):
        print(f"Found {hits.totalHits} document(s) that matched query '{query}': ")
        for hit in hits.scoreDocs:
            print(hit.toString())
            doc = self.searcher.doc(hit.doc)

            print(f"title: {doc.get('title')} \n"
                  f"abstract: {doc.get('abstract')}\n"
                  f"default_abstract: {doc.get('default_abstract')}\n"
                  f"default_similarity: {doc.get('default_similarity')}\n"
                  f"dbpedia_abstract: {doc.get('dbpedia_abstract')}\n"
                  f"dbpedia_similarity: {doc.get('dbpedia_similarity')}\n")
            print("-------------------------")

    def perform_query(self, text, max=5, type='parsed_abstract', display=True):
        # if type != 'parsed_abstract':
        #     command = f'title:"{text}" AND type:{type}'
        # else:
        #     command = f'abstract:"{text}" AND type:{type}'

        # query = QueryParser("abstract", self.analyzer).parse(f'abstract:"{text}" AND type:{type}')
        query = QueryParser("abstract", self.analyzer).parse(text)
        hits = self.searcher.search(query, max)
        if display:
            self.__display_results(hits, query)
        try:
            first_hit = self.searcher.doc(hits.scoreDocs[0].doc)
            return first_hit
        except:
            print('havent find anything')
            return

    # def get_numDocs(self):
    #     scoredocs = self.searcher.search(QueryParser("abstract", self.analyzer).parse(".*.")).scoreDocs
    #     return len(scoredocs)


if __name__ == "__main__":
    lucene.initVM()
    DATA_PATH = '../../data'
    INDEX_PATH = DATA_PATH + '/index_combined'
    retriever = Retriever(INDEX_PATH)

    # doc = retriever.perform_query('Anarchism', display=True, max=10)
    # dbpedia_doc = retriever.perform_query(doc['title'], type='dbpedia', display=True, max=1)
    # default_doc = retriever.perform_query(doc['title'], type='default', display=True, max=1)
