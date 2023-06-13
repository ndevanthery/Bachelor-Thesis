from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
nltk.download('stopwords')

example_sent = "This is a sample sentence, showing off the stop words filtration. Here you can write whatever you want to. You can also add a very big text file and see how this technique works"
#STOP WORDS ARE PARTICULAR TO RESPECTIVE LANGUAGES(english, spanish, french Et cetera)
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(example_sent)
filtered_sentence = [w for w in word_tokens if w not in stop_words]
print(filtered_sentence)