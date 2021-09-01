# EvalEval

This repository contains the code for the paper [Perturbation Checklist for Evaluating NLG Evaluation Metrics]()

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

In this work we provide a detailed analysis of NLG metrics by going beyound correlation with human scores. We propose a comprehensive criteria-checklist based evaluation that will act as a diagnostic tool in pointing out specific avenues of improvement in metrics. We create specific [templates](#templates) that are targeted to test the perfomance of a metric along a particular dimension. <br>

Please find more details of this work in our [paper]().

## Setup

### Install Dependencies

Our code is based on python 3.7 and to install all the dependencies run  <br>

```
pip install -r requirements.txt
```
After installing all dependiencies run
```
python3 initialise.py
```
### Load the data

All the datasets used in our experiments can be directly downloaded from [here](#gdrive-link) or by running the following command

```
bash download.sh
```

To use custom datasets please follow the following format or feel free to make changes in the code to make it compatible<br>
`jsonl` format
```
{'id': 0, 'references':'Tom went to play in the garden', ...}
{'id': 1, 'references':'It will rain today, ...}
.
.

```
`csv` format
```
id, references, ...
0 , Tom went to play in the garden, ..
1 , It will rain today, ..
```
## Templates

All the templates used in our works have been made avaialable in the `templates/` folder and are categorised in the following sections <br>

All tasks have the following criteria , the table can also be found in our paper

| Task| Criteria |
| -----| ------| 
| Machine Translation | Fluency, Adequacy |
| Abstrative Summraization | Fluency , Coherence , Relevance, Coverage, Clarity |
| Image Captioning | Fluency, Throughness , Correctness |
| Data to Text Generation | Fluency ,Coverage , Relevance |
| Question Generation | Fluency , Answerability |
<br> <br>

All the templates save the perturbed sentences along with the original in the `outputs/` folder. To test the metrics perfomance on these, pass the `reference` and `perturbed` sentences and compare the aggregated metric score with the annotations score given for every template.
<br> <br>

### Data-to-Text Generation
To run the perturbations use the following command
```
python3 main.py \
--task D2T  \
--ref_file data/<data.jsonl> \
--output_file example
--linguistic_criteria <all/Fluency/Invariance/Coverage/Relevance>
```

### Image Captioning

To run the perturbations use the following command
```
python3 main.py \
--task IC  \
--ref_file data/<data.jsonl> \
--output_file example
--linguistic_criteria <all/Fluency/Invariance/Completeness/Throughness>
```
### Translation

To run the perturbations use the following command
```

python3 main.py \
--task MT  \
--ref_file data/<data.jsonl> \
--output_file example
--linguistic_criteria <all/Fluency/Invariance/Adequacy>
```

### Dialogue

Coming soon ..

### Summarization

To run the perturbations use the following command
```
python3 main.py \
--task AS  \
--ref_file data/<data.jsonl> \
--output_file example
--linguistic_criteria <all/Fluency/Invariance/Coverage/Relevance/Clarity>
```

### Question Generation

To run the perturbations use the following command
```
python3 main.py \
--task QG  \
--ref_file data/<data.jsonl> \
--output_file example
--linguistic_criteria <all/Fluency/Invariance/Answerability>
```

## Human Evaluations

The human annotations collected for the templates can be downloaded from [here](#gdrive-link)

## Metrics

Coming soon ..

## Citation

If you find our work usefull please cite
```

```
