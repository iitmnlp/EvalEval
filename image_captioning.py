import re
import spacy
from checklist.editor import Editor
from checklist.perturb import Perturb
import random
from spacy.matcher import Matcher
from num2words import num2words
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


class BaseTemplate:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

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

    def drop_stopwods(self, sent):
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
        pattern = [{'POS': 'AUX'}]
        matcher = Matcher(self.nlp.vocab)
        matcher.add("Verb phrase", None, pattern)
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

    def generate(self, batch):
        raise NotImplementedError

'''
 [
            self.typos(batch),
            self.contrations(batch),
            self.expansions(batch),
            self.no_punct(batch),
            self.add_negation(batch),
            self.jumble(batch),
            self.remove_imp_adjective(batch),
            self.remove_stopwods(batch),
            self.replace_nouns_prouns(batch),
            self.sentence_reorder(batch),
            self.hyponyms(batch),
            self.synonym_adjective(batch),
            self.antonym_adjective(batch),
            self.number2words(batch)
        ]
'''

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
                    syn = Editor.related_words(sent, w)
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
                    syn = Editor.antonyms(sent, w)
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
                    syn = Editor.synonyms(sent, w)
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

    def generate(self, batch):
        return super().generate(batch)

class QuestionGenTempaltes(BaseTemplate):
    def __init__(self):
        super(QuestionGenTempaltes, self).__init__()

    def remove_question_word(self, sent):
        q = ['what','when','where','why','how','whose','whom','who','which']
        wor = word_tokenize(sent)
        sen = [w for w in wor if not w.lower() in q]
        out = " ".join(i for i in sen)
        return out if out!=sent else sent

    def change_question_word(self, sent):
        q = ['what','when','where','why','how','whose','whom','who','which']
        sen = []
        wor = word_tokenize(sent)
        for w in wor:
            if w.lower() in q:
                x = random.randint(0,len(q)-1)
                while q[x] == w.lower():
                    x = random.randint(0,len(q)-1)
                sen.append(q[x])
            else:
                sen.append(w)
        out = " ".join(wo for wo in sen)
        return out if out!=sent else sent

    def change_names(self, sent):
        return Perturb.perturb(sent, Perturb.change_names, n=1).data[0]

    def change_question_to_assetion(self, sent):
        q = ['what','when','where','why','how','whose','whom','who','which']
        toks = nltk.word_tokenize(sent)
        sent = []
        sent2 = []
        l = len(toks)
        for w in toks:
            if w.lower() in q:
                sent.append('{mask}')
            else:
                sent.append(w)
            sent2.append(w)
        ss = " ".join(x for x in sent)
        ss2 = " ".join(x for x in sent2)
        temp = Editor.template(ss, remove_duplicates=True, nsamples=1)
        out = temp['data'][0]
        if out.lower() != ss2.lower():
            out = out.replace("?",".")
        return out if out!=sent else sent

    def generate(self, batch):
        return super().generate(batch)

class DialogueTemplates(BaseTemplate):
    def __init__(self):
        super(DialogueTemplates, self).__init__()

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

    def change_names(self, sent):
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
    
    def generate(self, batch):
        return super().generate(batch)

class SummTemplates(BaseTemplate):
    def __init__(self) -> None:
        super(SummTemplates, self).__init__()

    def sentence_reorder(self, sent):
        text_split = [i.text for i in self.nlp(sent).sents]
        random.shuffle(text_split)
        return " ".join(text_split)

    def replace_nouns_prouns(self, sent):
        toks = sent_tokenize(sent)
        flag=0
        sen = []
        for c in toks:
            pos = nltk.pos_tag(nltk.word_tokenize(c))
            l = len(pos)
            i = 0
            p = pos[0]
            if p in ['NNS' ,'NNPS']:
                sen.append('They')
                flag = 1
                i = 1
            elif p in ['DT']:
                p1 = pos[1]
                if p1 in ['NNS' ,'NNPS']:
                    sen.append('They')
                    flag = 1
                    i = 2
                if p1 == 'NN':
                    sen.append('It')
                    flag = 1
                    i = 2
            while i<l:
                p = pos[i]
                sen.append(c)
                i+=1
        if flag == 1:
            out = " ".join(w for w in sen)

        return out if flag  else sent

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
        if flag==1: #len(sen)<l:
            out = " ".join(w for w in sen)
        return out if flag  else sent

    def repeat_sentences(self, sent):
        toks = sent_tokenize(sent)
        sent = []
        l = len(toks)
        i = 0
        while i<l:
            sent.append(toks[i])
            i+=1
        sent.append(toks[0])
        out = " ".join(x for x in sent)
        return out if out !=sent  else sent
        
def generate(task, linguistic_criteria, batch):
    task_list = {
        'IC': ImageCapTemplates(),
        'MT': TranslationTemplates(),
        'DG': DialogueTemplates(),
        'AS': SummTemplates(),
        'D2T': Data2TextTemplates(),
        'QG': QuestionGenTempaltes()
    }
    
    _task = task_list[task]
    template_list ={
        'Fluency': [
                _task.jumble,
                _task.subject_veb_dis,
                _task.typos,
        ],
        'Invariance' : [
                _task.synonyms,
                _task.contrations,
                _task.expansions,
                _task.number2words
        ],
        'Adequacy': [
            _task.negat,
            _task.drop_phrases

        ],
        'Informativeness': [
            _task.hyponyms
        ],
        'Coherence': [
            _task.sentence_reorder
        ],
        'Calrity':[
            _task.replace_nouns_prouns
        ],
        'Answerability':[
            _task.change_question_word,
            _task.remove_question_word
        ],
        'Relevance':[
            _task.change_names
        ],
        'Correctness':[
            _task.change_gender,
            _task.change_attributes
        ],
        'Throughness':[
            _task.remove_objects,
            _task.repeat_object
        ],
        'Coverage':[
            _task.drop_phrases,
        ]
    }
    # batch foRMAT should be jsonl file
    # RefeRence, candidate
    out = {}
    templates = template_list[linguistic_criteria]
    for operand in templates:
        out[operand.__name__] = map(operand, batch)

    # takes in input as jsonl and RetuRns peRtubed outputs
