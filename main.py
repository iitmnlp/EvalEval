import os
import json
import pandas as pd
from templates.summarization import SummTemplates
from templates.image_captioning import ImageCapTemplates
from templates.dialogue import DialogueTemplates
from templates.question_generation import QuestionGenTemplates
from templates.data_to_text import Data2TextTemplates
from templates.translation import TranslationTemplates
import argparse

def _generate(args, batch, ids):
    task_list = {
        'IC': ImageCapTemplates(),
        'MT': TranslationTemplates(),
        'DG': DialogueTemplates(),
        'AS': SummTemplates(),
        'D2T': Data2TextTemplates(),
        'QG': QuestionGenTemplates()
    }
    
    _task = task_list[args.task]
    if args.task =='MT':
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_verb_dis,
                _task.typos,
                _task.remove_punct,
                _task.drop_stopwords,
                _task.hyponyms,            
                _task.drop_adjectives

            ],
            'Invariance' : [
                _task.synonym_adjective,  
                _task.antonym_adjective,  
                _task.contractions,
                _task.expansions,
                _task.number2words
            ],
            'Adequacy': [
                _task.add_negation,  
                _task.drop_phrases,  
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
                _task.subject_verb_dis,
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
                _task.contractions,
                _task.expansions,
                _task.number2words
            ],
 
            'Calrity':[
                _task.replace_nouns_pronouns  
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
                _task.subject_verb_dis,
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
                _task.contractions,
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
            'Clarity':[
                _task.replace_nouns_prouns  
            ],
        }
    elif args.task =='D2T':
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_verb_dis,
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
                _task.change_names,
                _task.change_numeric,
                _task.add_negation,  
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
                _task.subject_verb_dis,
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
                _task.contractions,
                _task.expansions,
                _task.number2words
            ],
            'Answerability':[
                _task.change_question_word,
                _task.remove_question_word,
                _task.change_question_to_assetion, 
                _task.change_names
            ]
        }
    elif args.task =='DG':
        speaker, context = batch
        template_list ={
            'Fluency': [
                _task.jumble,
                _task.subject_verb_dis,
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
                _task.contractions,
                _task.expansions,
                _task.number2words
            ],
            'Avoid repetition': [
                _task.repeat_itself,
                _task.repeat_last_speaker
            ],
            'Making sense': [
                _task.negate_previous_utterance,
            ],
            'Interesting' : [
                _task.sorry_reply,
                _task.generic
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
        if args.task !='DG':
            out = map(operand, batch)
            for i,j,k in zip(out, batch, ids):
                if i ==j:
                    continue
                data.append({'type':operand.__name__,'id':k, 'reference': j, 'perturbed': i})
        else:
            out = map(operand, speaker, context)
            for i,j,k in zip(out, speaker, ids):
                if i ==j:
                    continue
                data.append({'type':operand.__name__,'id':k, 'reference': j, 'perturbed': i})

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
                                'Answerability','Relevance','Correctness','Throughness','Coverage','Clarity','all'] ,
                                type=str, help='The linguistic dimension')
    parser.add_argument('--ref_file', type=str, help='input reference file(supports cvs/jsonl')
    parser.add_argument('--output_file', default='output.jsonl', type=str, help='output file')
    args = parser.parse_args()

    if args.task !='DG':
        if 'csv' == args.ref_file.split('.')[-1]:
            df = pd.read_csv(args.ref_file)
            try:
                batch = list(df['sentences'].values)
                ids = list(df['id'].values)
            except KeyError as msg:
                print(msg, 'please use the given naming convention')
                exit()
        elif 'jsonl' == args.ref_file.split('.')[-1]:
            batch =[]
            ids =[]
            with open(args.ref_file) as f:
                for line in f:
                    data = json.loads(line)
                    try:
                        batch.append(data['references'])
                        ids.append(data['id'])
                    except KeyError as msg:
                        print(msg,'please format the input file correctly')
                        exit()
            f.close()
    elif args.task =='DG':
        if 'csv' == args.ref_file.split('.')[-1]:
            df = pd.read_csv(args.ref_file)
            try:
                context = list(df['contexts'].values)
                batch = (list(df['resp1'].values), context)
            except KeyError as msg:
                print(msg, 'please use the given naming convention')
                exit()
        else:
            print('Only supports csv files !')

    if 'csv' == args.ref_file.split('.')[-1]:
        df = pd.read_csv(args.ref_file)
        try:
            batch = list(df['sentences'].values)
            ids = list(df['id'].values)
        except KeyError as msg:
            print(msg, 'please use the given naming convention')
            exit()
    elif 'jsonl' == args.ref_file.split('.')[-1]:
        batch =[]
        ids =[]
        with open(args.ref_file) as f:
            for line in f:
                data = json.loads(line)
                try:
                    batch.append(data['references'])
                    ids.append(data['id'])
                except KeyError as msg:
                    print(msg,'please format the input file correctly')
                    exit()
        f.close()
    else:
        print('Currently only supporting csv and jsonl extensions')
        raise NotImplementedError
    _generate(args, batch, ids)
