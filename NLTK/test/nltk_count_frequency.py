import nltk
EXAMPLE_TEXT = "An an valley indeed so no wonder future nature vanity. Debating all she mistaken indulged believed provided declared. He many kept on draw lain song as same. Whether at dearest certain spirits is entered in to. Rich fine bred real use too many good. She compliment unaffected expression favourable any. Unknown chiefly showing to conduct no."
frequency = nltk.FreqDist(EXAMPLE_TEXT) 
for key,val in frequency.items(): 
    print (str(key) + ':' + str(val))