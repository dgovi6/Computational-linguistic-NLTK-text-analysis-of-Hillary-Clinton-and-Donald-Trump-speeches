# -*- coding: utf-8 -*-

import sys
import codecs
import nltk
from nltk import bigrams, trigrams
import math


def tokenizza(frasi): #tokenizza le frasi prese in input
       tokens = []
       for frase in frasi:
              tok = nltk.word_tokenize(frase)
              tokens = tokens + tok
       return tokens #restituisce i tokens


def annotazioneLinguistica(tokens): #Part-Of-Speach tagger per i token presi in input
      tokensPOS = nltk.pos_tag(tokens)
      return tokensPOS #restituisce i tokens taggati


def distribuzioneFrequezaPOS(tokensPOS, x):
       onlyPOS = []
       listaPOS = tokensPOS
       for elem in listaPOS: #scorro la lista dei token taggati
              onlyPOS.append(elem[1]) #appendo alla lista vuota onlyPOS soltanto i tag degli elementi che scorro
       distrOnlyPOS = nltk.FreqDist(onlyPOS) #calcolo la distribuzione di frequenza dei tag
       listaFreqOnlyPOS = distrOnlyPOS.most_common(x) #seleziono gli x(numero richiesto di tag) tag più frequenti
       for item in listaFreqOnlyPOS: #scorro la lista degli x tag selezionati
              print item[0], "------ con frequenza: ", item[1] #stampo i tag ordinati per frequenza
       

def distribuzioneFrequenzaTOK(tokensPOS, x):
       noPoints = []
       listaPosTok = tokensPOS
       cond = [".", ",", ":"] #stabilisco una lista di tag come condizione
       for elem in listaPosTok: #scorro la lista dei token taggati
              if elem[1] not in cond: #se il tag del token in questione non appartiene alla lista
                     noPoints.append(elem[0]) #appendo il token (senza il tag) alla lista vuota noPoints
       distrNoPoint = nltk.FreqDist(noPoints) #calcolo la distribuzione di frequenza dei token aggiunti alla lista
       listaFreqNoPoint = distrNoPoint.most_common(x) #e ne selezione gli x più frequenti
       for item in listaFreqNoPoint:
              print item[0], "------ con frequenza: ", item[1] #stampo i token selezionati ordinati per frequenza (esclusa la punteggiatura)


def distribuzioneFrequenzaBigrammi(bigrammiPOS, x):
       selBig = []
       listaPosBig = bigrammiPOS
       cond = [".", ",", ":", "DT", "CC", "IN"] #stabilisco una lista di tag come condizione 
       for elem in listaPosBig: #scorro i bigrammi taggati
              if ( ( elem[0][1] not in cond ) and ( elem[1][1] not in cond ) ) : #se i tag dei due elementi formanti il bigramma non appartengono alla lista condizione
                     selBig.append(elem) #appendo il bigramma alla lista vuota selBig
       distrSelBig = nltk.FreqDist(selBig) #calcolo la istribuzione di frequenza dei bigrammi
       listaFreqSelBig = distrSelBig.most_common(x) #e ne seleziono gli x più frequenti
       for item in listaFreqSelBig:
              print "(", item[0][0][0], ", ", item[0][1][0], ")", "------ con frequenza: ", item[1] #stampo i bigrammi selezionati ordinati per frequenza restituendoli senza i relativi tag


def distribuzioneFrequenzaTrigrammi(trigrammiPOS, x):
       selTrig = []
       listaPosTrig = trigrammiPOS
       cond = [".", ",", ":", "DT", "CC", "IN"] #stabilisco una lista di tag come condizione
       for elem in listaPosTrig: #scorro i trigrammi taggati
              if ( (elem[0][1] not in cond) and (elem[1][1] not in cond) and (elem[2][1] not in cond) ) : #se i tag dei tre elementi formanti il trigramma non appartengono alla lista condizione
                     selTrig.append(elem) #appendo il trigramma alla lista vuota selTrig
       distrSelTrig = nltk.FreqDist(selTrig) #calcolo la distribuzione di frequenza dei trigrammi
       listaFreqSelTrig = distrSelTrig.most_common(x) #e ne seleziono gli x più frequenti
       for item in listaFreqSelTrig:
              print "(", item[0][0][0], ", ", item[0][1][0], ", ", item[0][2][0], ")", "------ con frequenza: ", item[1] #stampo i trigrammi selezionati ordinati per frequenza restituendoli senza i relativi tag


