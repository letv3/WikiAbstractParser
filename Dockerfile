FROM python:3.9

RUN apt-get update \
    && apt-get install -y default-jdk ant

RUN apt-get install -y python3.9 python3-dev gcc gfortran musl-dev libopenblas-dev liblapack-dev
ADD repositories.txt /etc/apk/repositories

WORKDIR /usr/lib/jvm/default-java/jre/lib
RUN ln -s ../../lib amd64

WORKDIR /usr/src/pylucene
RUN curl https://downloads.apache.org/lucene/pylucene/pylucene-8.9.0-src.tar.gz \
    | tar -xz --strip-components=1
RUN cd jcc \
    && NO_SHARED=1 JCC_JDK=/usr/lib/jvm/default-java python setup.py install
RUN make all install JCC='python -m jcc' ANT=ant PYTHON=python NUM_FILES=8

WORKDIR /usr/src
RUN rm -rf pylucene


WORKDIR /usr/WikiAbstractParser

COPY requirements.txt  requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip setuptools  && \
    pip3 install --no-cache-dir -r requirements.txt


#FROM coady/pylucene
#
#ADD repositories.txt /etc/apk/repositories
#
#RUN apt-get install -y python3.9 python3-dev gcc gfortran musl-dev libopenblas-dev liblapack-dev
#
#WORKDIR /usr/WikiAbstractParser
#
#COPY requirements.txt  requirements.txt
#
#RUN pip3 install --no-cache-dir --upgrade pip setuptools  && \
#    pip3 install --no-cache-dir -r requirements.txt
