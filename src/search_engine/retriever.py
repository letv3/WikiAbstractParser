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
                  f"abstract: {doc.get('abstract')}")
            print("-------------------------")

    def perform_query(self, text, max=5, display=True):
        query = QueryParser("abstract", self.analyzer).parse(text)
        hits = self.searcher.search(query, max)
        if display:
            self.__display_results(hits, query)
        first_hit = self.searcher.doc(hits.scoreDocs[0].doc)
        first_doc_tuple = {'title': first_hit.get('title'),
                           'abstract': first_hit.get('abstract')
                           }
        return first_doc_tuple


if __name__ == "__main__":
    lucene.initVM()
    DATA_PATH = '../../data'
    INDEX_PATH = DATA_PATH + '/index'
    retriever = Retriever(INDEX_PATH)
    doc = retriever.perform_query('greates of Greek warriors', display=True)
    # print(doc['title'])