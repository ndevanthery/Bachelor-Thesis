from nltk.tokenize import TreebankWordTokenizer
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import nltk
nltk.download('omw')

lang='fra'

sent = TreebankWordTokenizer().tokenize("Je voudrai essayer avec cette phrase")
synsets = [lesk(sent, w, 'n') for w in sent]
print(synsets)

for ws in sent:
    for ss in [n for synset in wn.synsets(ws, lang=lang) for n in synset.lemma_names(lang)]:
        print((ws, ss), '\n')