from nltk.tokenize import sent_tokenize, word_tokenize

import nltk

#Tokenizer
nltk.download('punkt')

#test text
EXAMPLE_TEXT = "An an valley indeed so no wonder future nature vanity. Debating all she mistaken indulged believed provided declared. He many kept on draw lain song as same. Whether at dearest certain spirits is entered in to. Rich fine bred real use too many good. She compliment unaffected expression favorable any. Unknown chiefly showing to conduct no."

#tokenize sentences and words.
tokened_sent = sent_tokenize(EXAMPLE_TEXT)
tokened_word = word_tokenize(EXAMPLE_TEXT)




print(tokened_sent)
print(tokened_word)
