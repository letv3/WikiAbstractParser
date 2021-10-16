import lucene
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.analysis import StopFilter
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
test = """"Anarchism''' is a [[political philosophy]] and [[Political movement|movement]] that is sceptical of [[authority]] and rejects all involuntary, coercive forms of [[hierarchy]]. Anarchism calls for the abolition of the [[State (polity)|state]], which it holds to be undesirable, unnecessary, and harmful. As a historically [[left-wing]] movement, placed on the farthest left of the [[political spectrum]], it is usually described alongside [[libertarian Marxism]] as the [[libertarian]] wing ([[libertarian socialism]]) of the [[socialist movement]], and has a strong historical association with [[anti-capitalism]] and [[socialism]].The [[history of anarchism]] goes back to [[prehistory]], when humans lived in anarchic societies long before the establishment of formal states, [[realm]]s, or [[empire]]s. With the rise of organised hierarchical bodies, [[scepticism]] toward authority also rose, but it was not until the 19th century that a self-conscious political movement emerged. During the latter half of the 19th and the first decades of the 20th century, the anarchist movement flourished in most parts of the world and had a significant role in workers' struggles for [[emancipation]]. Various [[anarchist schools of thought]] formed during this period. Anarchists have taken part in several revolutions, most notably in the [[Spanish Civil War]], whose end marked the end of the [[classical era of anarchism]]. In the last decades of the 20th and into the 21st century, the anarchist movement has been resurgent once more.
Anarchism employs a [[diversity of tactics]] in order to meet its ideal ends which can be broadly separated into revolutionary and evolutionary tactics; there is significant overlap between the two, which are merely descriptive. Revolutionary tactics aim to bring down authority and state, having taken a violent turn in the past, while evolutionary tactics aim to prefigure what an anarchist society would be like. Anarchist thought, criticism, and [[Praxis (process)|praxis]] have played a part in diverse areas of human society. Anarchism has been both defended and criticised; criticism of anarchism include claims that it is internally inconsistent, violent, or utopian.
{{toc limit|3}}
"""
# StandardAnalyzer example.
analyzer = StandardAnalyzer()
stop_words = EnglishAnalyzer.getDefaultStopSet()
engilish_analyzer = EnglishAnalyzer()
stream = analyzer.tokenStream("", StringReader(test))
stream = StopFilter(stream, stop_words)
stream.reset()

tokens = []
while stream.incrementToken():
    tokens.append(stream.getAttribute(CharTermAttribute.class_).toString())
print(tokens)