def bigrammiAggSosXCongiunta(tokens, bigrammiPOS, x, y):
       t = []
       z = []
       for big in set(bigrammiPOS): #scorro i singoli bigrammi
              frequenzaBigramma = bigrammiPOS.count(big) #calcolo la frequenza del bigramma in questione
              frequenzaA = tokens.count(big[0][0]) #calcolo la frequenza del primo elemento del bigramma
              frequenzaB = tokens.count(big[1][0]) #calcolo la frequenza del secondo elemento del bigramma
              probA= (frequenzaA*1.0) / (len(tokens)*1.0) #calcolo la probabilità del primo elemento del bigramma
              if (frequenzaA > x) and (frequenzaB > x): #controllo che la frequenza di ogni token preso in considerazione sia maggiore di x
                     probCondizionata=(frequenzaBigramma*1.0) / (frequenzaA*1.0) #dunque calcolo la probabilità condizionata del bigramma
                     probCongiunta = probA*1.0 * probCondizionata*1.0 #e calcolo la probabilità congiunta del bigramma
              bigProb = big, probCongiunta #vincolo bigramma e relativa probabilità congiunta inserendoli in una tupla
              t.append(bigProb) #appendo la tupla alla lista vuota t
       def getKey(item):
              return item[1]
       t2 = sorted(t, key = getKey, reverse = True) #ordino le tuple secondo la probabilità congiunta
       cond1 = ["JJ", "JJR", "JJS"] #stabilisco una lista di tag come condizione per il primo elemento del bigramma
       cond2 = ["NN", "NNS", "NNP", "NNPS"] #stabilisco una lista di tag come condizione per il secondo elemento del bigramma
       for w in t2: #scorro la lista delle tuple ordinate
              if (w[0][0][1] in cond1) and (w[0][1][1] in cond2) :
                     z.append(w) #se viene soddisfatta la condizione (ovvero bigrammi composti da agg + sos) appendo l'elemento in questione alla lista vuota z 
       for i, q in enumerate(z): #scorro la lista z controllando il numero di iterazioni
              if i < y: #controllo che il numero di iterazioni rimanga sotto il numero y
                     print "(", q[0][0][0], ", ", q[0][1][0], ")", "------ con probabilità congiunta: ", q[1] #stampa gli y bigrammi ordinati per probabilità congiunta, senza i tag assegnati agli elementi


def bigrammiAggSosXCondizionata(tokens, bigrammiPOS, x, y):
       t = []
       z = []
       for big in set(bigrammiPOS): #scorro i singoli bigrammi
              frequenzaBigramma = bigrammiPOS.count(big) #calcolo la frequenza del bigramma in questione
              frequenzaA = tokens.count(big[0][0]) #calcolo la frequenza del primo elemento del bigramma
              frequenzaB = tokens.count(big[1][0]) #calcolo la frequenza del secondo elemento del bigramma
              if (frequenzaA > x) and (frequenzaB > x): #controllo che la frequenza di ogni token preso in considerazione sia maggiore di x
                     probCondizionata = (frequenzaBigramma*1.0) / (frequenzaA*1.0) #dunque calcolo la probabilità condizionata del bigramma
              bigProb = big, probCondizionata #vincolo bigramma e relativa probabilità congiunta inserendoli in una tupla
              t.append(bigProb) #appendo la tupla alla lista vuota t
       def getKey(item):
              return item[1]
       t2 = sorted(t, key = getKey, reverse = True) #ordino le tuple secondo la probabilità condizionata
       cond1 = ["JJ", "JJR", "JJS"] #stabilisco una lista di tag come condizione per il primo elemento del bigramma
       cond2 = ["NN", "NNS", "NNP", "NNPS"] #stabilisco una lista di tag come condizione per il secondo elemento del bigramma
       for w in t2: #scorro la lista delle tuple ordinate
              if (w[0][0][1] in cond1) and (w[0][1][1] in cond2) :
                     z.append(w) #se viene soddisfatta la condizione (ovvero bigrammi composti da agg + sos) appendo l'elemento in questione alla lista vuota z
       for i, q in enumerate(z): #scorro la lista z controllando il numero di iterazioni
              if i < y: #controllo che il numero di iterazioni rimanga sotto il numero y
                     print "(", q[0][0][0], ", ", q[0][1][0], ")", "------ con probabilità condizionata: ", q[1] #stampa gli y bigrammi ordinati per probabilità congiunta, senza i tag assegnati agli elementi


