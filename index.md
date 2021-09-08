# EvalEval

This webpage and repository are complementary to the paper [Perturbation Checklist for Evaluating NLG Evaluation Metrics]()

## Contents

- [Overview](#overview)
- [Criteria](#criteria)
  - [Correlations of criteria](#correlations-of-criteria)
- [Templates](#templates)
- [Code](#code)
- [Human Evaluations](#human-evaluations)
- [Metrics](#metrics)
- [Citation](#citation)

## Overview

In this work we provide a detailed analysis of NLG metrics by going beyond correlation with human scores. We propose a comprehensive criteria-checklist based evaluation that will act as a diagnostic tool in pointing out specific avenues of improvement in metrics. We create specific [templates](#templates) that are targeted to test the performance of a metric along a particular dimension. <br>

Please find more details of this work in our [paper]().

## Criteria

Each of the NLG tasks have the following criteria, the table can also be found in our paper and has been referred from the survey paper, [A Survey of Evaluation Metrics Used for NLG Systems](https://arxiv.org/abs/2008.12009)

| Task| Criteria |
| -----| ------| 
| Machine Translation | Fluency, Adequacy |
| Abstrative Summarization | Fluency , Coherence , Relevance, Coverage, Clarity |
| Image Captioning | Fluency, Thoroughness , Correctness |
| Data to Text Generation | Fluency ,Correctness, Coverage , Relevance |
| Question Generation | Fluency , Answerability, Relevance |
| Dialogue | Fluency, Relevance, Making sense, Interesting, Avoid Repetition |

<br> 

### Correlations of criteria

Do these criteria correlate with each other?

<img src="https://user-images.githubusercontent.com/23221743/132134073-64e11188-4901-442a-9de1-9f3618120e62.png" width="500"/>


## Templates

The following examples illustrate the perturbations created by each template for different NLG tasks and criteria.

<!---![perturbations_egs](https://user-images.githubusercontent.com/23221743/132132947-9ffaf335-ddd6-472d-b809-d4e84a51362f.png)--->
<div style="text-align: center">
<img src="https://user-images.githubusercontent.com/23221743/132132947-9ffaf335-ddd6-472d-b809-d4e84a51362f.png" align="center"/></div>

<!--- ![perturbations_examples](./figures/result_table.png) --->

All the templates used in our works have been made available in the `templates/` folder and are categorized by the tasks <br>


## Code

The code is publicly available [here](https://github.com/iitmnlp/EvalEval).

## Human Evaluations

The human annotations collected for the templates can be downloaded from [here](#gdrive-link)

## Metrics



## Citation

If you find our work useful please cite
```

```
