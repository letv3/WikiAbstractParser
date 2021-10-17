import string
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher

from collections import Counter
from math import sqrt

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


class TextSimilarityComparator:
    """Class to compare similarity of 2 different(Wiki abstracts in our case)"""

    def __init__(self):
        self.stopwords = stopwords.words('english')

    def clean_string(self, text):
        text = ''.join([word for word in text if word not in string.punctuation])
        text = text.lower()
        text = ' '.join([word for word in text.split() if word not in self.stopwords])
        return text

    def compare_texts(self, first_text, second_text ) -> float:
        """function to compare similarity of two texts"""
        """:return Float value from 0 to 1 which represent similarity of two strs"""
        first_text = first_text.reshape(1, -1)
        second_text = second_text.reshape(1, -1)
        return cosine_similarity(first_text, second_text)


if __name__ == '__main__':
    comparator = TextSimilarityComparator()

    va = 'animation method which image figures manipulated appear motion picture moving images traditional animation images drawn painted hand transparent ' \
         'cel celluloid sheets photographed exhibited film today most animations made computer generated imagery cgi computer animation can very detailed ' \
         'computer animation animation methods 3d animation while traditional animation computers traditional animation 2d computer animation which may have ' \
         'look traditional animation can used stylistic reasons low bandwidth faster real time rendering s other common animation methods apply stop motion ' \
         'technique two three dimensional objects like cutout animation paper cutouts puppet s clay animation clay figures commonly effect animation achieved ' \
         'rapid succession sequential images minimally differ from each other illusion motion pictures general thought rely phi phenomenon beta movement exact ' \
         'causes still uncertain analog device analog mechanical animation media rely rapid display sequential images include phenakistiscope ph\xc3\xa9nakisticope' \
         ' zoetrope flip book praxinoscope film television video popular electronic animation media originally were analog now operate digital media digitally' \
         ' display computer techniques like animated gif flash animation were developed animation more pervasive than many people know apart from short films ' \
         'feature films television show television series animated gifs other media dedicated display moving images animation also prevalent video game s motion ' \
         'graphics user interface s visual effects sfn buchan 2013 physical movement image parts through simple mechanics instance moving images magic lantern ' \
         'shows can also considered animation mechanical manipulation three dimensional puppets objects emulate living beings has very long history automaton ' \
         'automata electronic automata were popularized disney animatronics animator s artists who specialize creating animation toc limit 3'

    vb = "stop motion animation used describe animation created physically manipulating real world objects photographing them one frame film time create illusion " \
         "movement sfn solomon 1989 p 299 many different types stop motion animation usually named after medium used create animation sfn laybourne 1998 p 159 " \
         "computer software widely available create type animation traditional stop motion animation usually less expensive more time consuming produce than " \
         "current computer animation sfn laybourne 1998 p 159 puppet animation typically involves stop motion puppet figures interacting constructed environment" \
         " contrast real world interaction model animation sfn solomon 1989 p 171 puppets generally have armature sculpture armature inside them keep them still " \
         "steady constrain motion particular joints sfn laybourne 1998 pp 155 56 examples include tale fox france 1937 nightmare before christmas us 1993 corpse" \
         " bride us 2005 coraline film coraline us 2009 films ji\xc5\x99\xc3\xad trnka adult animated sketch comedy television series robot chicken us 2005 " \
         "present puppetoon created using techniques developed george pal sfn beck 2004 p 70 puppet animated films typically use different version puppet " \
         "different frames rather than simply manipulating one existing puppet sfn beck 2004 pp 92 93 file:claychick.jpg thumb clay animation scene from " \
         "finland finnish television commercial clay animation plasticine animation often called claymation which however laika company trademarked name " \
         "uses figures made clay similar malleable material create stop motion animation sfn solomon 1989 p 299 sfn laybourne 1998 pp 150 151 figures may have" \
         " armature sculpture armature wire frame inside similar related puppet animation below can manipulated pose figures sfn laybourne 1998 pp 151 54 " \
         "alternatively figures may made entirely clay films bruce bickford animator bruce bickford where clay creatures morph variety different shapes examples" \
         " clay animated works include gumby show us 1957 1967 mio mao italy 1974 2005 morph animation morph shorts uk 1977 2000 wallace gromit shorts uk 1989 " \
         "jan \xc5\xa1vankmajer s dimensions dialogue czechoslovakia 1982 trap door uk 1984 films include wallace amp gromit curse were rabbit chicken run " \
         "adventures mark twain 1985 film adventures mark twain sfn beck 2004 p 250 strata cut animation strata cut animation most commonly form clay animation " \
         "which long bread like quot loaf quot clay internally packed tight loaded varying imagery sliced thin sheets animation camera taking frame end loaf each" \
         " cut eventually revealing movement internal images within sfn furniss 1998 pp 52 54 cutout animation type stop motion animation produced moving two" \
         " dimensional pieces material paper cloth sfn laybourne 1998 pp 59 60 examples include terry gilliam s animated sequences from monty python's flying " \
         "circus uk 1969 1974 fantastic planet france czechoslovakia 1973 tale tales 1979 film tale tales russia 1979 pilot episode adult television sitcom series" \
         " sometimes episodes south park us 1997 music video live moment from verona riots band produced alberto serrano n\xc3\xadvola uy\xc3\xa1 spain 2014 " \
         "silhouette animation variant cutout animation which characters backlit only visible silhouettes sfn culhane 1990 pp 170 171 examples include adventures " \
         "prince achmed weimar republic 1926 princes et princesses france 2000 model animation refers stop motion animation created interact exist part live " \
         "action world sfn harryhausen dalton 2008 pages 9 11 intercutting matte filmmaking matte effects split screens often employed blend stop motion " \
         "characters objects live actors settings lt ref name quot harryhausen_dalton222 226 quot gt examples include work ray harryhausen seen films jason " \
         "argonauts 1963 film jason argonauts 1963 lt ref name quot harryhausen_dalton18 quot gt work willis h o'brien films king kong 1933 film king kong 1933 " \
         "go motion variant model animation uses various techniques create motion blur between frames film which present traditional stop motion sfn smith 1986 p" \
         " 90 technique invented industrial light amp magic phil tippett create special effect scenes film empire strikes back 1980 sfn watercutter 2012 anothe" \
         "r example dragon named quot vermithrax quot from 1981 film dragonslayer 1981 film dragonslayer sfn smith 1986 pages 91 95 object animation refers use " \
         "regular inanimate objects stop motion animation opposed specially created items sfn laybourne 1998 pp 51 57 graphic animation uses non drawn flat " \
         "visual graphic material photographs newspaper clippings magazines etc which sometimes manipulated frame frame create movement sfn laybourne 1998 p " \
         "128 other times graphics remain stationary while stop motion camera moved create screen action brickfilm subgenre object animation involving using " \
         "lego other similar brick toys make animation sfn paul 2005 pages 357 63 sfn herman 2014 have had recent boost popularity advent video sharing sites " \
         "youtube availability cheap cameras animation software sfn haglund 2014 pixilation involves use live humans stop motion characters sfn laybourne 1998"
    sentences = [va, vb]
    cleaned = list(map(comparator.clean_string, sentences))
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()
    csim = comparator.compare_texts(vectors[0], vectors[1])
    print(csim)
