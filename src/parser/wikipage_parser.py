import re, csv, datetime

MEDIAWIKI_ARTICLES_DUMPFILE_PATH = 'data/enwiki-latest-pages-articles1.xml'
MEDIAWIKI_ABSTRACTS_DUMPFILE_PATH = 'data/enwiki-latest-abstract.xml'
DBPEDIA_ABSTRACTS_DUMPFILE_PATH = '/data/long-abstracts_lang=en.ttl'

PARSED_DBPEDIA_ABSTRACTS_PATH = '../../data/document_base/dbpedia/dbpedia_abstracts.csv'
PARSED_MEDIAWIKI_ABSTRACTS_PATH = '../../data/document_base/mediawiki_abstracts.csv'
PARSED_ABSTRACTS_PATH = '../../data/document_base/parsed_abstracts.csv'

WRITE_PATH = [PARSED_ABSTRACTS_PATH, PARSED_MEDIAWIKI_ABSTRACTS_PATH]

class AbstractExtractor:

    def __init__(self,
                 path_to_wiki_articles='../../data/enwiki-latest-pages-articles1.xml',
                 path_to_wiki_abstracts='../../data/enwiki-latest-abstract.xml',
                 path_to_dbpedia_abstracts = '../../data/long-abstracts_lang=en.ttl',
                 number_of_abstracts=1000):
        self.path_to_wiki_articles = path_to_wiki_articles
        self.path_to_wiki_abstracts = path_to_wiki_abstracts
        self.path_to_dbpedia_long_abstracts = path_to_dbpedia_abstracts
        self.number_of_abstracts = number_of_abstracts

    def parse_abstracts_from_wiki_articles(self):
        title_pattern = re.compile("\s*<title>([^\n]*)</title>\s*").match
        abstract_pattern = re.compile("'''([^\n]*)").match
        header_pattern = re.compile("(={1,6})([^\n]+?)(={1,6})[ \t]*(\n|\Z)").match
        parsed_pages = []
        abstract_parsing = False
        with open(self.path_to_wiki_articles) as file:
            abstract_text = ''
            idx = 0
            for line in file:
                # if idx == self.number_of_abstracts:
                #     break

                if line == '\n':
                    continue  # skip new line line

                if title := title_pattern(line):
                    title_text = title.group(1)
                elif abs := abstract_pattern(line):
                    abstract_parsing = True
                    abstract_text = abs.group(1)
                elif abstract_parsing and (not header_pattern(line)):
                    abstract_text += line
                elif abstract_parsing and header_pattern(line):
                    abstract_parsing = False
                    idx += 1
                    if idx % 1000 == 0: print(f"parsed: {idx} time: {datetime.datetime.now()}")
                    parsed_pages.append((title_text, abstract_text))
        return parsed_pages

    def parse_abstracts_from_wiki_abstracts(self):
        title_pattern = re.compile('(<title>Wikipedia: )([^\n]*)(</title>)')
        abstract_pattern = re.compile('(<abstract>)([^\n]*)(</abstract>)')
        parsed_abstracts = []
        with open(self.path_to_wiki_abstracts) as file:
            idx = 0
            for line in file:
                # if idx == self.number_of_abstracts: break
                line = file.readline()
                if title := re.match(title_pattern, line):
                    title_text = title.group(2)
                elif abstract := re.match(abstract_pattern, line):
                    text_abstract = abstract.group(2)
                    parsed_abstracts.append((title_text, text_abstract))
                    idx += 1
                    if idx % 1000 == 0: print(f"parsed: {idx} time: {datetime.datetime.now()}")
        return parsed_abstracts

    def parse_dbpedia_abstracts(self):
        title_pattern = re.compile(r"^<http:\/\/dbpedia\.org\/resource\/([^\>]*)> <")
        abstract_pattern = re.compile(r'"([^"]*)"')
        parsed_abstracts = []
        with open(self.path_to_dbpedia_long_abstracts) as file:
            idx = 0
            for line in file:
                if title := title_pattern.match(line):
                    title_text = title.group(1)
                    abstract_text = abstract_pattern.search(line).group(1)
                    idx += 1
                    parsed_abstracts.append((title_text, abstract_text))
                # if idx == 10: break
                if idx % 1000 == 0: print(f"parsed: {idx} time: {datetime.datetime.now()}")
        return parsed_abstracts


def write_abstracts_to_csv(parsed_abstracts, path_to_write_docs, add_index=True):
    with open(path_to_write_docs, 'w', newline='') as prepared_abs_file:
        writer = csv.writer(prepared_abs_file, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar=' ')
        for idx, abstract in enumerate(parsed_abstracts):
            abstract = [abstract[0], abstract[1].replace('\n', ' ')]
            writer.writerow(abstract)
            if idx % 10000 == 0: print(f"{idx} document writen")


if __name__ == "__main__":
    abs_extractor = AbstractExtractor()
    print(f"started parsing: {datetime.datetime.now()}")
    # #parse abstracts from articles dump
    selfparsed_abstracts = abs_extractor.parse_abstracts_from_wiki_articles()
    write_abstracts_to_csv(selfparsed_abstracts, PARSED_ABSTRACTS_PATH)
    # # extract abstracts from mediawiki dump
    # mediawiki_parsed_abstracts = abs_extractor.parse_abstracts_from_wiki_abstracts()
    # write_abstracts_to_csv(mediawiki_parsed_abstracts, PARSED_MEDIAWIKI_ABSTRACTS_PATH)
    # # parse abstracts from dbpedia and write to csv
    # abss = abs_extractor.parse_dbpedia_abstracts()
    # write_abstracts_to_csv(abss, PARSED_DBPEDIA_ABSTRACTS_PATH)
    print(f"finished: {datetime.datetime.now()}")
