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
    ## TODO : need to split this into multiple dictonaies based on task as some templates
    ## aen't defined foR some tasks
    template_list ={
    #     'Fluency': [
    #             _task.jumble,
    #             _task.subject_veb_dis,
    #             _task.typos,
    #     ],
    # 
        'Invariance' : [
                _task.synonym_adjective,
                _task.contrations,
                _task.expansions,
                _task.number2words
        ],
    }
    #     'Adequacy': [
    #         _task.add_negation,
    #         _task.drop_phrases

    #     ],
    #     'Informativeness': [
    #         _task.hyponyms
    #     ],
    #     'Coherence': [
    #         _task.sentence_reorder
    #     ],
    #     'Calrity':[
    #         _task.replace_nouns_prouns
    #     ],
    #     'Answerability':[
    #         _task.change_question_word,
    #         _task.remove_question_word
    #     ],
    #     'Relevance':[
    #         _task.change_names
    #     ],
    #     'Correctness':[
    #         _task.change_gender,
    #         _task.change_attributes
    #     ],
    #     'Throughness':[
    #         _task.remove_objects,
    #         _task.repeat_object
    #     ],
    #     'Coverage':[
    #         _task.drop_phrases,
    #     ]
    # }
    data =[]
    templates = template_list[args.linguistic_criteria]
    for operand in templates:
        out = map(operand, batch)
        for i,j in zip(out, batch):
            if i ==j:
                continue
            data.append({'type':operand.__name__, 'reference': j, 'perturbed': i})

    with open('outputs/' + args.output_file + '-'+args.linguistic_criteria +'.jsonl' , 'w') as fp:
        for i in data:
            json.dump(i, fp)
    fp.close()

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, 
                            choices=['IC','MT','QG','D2T','DG','AS'], 
                            help='The nlp task in consideration')
    parser.add_argument('--linguistic_criteria',
                                choices=['Fluency','Invariance','Adequacy','Informativeness','Coherence',
                                'Answerability','Relevance','Correctness','Throughness','Coverage'] ,
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