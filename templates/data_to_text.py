from checklist.perturb import Perturb
import random
import nltk
from templates.base import BaseTemplate

class Data2TextTemplates(BaseTemplate):
    def __init__(self):
        super(Data2TextTemplates, self).__init__()

    def change_numeric(self, sent):
        return Perturb.perturb(sent, Perturb.change_number, n=1)[0]
    
    def modify_names(self, sent):
        return Perturb.perturb(sent, Perturb.change_names, n=1)[0]

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