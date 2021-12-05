# Vyhladavanie Informacie
## Wikipedia Abstract Search System
## Oleksandr Lytvyn


to launch the app, you will need to have docker installed.
1. Pull the docker image from docker hub: docker pull letv3/pylucene_w_sklearn
2. Set this images as remote execution environment for the project: https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker
3. Download next archives and extract files to the **/data** folder:
   1. https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
   2. https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
   3. https://databus.dbpedia.org/dbpedia/text/long-abstracts/2021.08.01/long-abstracts_lang=en.ttl.bz2
4. Run main.py. It will:
   2. Create index
   3. Prompts for the phrase to search
   4. Retrieves most suitable documents
   5. Shows _Cosine Similarity_ of the first abstract to the abstracts from mediawiki and dbpedia
