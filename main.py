import os
import json
import pandas as pd
from templates.summarization import SummTemplates
from templates.image_captioning import ImageCapTemplates
from templates.dialogue import DialogueTemplates
from templates.question_generation import QuestionGenTempaltes
from templates.data_to_text import Data2TextTemplates
from templates.translation import TranslationTemplates
import argparse

def _generate(args, batch):
    task_list = {
        'IC': ImageCapTemplates(),
        'MT': TranslationTemplates(),
        'DG': DialogueTemplates(),
        'AS': SummTemplates(),
        'D2T': Data2TextTemplates(),
        'QG': QuestionGenTempaltes()
    }
    
    _task = task_list[args.task]
    if args.task =='MT':
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_veb_dis,
                _task.typos,
                _task.remove_punct,
                _task.drop_stopwords,
                _task.hyponyms,            # TODO fix bug
                _task.drop_adjectives

            ],
            'Invariance' : [
                _task.synonym_adjective,  # TODO fix bug
                _task.antonym_adjective,  # TODO fix bug
                _task.contrations,
                _task.expansions,
                _task.number2words
            ],
            'Adequacy': [
                _task.add_negation,  
                #_task.drop_phrases,  TODO
                _task.repeat_phrases,
                _task.change_numeric, 
                _task.change_names, 
                _task.only_stop,

        ]
        }
    elif args.task =='IC':
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_veb_dis,
                _task.typos,
                _task.remove_punct,
                _task.drop_stopwords,
                _task.add_negation, 
                _task.hyponyms,
                _task.drop_adjectives

            ],
            'Invariance' : [
                _task.synonym_adjective,
                _task.antonym_adjective,
                _task.contrations,
                _task.expansions,
                _task.number2words
            ],
            'Correctness':[
                _task.change_gender,
                _task.change_attributes,
                _task.change_object_order,
                _task.replace_object_with_synonym

            ],
            'Throughness':[
                _task.drop_objects,
                _task.repeat_object
            ],
        }
    elif args.task =='AS':
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_veb_dis,
                _task.typos,
                _task.remove_punct,
                _task.drop_stopwords,
                _task.add_negation,  
                _task.hyponyms,
                _task.drop_adjectives

            ],
            'Invariance' : [
                _task.synonym_adjective,
                _task.antonym_adjective,
                _task.contrations,
                _task.expansions,
                _task.number2words
            ],
            'Coherence': [
                _task.sentence_reorder,
                _task.repeat_sentences
        ],
            'Relevance':[
                _task.change_names
        ],
            'Coverage':[
                _task.drop_phrases,
        ],
            'Calrity':[
                _task.replace_nouns_prouns  # TODO fix bugs
            ],
        }
    elif args.task =='D2T':
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_veb_dis,
                _task.typos,
                _task.remove_punct,
                _task.drop_stopwords,
                _task.add_negation,  
                _task.hyponyms,
                _task.drop_adjectives
            ],
            'Invariance' : [
                _task.synonym_adjective,
                _task.antonym_adjective,
                _task.contrations,
                _task.expansions,
                _task.number2words
            ],
            'Relevance':[
                _task.change_names,
                _task.change_numeric
            ],
            'Coverage':[
                _task.drop_phrases,
                _task.repeat_phrases
            ]
        }
    elif args.task =='QG':
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_veb_dis,
                _task.typos,
                _task.remove_punct,
                _task.drop_stopwords,
                _task.add_negation,   
                _task.hyponyms,
                _task.drop_adjectives
            ],
            'Invariance' : [
                _task.synonym_adjective,
                _task.antonym_adjective,
                _task.contrations,
                _task.expansions,
                _task.number2words
            ],
            'Answerability':[
                _task.change_question_word,
                _task.remove_question_word,
                #_task.change_question_to_assetion,  TODO fix bug
                _task.change_names
            ]
        }
    data =[]
    if args.criteria == 'all':
        templates = [j for i in template_list.values() for j in i]
    else:
        try:
            templates = template_list[args.criteria]
        except:
            print('Please use the criteria mentioned in the list')
    for operand in templates:
        out = map(operand, batch)
        c = len(data)
        for i,j in zip(out, batch):
            if i ==j:
                continue
            data.append({'type':operand.__name__, 'reference': j, 'perturbed': i})
        print(len(data)-c, operand.__name__)

    with open('outputs/' + args.output_file + '-'+args.criteria +'.jsonl' , 'w') as fp:
        for i in data:
            json.dump(i, fp)
    fp.close()

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, 
                            choices=['IC','MT','QG','D2T','DG','AS'], 
                            help='The nlp task in consideration')
    parser.add_argument('--criteria',
                                choices=['Fluency','Invariance','Adequacy','Informativeness','Coherence',
                                'Answerability','Relevance','Correctness','Throughness','Coverage','Calrity'] ,
                                type=str, help='The linguistic dimension')
    parser.add_argument('--ref_file', type=str, help='input reference file(supports cvs/jsonl')
    parser.add_argument('--output_file', default='output.jsonl', type=str, help='output file')
    args = parser.parse_args()
    if 'csv' == args.ref_file.split('.')[-1]:
        df = pd.read_csv(args.ref_file)
        try:
            batch = df['sentences'].values
        except KeyError as msg:
            print(msg, 'please use the given naming convention')
            exit()
    elif 'jsonl' == args.ref_file.split('.')[-1]:
        batch =[]
        with open(args.ref_file) as f:
            for line in f:
                data = json.loads(line)
                try:
                    batch.append(data['references'][0])
                except KeyError as msg:
                    print(msg,'please format the input file correctly')
                    exit()
        f.close()
    else:
        print('Currently only supporting csv and jsonl extensions')
        raise NotImplementedError
    _generate(args, batch)