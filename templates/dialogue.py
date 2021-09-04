from templates.base import BaseTemplate
import re
import random
from checklist.perturb import Perturb
class DialogueTemplates(BaseTemplate):
    def __init__(self):
        super(DialogueTemplates, self).__init__()

    def contractions(self, sent, context):
        return super().contractions(sent)
    
    def expansions(self, sent, context):
        return super().expansions(sent)

    def remove_punct(self, sent, context):
        return super().remove_punct(sent)

    def typos(self, sent, context):
        return super().typos(sent)

    def add_negation(self, sent, context):
        return super().add_negation(sent)

    def jumble(self, sent, context):
        return super().jumble(sent)

    def drop_stopwords(self, sent, context):
        return super().drop_stopwords(sent)

    def synonym_adjective(self, sent, context):
        return super().synonym_adjective(sent)

    def antonym_adjective(self, sent, context):
        return super().antonym_adjective(sent)

    def hyponyms(self, sent, context):
        return super().hyponyms(sent)

    def subject_verb_dis(self, sent, context):
        return super().subject_veb_dis(sent)

    def number2words(self, sent, context):
        return super().number2words(sent)

    def drop_adjectives(self, sent, context):
        return super().drop_adjectives(sent)
    
    def repeat_phrases(self, sent, context):
        return super().repeat_phrases(sent)

    @staticmethod
    def preprocess_sent(i):
        return re.sub(r'[FS]S *:', '', i).strip()

    def negate_previous_utterance(self,sent, context):
        x = context.strip().split('\n')
        l = len(x)
        flag = 0
        if l > 1:
            if l%2 == 0:
                y = random.randrange(0,l-1,2)
            else:
                y = random.randrange(1,l-1,2)
            pr = self.preprocess_sent(x[y])
            try:
                k =Perturb.add_negation(self.nlp(pr)) 
                flag = 1
            except:
                pass
        if flag==1: 
            return str(k)
        return sent

    def repeat_itself(self, sent, context):
        x = context.strip().split('\n')
        le = len(x)
        flag = 0
        if le > 1:
            if le%2 == 0:
                y = random.randrange(0,le-1,2)
            else:
                y = random.randrange(1,le-1,2)
            pr = self.preprocess_sent(x[y])
            flag = 1
        if flag==1:
            return pr
        return sent

    def repeat_last_speaker(self, sent, context):
        x = context.strip().split('\n')
        pr = self.preprocess_sent(x[-1])
        return pr

    def sorry_reply(self, sent, context):
        return  "I'm sorry, can you repeat?"

    def generic(self, sent, context):
        ra = ["Yes", "ok", "thank you", "bye"]
        return random.choice(ra)