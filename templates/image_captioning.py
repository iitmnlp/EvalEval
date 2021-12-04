from checklist.editor import Editor
from templates.base import BaseTemplate
import nltk

class ImageCapTemplates(BaseTemplate):

    def __init__(self) -> None:
        super(ImageCapTemplates, self).__init__()

    def change_attributes(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        l = len(pos)
        sen = []
        flag = 0
        for i in range(l):
            w, p = pos[i]
            if p in ['JJ', 'JJR', 'JJS']:
                try:
                    syn = Editor().related_words(sent, w)
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

    def change_gender(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        l = len(pos)
        sen = []
        flag = 0
        for i in range(l):
            w, p = pos[i]
            if p in ['NN','NNP']: 
                try:
                    syn = Editor().antonyms(sent, w)
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

    def drop_objects(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        l = len(pos)
        for i in range(l-1):
            w, p = pos[i]
            if p in ['NN','NNP' ,'NNS' ,'NNPS']: 
                continue
            else:
                sen.append(w)
        sen.append(pos[l-1][0])
        if len(sen)<l:
            out = " ".join(w for w in sen)
        return out if len(sen)<l  else sent

    def replace_object_with_synonym(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        l = len(pos)
        sen = []
        flag = 0
        for i in range(l):
            w, p = pos[i]
            if p in ['NN','NNP' ,'NNS' ,'NNPS']: 
                try:
                    syn = Editor().synonyms(sent, w)
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

    def repeat_object(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        l = len(pos)
        rep_word = ''
        flag = 0
        for i in range(l-1):
            w, p = pos[i]
            if flag == 0 and p in ['NN','NNP' ,'NNS' ,'NNPS']: 
                rep_word = w
                flag = 1
                sen.append(w)
            else:
                sen.append(w)
        sen.append(rep_word)
        sen.append(pos[l-1][0])
        if flag==1: 
            out = " ".join(w for w in sen)
        return out if flag  else sent

    def change_object_order(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        locs = []
        objs = []
        l = len(pos)
        rep_word = ''
        flag = 0
        for i in range(l-1):
            w, p = pos[i]
            if p in ['NN','NNS']: 
                objs.append(w)
                locs.append(i)
                flag = 1
                sen.append(w)
            else:
                sen.append(w)
        sen.append(pos[l-1][0])
        
        if flag==1 and len(objs)>1: 
            x1 = locs[0]
            x2 = locs[-1]
            tmp = sen[x1] 
            sen[x1] = sen[x2]
            sen[x2] = tmp
            out = " ".join(w for w in sen)
        return out if flag==1 and len(objs)>1  else sent
