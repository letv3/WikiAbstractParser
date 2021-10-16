import re, csv, datetime

PATH_TO_FILE = '../../data/enwiki-latest-pages-articles1.xml-p1p41242'
SMALL_FILE = '../../data/wikidata-pagesample.xml'


class AbstractExtractor:

    def __init__(self,
                 path_to_wiki_articles='../../data/enwiki-latest-pages-articles1.xml-p1p41242',
                 path_to_wiki_abstracts='../../data/enwiki-latest-abstract.xml',
                 number_of_abstracts=100):
        self.path_to_wiki_articles = path_to_wiki_articles
        self.path_to_wiki_abstracts = path_to_wiki_abstracts
        self.number_of_abstracts = number_of_abstracts

    def parse_abstract_from_wiki_articles(self):
        title_pattern = re.compile("\s*<title>([^\n]*)</title>\s*").match
        abstract_pattern = re.compile("'''([^\n]*)").match
        header_pattern = re.compile("(={1,6})([^\n]+?)(={1,6})[ \t]*(\n|\Z)").match
        parsed_pages = []
        abstract_parsing = False
        with open(self.path_to_wiki_articles) as file:
            page_abstract = ''
            idx = 0
            for line in file:
                if idx == self.number_of_abstracts:
                    break

                if line == '\n':
                    continue  # skip new line line

                if title := title_pattern(line):
                    title_str = title.group(1)
                elif abs := abstract_pattern(line):
                    abstract_parsing = True
                    page_abstract = abs.group(1)
                elif abstract_parsing and (not header_pattern(line)):
                    page_abstract += line
                elif header_pattern(line) and abstract_parsing:
                    abstract_parsing = False
                    idx += 1
                    parsed_pages.append((title_str, page_abstract))
        return parsed_pages

    def parse_abstracts_from_wiki_abstracts(self):
        title_pattern = re.compile('(<title>Wikipedia: )([^\n]*)(</title>)')
        abstract_pattern = re.compile('(<abstract>)([^\n]*)(</abstract>)')
        parsed_abstracts = []
        with open(self.path_to_wiki_abstracts) as file:
            idx = 0
            for line in file:
                if idx == self.number_of_abstracts: break
                line = file.readline()
                if title := re.match(title_pattern, line):
                    title_text = title.group(2)
                elif abstract := re.match(abstract_pattern, line):
                    text_abstract = abstract.group(2)
                    parsed_abstracts.append((title_text, text_abstract))
                    idx += 1
        return parsed_abstracts


def write_abstracts_to_csv(parsed_abstracts, prepared=True):
    path_to_write_docs = '../../data/document_base/wiki_abstracts.csv' if prepared \
        else '../../data/document_base/parsed_abstracts.csv'
    print(path_to_write_docs)
    with open(path_to_write_docs, 'w', newline='') as prepared_abs_file:
        filed_names = ['docID', 'title', 'abstract']
        writer = csv.writer(prepared_abs_file, delimiter='\t')
        for idx, abstract in enumerate(parsed_abstracts):
            writer.writerow([str(idx)] + list(abstract))


if __name__ == "__main__":
    abs_extractor = AbstractExtractor();
    print(f"started parsing: {datetime.datetime.now()}")
    parsed_abstracts = abs_extractor.parse_abstract_from_wiki_articles()
    print(f"finished parsing and started writing to file: {datetime.datetime.now()}")
    write_abstracts_to_csv(parsed_abstracts, prepared=False)
    print(f"finished: {datetime.datetime.now()}")
