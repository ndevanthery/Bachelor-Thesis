from nltk.corpus import wordnet
synonyms = []
for syns in wordnet.synsets('Foie'):
 synonyms.append(syns.name())
print ("synonyms", synonyms)
#FINDING ANTONYMS FROM WORDNETS
from nltk.corpus import wordnet
antonyms = []
for syn in wordnet.synsets("MRI"):
 for l in syn.lemmas():
  if l.antonyms():
   antonyms.append(l.antonyms()[0].name())
print(antonyms)