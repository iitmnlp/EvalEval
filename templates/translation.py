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
        return Perturb.perturb(sent, Perturb.change_number, n=1)[0]

    def modify_names(self, sent):
        return Perturb.perturb(sent, Perturb.change_names, n=1)[0]

    def repeat_phrases(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        l = len(pos)
        rep_word = ''
        flag = 0
        for i in range(l-1):
            w, p = pos[i]
            if i< l*0.25: 
                rep_word += " " +w
                flag = 1
                sen.append(w)
            else:
                sen.append(w)
        sen.append(pos[l-1][0])
        sen.append(rep_word)
        if flag==1: 
            out = " ".join(w for w in sen)
        return out 