def bigrammiAggSosXLMI(tokens, bigrammiPOS, x, y):
       t = []
       z = []
       for big in set(bigrammiPOS): #scorro i singoli bigrammi
              frequenzaBigramma = bigrammiPOS.count(big) #calcolo la frequenza del bigramma in questione
              frequenzaA = tokens.count(big[0][0]) #calcolo la frequenza del primo elemento del bigramma
              frequenzaB = tokens.count(big[1][0]) #calcolo la frequenza del secondo elemento del bigramma
              probBigramma = (frequenzaBigramma*1.0) / (len(tokens)*1.0) #calcolo la probabilità del bigramma
              probA = (frequenzaA*1.0) / (len(tokens)*1.0) #calcolo la probabilità del primo elemento del bigramma
              probB = (frequenzaB*1.0) / (len(tokens)*1.0) #calcolo la probabilità del secondo elemento del bigramma
              if (frequenzaA > x) and (frequenzaB > x): #controllo che la frequenza di ogni token preso in considerazione sia maggiore di x
                     LMI = frequenzaBigramma * math.log( (probBigramma*1.0) / (probA*1.0 * probB*1.0) ) #dunque calcolo la Local Mutual Information del bigramma    
              bigLMI = big, LMI #vincolo bigramma e relativa LMI inserendoli in una tupla
              t.append(bigLMI) #appendo la tupla alla lista vuota t
       def getKey(item):
              return item[1]
       t2 = sorted(t, key=getKey, reverse = True) #ordino le tuple secondo la LMI
       cond1 = ["JJ", "JJR", "JJS"] #stabilisco una lista di tag come condizione per il primo elemento del bigramma
       cond2 = ["NN", "NNS", "NNP", "NNPS"] #stabilisco una lista di tag come condizione per il secondo elemento del bigramma
       for w in t2: #scorro la lista delle tuple ordinate
              if (w[0][0][1] in cond1) and (w[0][1][1] in cond2) :
                     z.append(w) #se viene soddisfatta la condizione (ovvero bigrammi composti da agg + sos) appendo l'elemento in questione alla lista vuota z
       for i, q in enumerate(z): #scorro la lista z controllando il numero di iterazioni
              if i < y: #controllo che il numero di iterazioni rimanga sotto il numero y
                     print "(", q[0][0][0], ", ", q[0][1][0], ")", "------ con LMI: ", q[1] #stampa gli y bigrammi ordinati per LMI, senza i tag assegnati agli elementi


