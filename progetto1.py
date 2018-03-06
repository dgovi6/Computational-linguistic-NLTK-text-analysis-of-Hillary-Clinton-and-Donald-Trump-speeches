# -*- coding: utf-8 -*-

import sys
import codecs
import nltk


def tokenizza(frasi): #tokenizza le frasi prese in input
       tokens = []
       for frase in frasi:
              tok = nltk.word_tokenize(frase)
              tokens = tokens + tok
       return tokens #restituisce i tokens


def calcoloNTokens(file, tokens): #prende in input il file e i suoi token
       print "Il file", file, "è lungo", len(tokens), "tokens" #stampa la lunghezza in token del file


def calcoloAvgTokens(frasi, tokens): #calcola la media di token per frase
       avgToken = round((len(tokens)*1.0) / (len(frasi)*1.0), 3)
       return avgToken 


def stampaAvgTokens(file, avgTok): #stampa la lunghezza media delle frasi misurata in token
       print "Il file", file, "ha frasi di lunghezza media di", avgTok, "tokens"


def crescitaVocabolario(file1, file2, tokens1, tokens2, x):
       print "COMPARO LA GRANDEZZA DEL VOCABOLARIO DEI DUE TESTI ALL'AUMENTARE DEL CORPUS DI 1000 TOKENS:"
       interv = x #si definisce l'intervallo entro il quale si calcola la grandezza del vocabolario
       while interv < len(tokens1): #finché l'intervallo stabilito rimane inferiore alla lunghezza del testo
              vocabolarioX1 = set(tokens1[0:interv]) #si calcolano i vocabolari di file 1 e 2 prendendo i considerazione un numero di token che va da 0 a intervallo
              vocabolarioX2 = set(tokens2[0:interv])
              print "Il file", file1, "ha", len(vocabolarioX1), "type su", interv, "tokens \------------/ il file", file2, "ha", len(vocabolarioX2), "type su", interv, "tokens" #si stampa la grandezza del vocabolario dei due file entro l'intervallo considerato
              interv = interv + x #si accresce l'intervallo
       if (interv >= len(tokens1)): #quando la dimensione dell'intervallo supera quella del testo allora l'intervallo massimo preso in considerazione diventa uguale e non supera la lunghezza del testo stesso
              print "Il file", file1, "ha", len(set(tokens1)), "type su", len(tokens1), "tokens \------------/ il file", file2, "ha", len(set(tokens2)), "type su", len(tokens2), "tokens"


def crescitaRicchezzaLessicale(file1, file2, tokens1, tokens2, x):
       print "COMPARO LA RICCHEZZA LESSICALE DEI DUE TESTI ALL'AUMENTARE DEL CORPUS DI 1000 TOKENS:"
       interv = x #si definisce l'intervallo entro il quale si calcola la ricchezza lessicale
       while interv < len(tokens1): #finché l'intervallo stabilito rimane inferiore alla lunghezza del testo
              vocabolarioX1 = set(tokens1[0:interv]) #si calcola il vocabolario di file 1 e 2 prendendo i considerazione un numero di token che va da 0 a intervallo
              vocabolarioX2 = set(tokens2[0:interv])
              testoX1 = tokens1[0:interv] #si prende in cosiderazione la lunghezza dei testi 1 e 2 da 0 a intervallo
              testoX2 = tokens2[0:interv]
              print "Il file", file1, "ha una Token Type Ratio di", round(len(vocabolarioX1)*1.0/len(testoX1)*1.0, 3), "su", interv, "tokens \------------/ il file", file2, "ha una Token Type Ratio di", round(len(vocabolarioX2)*1.0/len(testoX2)*1.0, 3), "su", interv, "tokens" #si calcola e stampa la ricchezza lessicale dei due file entro l'intervallo considerato
              interv = interv + x #si accresce l'intervallo
       if (interv >= len(tokens1)): #quando la dimensione dell'intervallo supera quella del testo allora l'intervallo massimo preso in considerazione diventa uguale e non supera la lunghezza del testo stesso
                print "Il file", file1, "ha una Token Type Ratio di", round(len(set(tokens1))*1.0/len(tokens1)*1.0, 3), "su", len(tokens1), "tokens \------------/ il file", file2, "ha una Token Type Ratio di", round(len(set(tokens2))*1.0/len(tokens2)*1.0, 3), "su", len(tokens2), "tokens"


def annotazioneLinguistica(tokens): #Part-Of-Speach tagger per i token presi in input
      tokensPOS = nltk.pos_tag(tokens)
      return tokensPOS #restituisce i tokens taggati


def individuaSostantivi(tokensPos): #si prendono in input token taggati
       sostantiviTOT = []
       cond = ["NN", "NNS", "NNP", "NNPS"] #si stabilisce come condizione una lista di tag
       for tok in tokensPos: #si scorrono tutti i token taggati
                if tok[1] in cond: #se il token appartiene alla lista di tag 
                        sostantiviTOT.append(tok[1]) #si appende il token alla nuova lista che raccoglie tutti i tok che soddisfano la condizione
       return len(sostantiviTOT) #restituisce il numero di token che hanno superato la condizione (sostantivi)


def individuaVerbi(tokensPos): #si prendono in input token taggati                
       verbiTOT = []
       cond = ["VB", "VBD", "VBG", "VBN", "VBZ"] #si stabilisce come condizione una lista di tag
       for tok in tokensPos: #si scorrono tutti i token taggati
                if tok[1] in cond: #se il token appartiene alla lista di tag
                        verbiTOT.append(tok[1]) #si appende il token alla nuova lista che raccoglie tutti i tok che soddisfano la condizione
       return len(verbiTOT) #restituisce il numero di token che hanno superato la condizione (verbi)


