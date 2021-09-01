from checklist.editor import Editor
from checklist.perturb import Perturb
import random
import nltk
from nltk.corpus import stopwords
from templates.base import BaseTemplate
from nltk.tokenize import word_tokenize


class TranslationTemplates(BaseTemplate):
    def __init__(self):
        super(TranslationTemplates, self).__init__()

    def only_stop(self, sent):
        stop = set(stopwords.words('english'))
        wor = word_tokenize(sent)
        sen = [w for w in wor if not w in stop]
        out = " ".join(i for i in sen)
        return out

    def change_numeric(self, sent):
        text = self.nlp(sent)
        x = Perturb.perturb([text], Perturb.change_number, n=1).data
        return sent if  x==[] else x[0][1]

    def change_names(self, sent):
        text = self.nlp(sent)
        x = Perturb.perturb([text], Perturb.change_names, n=1).data
        return sent if  x==[] else x[0][1]

    def drop_phrases(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        l = len(pos)
        flag = 0
        le = round(l*0.2)
        x = random.randint(0,le-1)
        y = 0
        for i in range(l-1):
            w, p = pos[i]
            if x<=i and y < round(l*0.2): 
                y+=1
                flag = 1
                continue
            else:
                sen.append(w)
        sen.append(pos[l-1][0])
        if flag==1: 
            out = " ".join(w for w in sen)
        return out if flag  else sent