def probFraseMarkov0(frasi, tokens):
       probabilitaFraseMax = 0.0 
       distribuzioneFrequenzaTok = nltk.FreqDist(tokens) #calcolo la distribuzione di frequenza dei token
       for frase in frasi: #scorro le frasi
              probabilitaFrase = 1.0 
              tokensFrase = nltk.word_tokenize(frase) #tokenizzo la frase in questione
              contatore = 0 #imposto un contatore a 0
              if len(tokensFrase) < 10: #controllo che la frase in questione sia lunga almeno 10 token 
                     continue #altrimenti torno all'inizio del ciclo
              for tok in tokensFrase: #scorro i token della frase
                     if tokens.count(tok) > 2: #controllo che ogni token abbia frequenza di almeno 2
                            contatore = contatore + 1 #incremento il contatore
              if not (contatore == len(tokensFrase)): #se una volta scorsi tutti i token della frase il contatore non è uguale alla lunghezza della frase
                     continue #torno all'inizio del ciclo
              for elem in tokensFrase: #una volta controllata la validità della frase secondo le condizioni stabilite, scorro di nuovo i token della frase
                     probabilitaTok=distribuzioneFrequenzaTok[elem]*1.0 / len(tokens)*1.0 #calcolo la probabilità del token
                     probabilitaFrase=probabilitaFrase*1.0*probabilitaTok*1.0 #calcolo la porbabilità della frase con modello di Markov ordine 0
                     if probabilitaFrase>probabilitaFraseMax: #se la probabilità della frase in questione è maggiore dell'attuale porbabilità massima, la sostituisco alla probabilità massima
                            probabilitaFraseMax=probabilitaFrase
                            fraseMax=frase 
       print fraseMax, "------ con probabilità: ", probabilitaFraseMax #stampo la frase con probabilità massima e la relativa probabilità

       
def probFraseMarkov1(frasi, tokens, bigrammi):
       probabilitaFraseMax = 0.0
       distribuzioneFrequenzaTok = nltk.FreqDist(tokens) #calcoolo la distribuzione di frequenza dei token
       distribuzioneFrequenzaBig = nltk.FreqDist(bigrammi) #calcolo la distribuzione di frequenza dei bigrammi
       for frase in frasi: #scorro le frasi
              tokensFrase = nltk.word_tokenize(frase) #tokenizzo la frase in questione 
              contatore = 0 #imposto un contatore a 0
              if len(tokensFrase) < 10:  #controllo che la frase in questione sia lunga almeno 10 token
                     continue #altrimenti torno all'inizio del ciclo
              for tok in tokensFrase: #scorro i token della frase
                     if tokens.count(tok) > 2: #controllo che ogni token abbia frequenza di almeno 2
                            contatore = contatore + 1 #incremento il contatore
              if not (contatore == len(tokensFrase)): #se una volta scorsi tutti i token della frase il contatore non è uguale alla lunghezza della frase
                     continue #torno all'inizio del ciclo
              bigrammiFrase = list(bigrams(tokensFrase)) #creo i bigrammi per la frase in questione
              probabilitaFrase = (distribuzioneFrequenzaTok[bigrammiFrase[0][0]]*1.0) / (len(tokens)*1.0) #assegno come probabilità di partenza la probabilità del primo elemento del token della frase
              for big in bigrammiFrase: #scorro i bigrammi della frase
                     frequenzaBigramma = distribuzioneFrequenzaBig[big]*1.0 #calcolo la frequenza del bigramma
                     frequenzaA = (distribuzioneFrequenzaTok[big[0]]*1.0) #calcolo la frequenza del primo elemento del bigramma
                     probCondizionataBig = (frequenzaBigramma*1.0) / (frequenzaA*1.0) #calcolo la probabilità condizionata del bigramma
                     probabilitaFrase = probabilitaFrase*1.0 * probCondizionataBig*1.0 #calcolo la probabilità della frase con modello di Markov di ordine 1
                     if probabilitaFrase > probabilitaFraseMax: #se la probabilità della frase in questione è maggiore dell'attuale porbabilità massima, la sostituisco alla probabilità massima
                            probabilitaFraseMax = probabilitaFrase
                            fraseMax = frase
       print fraseMax, "------ con probabilità: ", probabilitaFraseMax #stampo la frase con probabilità massima e la relativa probabilità


