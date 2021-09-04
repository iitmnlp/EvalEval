import re
import spacy
from checklist.editor import Editor
from checklist.perturb import Perturb
import random
from spacy.matcher import Matcher
from num2words import num2words
import nltk

class BaseTemplate:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def no_punct(self, sent):
        return re.sub(r'[^\w\s]', ' ', sent) 

    def typos(self, sent):
        return Perturb.add_typos(sent)

    def contrations(self, sent):
        x = Perturb.contract(sent)
        return x if x != sent else sent

    def expansions(self, sent):
        x = Perturb.expand_contractions(sent)
        return x if x != sent else sent

    def add_negation(self, sent):
        x = Perturb.add_negation(self.nlp(sent)) 
        return x if x != sent and x else sent

    def jumble(self, sent):
        tokens = [i.text for i in self.nlp(sent)]
        random.shuffle(tokens)
        return ' '.join(tokens)

    def remove_stopwods(self, sent):
        all_stopwords = self.nlp.Defaults.stop_words
        x  = [word.text for word in self.nlp(sent) if not word.text in all_stopwords]
        return ' '.join(x)
    
    def synonym_adjective(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        flag = 0
        sen =[]
        for i in range(len(pos)):
            w, p = pos[i]
            if p in ['JJ', 'JJR', 'JJS']:
                try:
                    syn = Editor.synonyms(sent, w)
                except:
                    syn = []
                if len(syn) > 0:
                    sen.append(syn[0])
                    flag = 1
                else:
                    sen.append(w)
            else:
                sen.append(w)
        if flag == 1:
            out = " ".join(x for x in sen)

        return out if flag  else sent

    def antonym_adjective(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        flag = 0
        sen =[]
        for i in range(len(pos)):
            w, p = pos[i]
            if p in ['JJ', 'JJR', 'JJS']:
                try:
                    syn = Editor.antonyms(sent, w)
                except:
                    syn = []
                if len(syn) > 0:
                    sen.append(syn[0])
                    flag = 1
                else:
                    sen.append(w)
            else:
                sen.append(w)
        if flag == 1:
            out = " ".join(x for x in sen)

        return out if flag  else sent

    def hyponyms(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        flag = 0
        for i in range(len(pos)):
            w, p = pos[i]
            if p in ['NN','NNP','VB','VBP']:
                try:
                    syn = Editor.hyponyms(sent, w)
                except:
                    syn = []
                if len(syn) > 0:
                    sen.append(syn[0])
                    flag += 1
                else:
                    sen.append(w)
            else:
                sen.append(w)
        if flag > 0:
            out = " ".join(x for x in sen)
        return out if flag  else sent

    def remove_imp_adjective(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        for i in range(len(pos)):
            w, p = pos[i]
            if p in ['JJ', 'JJR', 'JJS'] and pos[i+1][1] in ['NN','NNP' ,'NNS' ,'NNPS']:
                continue
            else:
                sen.append(w)
        sen.append(pos[len(pos)-1][0])
        if len(sen)<len(pos):
            out = " ".join(w for w in sen)
        return out if len(sen)<len(pos)  else sent
    
    def subject_veb_dis(self, sent):
        cases = {'was':'were', 
                'were':'was', 
                'is':'are',
                'are':'is', 
                'has':'have',
                'have':'has',
                'does':'do',
                'do':'does'}
        sentence =''
        doc = self.nlp(sent)
        for i in doc:
            if i.pos_ =="AUX":
                try:
                    w = cases[i.text]
                except:
                    w =i.text
                sentence  = sentence + w + ' '
            else:
                sentence = sentence + i.text + ' '
        return sentence.strip()
        
    def number2words(self, sent):
        out = ''
        for i in sent.split(' '):
            if i.isdigit():
                out = out + num2words(i) + ' '
            else:
                out = out + i + ' '
        return out.strip()
    
    def repeat_phrases(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        l = len(pos)
        rep_word = ''
        flag = 0
        for i in range(l-1):
            w, p = pos[i]
            if i< l*0.25:
                rep_word += " " + w
                flag = 1
                sen.append(w)
            else:
                sen.append(w)
        sen.append(pos[l-1][0])
        sen.append(rep_word)
        if flag==1: 
            out = " ".join(w for w in sen)
        return out if flag  else sent