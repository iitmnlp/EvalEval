# EvalEval

This repository contains the code for the paper [Perturbation CheckLists for Evaluating NLG Evaluation Metrics](https://arxiv.org/abs/2109.05771) to appear at **EMNLP, 2021**.

Authors: **Ananya B. Sai**, **Tanay Dixit**, **Dev Yashpal Sheth**, **Sreyas Mohan** and **Mitesh M. Khapra**.

Webpage: [https://iitmnlp.github.io/EvalEval/](https://iitmnlp.github.io/EvalEval/)

## Contents

- [Overview](#overview)
- [Setup](#setup)
- [Templates](#templates)
  - [Data-to-Text Generation](#data-to-text-generation)
  - [Image Captioning](#image-captioning)
  - [Translation](#translation)
  - [Dialogue](#dialogue)
  - [Summarization](#Summarization)
  - [Question Generation](#question-generation)
- [Human Evaluations](#human-evaluations)
- [Metrics](#metircs)
- [Citation](#citation)

## Overview

In this work we provide a detailed analysis of NLG metrics by going beyond correlation with human scores. We propose a comprehensive criteria-checklist based evaluation that will act as a diagnostic tool in pointing out specific avenues of improvement in metrics. We create specific [templates](#templates) that are targeted to evaluate the ability of a metric to capture a particular dimension. <br>

Please find more details of this work in our [paper](https://arxiv.org/abs/2109.05771).

## Setup

### Install Dependencies

Our code is based on python 3.7 and to install all the dependencies run the following command. <br>

```
pip install -r requirements.txt
```
### Load the data

All the original datasets used in our experiments can be directly downloaded by running the following command.

```
cd data
bash download.sh
```

To use custom datasets please follow the following format or feel free to make changes in the code to make it compatible. <br>
`jsonl` format
```
{'id': 0, 'references':'Tom went to play in the garden', ...}
{'id': 1, 'references':'It will rain today', ...}
.
.

```
`csv` format
```
id, references, ...
0 , Tom went to play in the garden, ..
1 , It will rain today, ..
```

**Note**:  DG follows a different format than the rest

## Templates

All the templates used in our works have been made available in the `templates/` folder and are categorized in the following sections. <br>

All tasks have the following criteria, the table can also be found in our paper.

| Task| Criteria |
| -----| ------| 
| Machine Translation (MT) | Fluency, Adequacy |
| Abstrative Summarization (AS)| Fluency, Coherence, Relevance, Coverage, Clarity |
| Image Captioning (IC)| Fluency, Thoroughness, Correctness |
| Data to Text Generation (D2T)| Fluency, Correctness, Coverage, Relevance |
| Question Generation (QG)| Fluency, Answerability, Relevance |
| Dialogue Generation (DG)| Fluency, Relevance, Making sense, Interesting, Avoid Repetition |

<br> 

All the templates save the perturbed sentences along with the original in the `outputs` folder. To test the metrics performance on these, pass the `reference` and `perturbed` sentences and compare the aggregated metric score over the entire dataset with the annotations score given for every template. More details can be found in the [metrics section](#metrics).
<br> 

### Data-to-Text Generation
To run the perturbations use the following command.
```
python3 main.py \
        --task D2T  \
        --ref_file data/<data.jsonl> \
        --output_file example \
        --criteria <all/Fluency/Invariance/Coverage/Relevance>
```

### Image Captioning

To run the perturbations use the following command.
```
python3 main.py \
        --task IC  \
        --ref_file data/<data.jsonl> \
        --output_file example \
        --criteria <all/Fluency/Invariance/Completeness/Throughness>
```
### Machine Translation

To run the perturbations use the following command.
```
python3 main.py \
        --task MT  \
        --ref_file data/<data.jsonl> \
        --output_file example \
        --criteria <all/Fluency/Invariance/Adequacy>
```

### Dialogue Generation

To run the perturbations use the following command.
```
python3 main.py \
        --task DG  \
        --ref_file data/<data.csv> \
        --output_file example \
        --criteria <all/Fluency/Invariance/Avoid-repetition/Making-sense>
```

### Abstrative Summarization

To run the perturbations use the following command.
```
python3 main.py \
        --task AS  \
        --ref_file data/<data.jsonl> \
        --output_file example \
        --criteria <all/Fluency/Invariance/Coverage/Relevance/Clarity>
```

### Question Generation

To run the perturbations use the following command.
```
python3 main.py \
        --task QG  \
        --ref_file data/<data.jsonl> \
        --output_file example \
        --criteria <all/Fluency/Invariance/Answerability>
```

## Human Evaluations

The human annotations collected for the perturbation templates can be downloaded from [here](https://drive.google.com/drive/folders/1UCyPb5FM-VPggwYwsRY4d7_nNseK8ZFM?usp=sharing).

We also used the human judgement scores collected along multiple criteria for different tasks from the following sources: <br>

| Task| Link(s) |
| -----| ------| 
| AS| [data+instructions](https://github.com/Yale-LILY/SummEval#human-annotations) |
| IC| [data](https://www.dropbox.com/s/z1l4o3j0gj8yyp8/AMT_eval.zip?dl=0) , [instructions](https://imagesdg.wordpress.com/image-to-scene-description-graph/) |
| D2T| [data+ instructions](https://github.com/WebNLG/challenge-2020/tree/main/evaluation/human-evaluation/results) |
| QG| [data](https://github.com/PrekshaNema25/Answerability-Metric/tree/master/annotated-questions) |
| DG| [data+instructions](https://github.com/facebookresearch/ParlAI/tree/controllable_dialogue_archive/projects/controllable_dialogue) |

<br> 


## Metrics

We followed the implementation of metrics with the help of the following repositories:
 For BLEU, METEOR, ROUGE-L, CIDEr, Embedding Averaging, Greedy Matching, and Vector Extrema, we use the implementation provided by [Sharma et al. (2017)](https://github.com/Maluuba/nlg-eval). For chrF++, TER, BERTScore, and BLEURT, we use the repository of [Castro Ferreira et al. (2020)](https://github.com/WebNLG/GenerationEval).  For SMS, WMDo, and Mover-Score, we use the implementation provided by [Fabbri et al. (2020)](https://github.com/Yale-LILY/SummEval). For all the remaining task-specific metrics, we use the official codes from the respective papers.

## Citation

```
@InProceedings{Sai_2021_EMNLP,
    author = {Sai, Ananya B. and Dixit, Tanay and Sheth, Dev Yashpal and Mohan, Sreyas and Khapra, Mitesh M.},
    title = {Perturbation CheckLists for Evaluating NLG Evaluation Metrics},
    booktitle = {Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP)},
    month = {November},
    year = {2021}
}
```
