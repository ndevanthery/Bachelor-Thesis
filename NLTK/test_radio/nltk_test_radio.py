from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from nltk.wsd import lesk

import nltk

nltk.download('wordnet')
nltk.download('omw')
#Tokenizer
nltk.download('punkt')

#test text
US_ABDO_COMPLET = '''Foie   :  taille et structure normales. 
                            Nodule hyperéchogène de 16 mm dans le segment IV évoquant un petit hémangiome.
                            Les veines sus-hépatiques et la veine porte sont de calibre normal avec un flux hépatopète au niveau portal.
                Voies biliaires   :   de calibre normal, le cholédoque mesure 4 mm au niveau du hile hépatique. 
                Status post-cholécystectomie.
                Pancréas   :   sans anomalie.
                Rate   :   de taille normale, homogène.
                Reins   :   de morphologie normale, sans dilatation des cavités.
                Rétropéritoine   :   pas d’adénopathies ni de masse. 
                Aorte de calibre normal.
                Tube digestif   :   sans anomalie grossière. 
                Absence d'épaississement des parois intestinaux en fosse iliaque droite. 
                Absence de liquide libre. 
                L'appendice n'est pas identifié. 
                Le passage de la sonde échographique en fosse iliaque droite est indolore ce jour.
                Péritoine   :   pas de liquide libre.
                Vessie   :   parois régulières et non épaissies.
                Organes génitaux   :   d'aspect normal.
                Autres constatations   :   aucune. 
                '''

US_ABDO_INF = '''  
    Reins   :   de taille et de morphologie normales, sans dilatation des cavités.
    Rétropéritoine   :   pas d’adénopathies ni de masse. 
    Aorte de calibre normal.
    Tube digestif   :   sans anomalie grossière (examen non dédié).
    Péritoine   :   pas de liquide libre.
    Vessie   :   en réplétion modérée, à parois régulières et non épaissies.
    Organes génitaux   :   d'aspect normal. 
    Ovaires bien visibles sans anomalie.
    Autres constatations   :    un contrôle de l’abdomen supérieur ne montre pas d’anomalie.
'''

US_ABDO_SUP = '''
                Foie   :   taille normale (14 cm craniocaudal au lobe droit). 
                            Minime hétérogénéité diffuse du parenchyme hépatique pouvant être en rapport avec une discrète stéatose irrégulière. 
                            Lésion échogène au segment IV a (ou coalescence de deux lésions échogènes avec un centre hypoéchogène) mesurant 40 x 30 mm posant un diagnostic différentiel d'hémangiome versus adénome. 
                            Lésion échogène de 2 cm en avant de la bifurcation de la veine porte évoquant un hémangiome. 
                            Flux porte physiologique au doppler.
                Voies biliaires   :   de calibre normal. Vésicule de parois fines sans calcul décelable.
                Pancréas   :   sans anomalie.
                Rate   :   de taille normale, homogène.
                Reins   :   de morphologie normale, sans dilatation des cavités.
                Rétropéritoine   :   pas d’adénopathies ni de masse. 
                Aorte de calibre normal.
                Tube digestif   :   sans anomalie grossière (examen non dédié).
                Péritoine   :   pas de liquide libre.
                Autres constatations   :   un contrôle de l’abdomen inférieur ne montre pas d’anomalie. Vessie vide.      
                '''
ps = PorterStemmer()


report = US_ABDO_INF
#tokenize sentences and words.
tokened_sent = sent_tokenize(report)
tokened_word = word_tokenize(report)



#print(tokened_sent)
stop_words = set(stopwords.words('french'))

lang = 'fra'


#syn1 = wn.synsets('Foie' ,lang=lang)[0]
"""
organ = wn.synsets('Organ')[0]

 
print(syn1.name())
print(syn2.name())
print(syn1.wup_similarity(syn2)) """




### Test the meaning closeness of words to find the organs, or something else.
""" for sen in tokened_sent:

    tokened_word = word_tokenize(sen)
    filtered_sentence = [w for w in tokened_word if w not in stop_words]
    for w in filtered_sentence:
        try : 
            word_synset = wn.synsets(w , lang='fra')[0]
            similarity = word_synset.wup_similarity(organ)
            
            if(similarity > 0.5):
                print("{:10}: {:.3f} probability to be an organ".format(w, similarity))
            

           
        except:
            pass
    

 """
infos = []
organes =[]
for sen in tokened_sent:
    splittedSen = sen.split(':')
    if(len(splittedSen) >1):
        organes.append(splittedSen[0])
        infos.append(splittedSen[1])
    else:
    
        infos[len(infos)-1] += sen



    
for i in range(0,len(infos)):
    print("{:10} : {}".format(organes[i] , infos[i]))
    print('\n')
    
    

print(len(infos))