from nltk.stem import PorterStemmer


#Stemming

ps = PorterStemmer()
example_words = ["python","pythoner","pythoning","pythoned","pythonly"]
for w in example_words:
 print(ps.stem(w))
'''
THERE ARE A LOT MANY STEMMERS AVAILABLE IN IN THE NLTK LIBRARY:
1)PorterStemmer
2)SnowballStemmer
3)LancasterStemmer
4)RegexpStemmer
5)RSLPStemmer
'''