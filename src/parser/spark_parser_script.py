import time, os, glob,re

import pyspark.sql.functions as sparkfunctions
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark import SparkContext


def check_object(obj):
    if isinstance(obj, str):
        if obj != '':
            return obj
    return ''


def parse_wiki_articles_file(spark, path):
    abstract_pattern = r"'''([^\=]*)(?=(={1,6})([^\n]+?)(={1,6})[ \t]*(\n|\Z))"
    customSchema = StructType([
        StructField('title', StringType()),
        StructField('revision', StructType([
            StructField('text', StructType([
                StructField('_VALUE', StringType())
            ]))
        ]))
    ])
    df = spark.read.format('com.databricks.spark.xml')\
        .options(rowTag='page').load(path, schema=customSchema)
    all_abstracts_rdd = df.rdd.map(
        lambda loop: (
            loop['title'].replace('Wikipedia:',''),
            abstract_text.group(0).replace('\n', ' ')
            if (abstract_text := re.search(pattern=abstract_pattern,
                                           string=check_object(loop['revision']['text']['_VALUE']),
                                           flags=re.MULTILINE | re.DOTALL)
                ) is not None else None
        ))
    all_abstracts = all_abstracts_rdd.toDF(['title', 'abstract'])
    valid_abstracts = all_abstracts.dropna()
    return valid_abstracts


if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    # xml file that work good
    # link: https://dumps.wikimedia.org/enwiki/20211101/enwiki-20211101-pages-articles1.xml-p1p41242.bz2

    path_to_good_xml = "enwiki-20211101-pages-articles1.xml-p1p41242"

    # xml that throughs error
    # link: https://dumps.wikimedia.org/enwiki/20211101/enwiki-20211101-pages-articles10.xml-p4045403p5399366.bz2
    path_to_erroring_xml = "enwiki-20211101-pages-articles10.xml-p4045403p5399366"

    path_to_parse = path_to_erroring_xml

    # output folder
    parsed_abstracts_dir = 'parsed_wiki_abstract'

    if os.path.exists(path_to_parse):
            start_time_single = time.time()
            parsed_wikipedia_abstracts_0 = parse_wiki_articles_file(spark, path=path_to_parse)
            # res = parsed_wikipedia_abstracts_0.union(parsed_wikipedia_abstracts_1)
            print(f"parisng time: {time.time() - start_time_single}")
            parsed_wikipedia_abstracts_0.printSchema()

            parsed_wikipedia_abstracts_0.write.csv(path=parsed_abstracts_dir, sep='\t', mode='overwrite')

            print(f"document{path_to_parse} elapsed: {time.time() - start_time_single}")