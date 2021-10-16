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

if __name__ == "__main__":
    DATA_PATH = '../../data'
    INDEX_PATH = DATA_PATH + '/index'
    lucene.initVM()
    analyzer = StandardAnalyzer()
    indir = SimpleFSDirectory(Paths.get(INDEX_PATH))
    searcher = IndexSearcher(DirectoryReader.open(indir))

    query = QueryParser("abstract", analyzer).parse("Anarchism")
    MAX = 1000
    hits = searcher.search(query, MAX)

    print(f"Found {hits.totalHits} document(s) that matched query '{query}': ")
    for hit in hits.scoreDocs:
        print (hit.score, hit.doc, hit.toString())
        doc = searcher.doc(hit.doc)
        print(doc.get("abstract").encode("utf-8"))