def individuaSVAJ(tokensPos): #si prendono in input token taggati
        SVAJ = []
        cond = ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBZ", "RB", "WRB", "JJ", "JJR", "JJS"] #si stabilisce come condizione una lista di tag
        for tok in tokensPos: #si scorrono tutti i token taggati
                  if tok[1] in cond: #se il token appartiene alla lista di tag
                        SVAJ.append(tok[1]) #si appende il token alla nuova lista che raccoglie tutti i tok che soddisfano la condizione
        return len(SVAJ) #restituisce il numero di token che hanno superato la condizione (sostantivi+verbi+avverbi+aggettivi)


def individuaAllButP(tokensPos): #si prendono in input token taggati 
        AllButP = []
        cond = [".", ","] #si stabilisce come condizione una lista di tag
        for tok in tokensPos: #si scorrono tutti i token taggati
                  if tok[1] not in cond: #se il token non appartiene alla lista di tag
                        AllButP.append(tok[1]) #si appende il token alla nuova lista che raccoglie tutti i tok che soddisfano la condizione
        return len(AllButP) #restituisce il numero di token che hanno superato la condizione (tutti tranne la punteggiatura)


def densitaLessicale(tokens): #calcola e restituisce la denistà lessicale dei due file
        return round( (individuaSVAJ(annotazioneLinguistica(tokens))*1.0) / (individuaAllButP(annotazioneLinguistica(tokens))*1.0), 3)


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
       avgTok1 = calcoloAvgTokens(frasi1, tokens1)
       avgTok2 = calcoloAvgTokens(frasi2, tokens2)
       vocabolario1 = set(tokens1) #vocabolario del fil 1
       vocabolario2 = set(tokens2) #vocabolario del file 2
       
       print "CALCOLO IL NUMERO DEI TOKENS:"
       print
       calcoloNTokens(file1, tokens1) #si richiama la funzione per entrambi i file
       calcoloNTokens(file2, tokens2)
       print
       print "CONFRONTO I DUE TESTI SULLA BASE DEL NUMERO DI TOKENS:"
       print
       if len(tokens1) > len(tokens2): #si esegue il confronto per stabilire quale dei due file sia il più lungo e si stampa il risultato
           print "Il file", file1, "è più lungo del file", file2
       elif len(tokens1) < len(tokens2):
           print "Il file", file2, "è più lungo del file", file1
       else:
           print "I due file sono della stessa lunghezza"
       print
       print "///////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "CALCOLO LA LUNGHEZZA MEDIA DELLE FRASI IN TOKENS:"
       print
       stampaAvgTokens(file1, avgTok1) #si richiama la funzione per entrambi i file
       stampaAvgTokens(file2, avgTok2)
       print
       print "CONFRONTO I DUE TESTI SULLA BASE DELLA LUNGHEZZA MEDIA DELLE FRASI IN TOKENS:"
       print
       if avgTok1 > avgTok2: #si confrontano i due file sulla base della lunghezza media delle frasi in token
           print "Le frasi del file", file1, "hanno una lunghezza media maggiore di quelle del file", file2
       elif avgTok1 < avgTok2:
           print "Le frasi del file", file2, "hanno una lunghezza media maggiore di quelle del file", file1
       else:
           print "Le frasi dei due file hanno la stessa lunghezza media"
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "CALCOLO IL VOCABOLARIO DEI DUE TESTI:"
       print #si stampa la lunghezza del vocabolario per entrambi i file
       print "Il file", file1, "ha un vocabolario di", len(vocabolario1), "tokens"
       print "Il file", file2, "ha un vocabolario di", len(vocabolario2), "tokens"
       print
       crescitaVocabolario(file1, file2, tokens1, tokens2, 1000)
       print
       print "////////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "CALCOLO LA RICCHEZZA LESSICALE, COME TYPE TOKEN RATIO, DEI DUE TESTI:"
       print #si calcola la ricchezza lessicale come token type ratio per entrambi i file
       print "Il file", file1, "ha una Type Token Ratio di", round((len(vocabolario1)*1.0) / (len(tokens1)*1.0), 3)
       print "Il file", file2, "ha una Type Token Ratio di", round((len(vocabolario2)*1.0) / (len(tokens2)*1.0), 3)
       print
       crescitaRicchezzaLessicale(file1, file2, tokens1, tokens2, 1000) #si richiama la funzione per il confronto della crescita lessicale per entrambi i file
       print
       print "//////////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "CALCOLO IL RAPPORTO TRA SOSTANTIVI E VERBI:"
       print #si calcola e stampa il rapporto sostantivi/verbi per entrambi i file, mettendoli a confronto
       print "Il file", file1, "ha un rapporto sostantivi/verbi di", round((individuaSostantivi(annotazioneLinguistica(tokens1))*1.0) / (individuaVerbi(annotazioneLinguistica(tokens1))*1.0), 3), "\------------/ il file", file2, "ha un rapporto sostantivi/verbi di", round((individuaSostantivi(annotazioneLinguistica(tokens2))*1.0) / (individuaVerbi(annotazioneLinguistica(tokens2))*1.0), 3)
       print
       print "//////////////////////////////////////////////////////////////////////////////////////////////////////"
       print
       print "COMPARO LA DENSITÀ LESSICALE DEI DUE TESTI, CALCOLATA COME (|Sostantivi|+|Verbi|+|Avverbi|+|Aggettivi|)/(TOT-( |.|+|,| ) ) :"
       print #si stampa la densità lessicale per i due file 
       print "Il file", file1, "ha una densità lessicale di", densitaLessicale(tokens1), "\------------/ il file", file2, "ha una densità lessicale di", densitaLessicale(tokens2)
       
       
       
       
       
         
main(sys.argv[1], sys.argv[2])