def NEt (tokensPOS):
       analisi = nltk.ne_chunk(tokensPOS) #creo l'albero
       NElist = [] #creo una lista vuota da popolare con coppie valore, entità 
       for nodo in analisi: #scorro l'albero
              NE = ' '
              if hasattr(nodo, 'label'): #se è un nodo terminale
                     if nodo.label() in ["PERSON", "GPE", "ORGANIZATION"]: #e se corrisponde a un'entità nominata
                            for partNE in nodo.leaves(): #scorro ongi foglia e creo la NE completa
                                   NE = NE + ' ' + partNE[0]
                            NElist.append([NE,nodo.label()]) #inserisco la NE nella lista accompagnata dalla sua Name Entity
       return NElist #restituisco la lista di NE


def NEspec (listaNE, NE, n): #estraggo solo una specifica NE 
       lista = [] 
       for i in listaNE: #scorro la lista di NE
              if i[1] == NE: #se l'entità è del tipo specificato la appendo alla lista vuota lista
                     lista.append(i[0])
       distr = nltk.FreqDist(lista) #calcolo la distribuzione di frequenza sulla lista
       listaOrdinata = distr.most_common(20) #seleziono i 20 elementi più frequenti
       for i in listaOrdinata:
              print NE.encode("utf-8"),":", i[0], "------ con frequenza:", i[1]


def main(file1, file2):
       fileInput1 = codecs.open(file1, "r", "utf-8")
       fileInput2 = codecs.open(file2, "r", "utf-8")
       raw1 = fileInput1.read()
       raw2 = fileInput2.read()
       sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
       frasi1 = sent_tokenizer.tokenize(raw1)
       frasi2 = sent_tokenizer.tokenize(raw2)
       tokens1 = tokenizza(frasi1)
       tokens2 = tokenizza(frasi2)
       tokensPOS1 = annotazioneLinguistica(tokens1) #token taggati per il file1
       tokensPOS2 = annotazioneLinguistica(tokens2) #token taggati per il file2
       bigrammi1 = list(bigrams(tokens1)) #lista dei bigrammi per il file1
       bigrammi2 = list(bigrams(tokens2)) #lista dei bigrammi per il file2
       bigrammiPOS1 = list(bigrams(annotazioneLinguistica(tokens1))) #lista dei bigrammi taggati per il file1
       bigrammiPOS2 = list(bigrams(annotazioneLinguistica(tokens2))) #lista dei bigrammi taggati per il file2
       trigrammiPOS1 = list(trigrams(annotazioneLinguistica(tokens1))) #lista dei trigrammi taggati per il file1
       trigrammiPOS2 = list(trigrams(annotazioneLinguistica(tokens2))) #lista dei trigrammi taggati per il file2

       print "Le 10 PoS più frequenti per il file: ", file1 #da qui in poi richiamo tutto le funzioni di cui sopra e genero l'output
       print
       distribuzioneFrequezaPOS(tokensPOS1, 10)
       print "------------------------------------------------------------------------------------"
       print
       print "Le 10 PoS più frequenti per il file: ", file2
       print
       distribuzioneFrequezaPOS(tokensPOS2, 10)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "I 20 token più frequenti escludendo la punteggiatura per il file: ", file1
       print
       distribuzioneFrequenzaTOK(tokensPOS1, 20)
       print "------------------------------------------------------------------------------------"
       print
       print "I 20 token più frequenti escludendo la punteggiatura per il file: ", file2
       print
       distribuzioneFrequenzaTOK(tokensPOS2, 20)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "I 20 bigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni per il file: ", file1
       print
       distribuzioneFrequenzaBigrammi(bigrammiPOS1, 20)
       print "------------------------------------------------------------------------------------"
       print 
       print "I 20 bigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni per il file: ", file2
       print 
       distribuzioneFrequenzaBigrammi(bigrammiPOS2, 20)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "I 20 trigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni per il file: ", file1
       print
       distribuzioneFrequenzaTrigrammi(trigrammiPOS1, 20)
       print "------------------------------------------------------------------------------------"
       print
       print "I 20 trigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni per il file: ", file2
       print
       distribuzioneFrequenzaTrigrammi(trigrammiPOS2, 20)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "I 20 bigrammi composti da Aggettivo e Sostantivo (dove ogni token deve avere una frequenza maggiore di 2), con probabilità congiunta massima per il file: ", file1
       print
       bigrammiAggSosXCongiunta(tokens1, bigrammiPOS1, 2, 20)
       print "------------------------------------------------------------------------------------"
       print
       print "I 20 bigrammi composti da Aggettivo e Sostantivo (dove ogni token deve avere una frequenza maggiore di 2), con probabilità congiunta massima per il file: ", file2
       print
       bigrammiAggSosXCongiunta(tokens2, bigrammiPOS2, 2, 20)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "I 20 bigrammi composti da Aggettivo e Sostantivo (dove ogni token deve avere una frequenza maggiore di 2), con probabilità condizionata massima per il file: ", file1
       print
       bigrammiAggSosXCondizionata(tokens1, bigrammiPOS1, 2, 20)
       print "------------------------------------------------------------------------------------"
       print
       print "I 20 bigrammi composti da Aggettivo e Sostantivo (dove ogni token deve avere una frequenza maggiore di 2), con probabilità condizionata massima per il file: ", file2       
       print
       bigrammiAggSosXCondizionata(tokens2, bigrammiPOS2, 2, 20)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "I 20 bigrammi composti da Aggettivo e Sostantivo (dove ogni token deve avere una frequenza maggiore di 2), con forza associativa (in termini di Local Mutual Information) massima per il file : ", file1
       print
       bigrammiAggSosXLMI(tokens1, bigrammiPOS1, 2, 20)
       print "------------------------------------------------------------------------------------"
       print
       print "I 20 bigrammi composti da Aggettivo e Sostantivo (dove ogni token deve avere una frequenza maggiore di 2), con forza associativa (in termini di Local Mutual Information) massima per il file : ", file2
       print
       bigrammiAggSosXLMI(tokens2, bigrammiPOS2, 2, 20)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "Frase con probabilità maggiore, calcolata con modello di Markov di ordine 0, con lunghezza maggiore di 10 tokens e con ogni token con frequenza maggiore di 2 per il file: ", file1
       print
       probFraseMarkov0(frasi1, tokens1)
       print "-----------------------------------------------------------------------------------"
       print
       print "Frase con probabilità maggiore, calcolata con modello di Markov di ordine 0, con lunghezza maggiore di 10 tokens e con ogni token con frequenza maggiore di 2 per il file: ", file2
       print
       probFraseMarkov0(frasi2, tokens2)
       print
       print "///////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "Frase con probabilità maggiore, calcolata con modello di Markov di ordine 1, con lunghezza maggiore di 10 tokens e con ogni token con frequenza maggiore di 2 per il file: ", file1
       print
       probFraseMarkov1(frasi1, tokens1, bigrammi1)
       print "-----------------------------------------------------------------------------------"
       print
       print "Frase con probabilità maggiore, calcolata con modello di Markov di ordine 1, con lunghezza maggiore di 10 tokens e con ogni token con frequenza maggiore di 2 per il file: ", file2
       print 
       probFraseMarkov1(frasi2, tokens2, bigrammi2)
       print
       print "///////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "Estraggo le Entità Nominate e ed estraggo i 20 nomi di persona più frequenti ordinati per frequenza per il file: ", file1
       print
       NEspec(NEt(tokensPOS1), "PERSON", file1)
       print "-----------------------------------------------------------------------------------"
       print 
       print "Estraggo le Entità Nominate e ed estraggo i 20 nomi di persona più frequenti ordinati per frequenza per il file: ", file2
       print
       NEspec(NEt(tokensPOS2), "PERSON", file2)
       print
       print "///////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "Estraggo le Entità Nominate e ed estraggo i 20 nomi di luogo più frequenti ordinati per frequenza per il file: ", file1
       print
       NEspec(NEt(tokensPOS1), "GPE", file1)
       print "-----------------------------------------------------------------------------------"
       print
       print "Estraggo le Entità Nominate e ed estraggo i 20 nomi di luogo più frequenti ordinati per frequenza per il file: ", file2
       print
       NEspec(NEt(tokensPOS2), "GPE", file2)


       
main(sys.argv[1], sys.argv[2])
