# paraphraseDecanlpCorpus
Paraphrases of [decaNLP](https://github.com/salesforce/decaNLP) questions. E.g.
```
What is the synopsis?
Give me a condensed version
Sum up the article
What would be a good summary of the article?
Sum it up
```

Dataset for the paper [Ask me in your own words: paraphrasing for multitask question answering](https://peerj.com/articles/cs-759).

## Using with the decaNLP code
The `templates` folder contains the question paraphrases gathered from mechanical turk, one-per-line. These have already been split 70:30 into train/test sets.

To use the dataset with decaNLP, you first need to slightly modify the [decaNLP code](https://github.com/salesforce/decaNLP) to dump the task data as jsonl files. First apply the patch:
```
git clone https://github.com/salesforce/decaNLP
cd decaNLP
git apply ../save_jsonl.patch 
```

Then follow the decaNLP instructions to run the `train.py`/`evaluate.py` scripts (just to download the data for the first time). In the `decaNLP/.data` directory you should now also have `.jsonl` files containing `question`, `context`, `answer` keys.

Running:
```
python makeCorpus.py --data decaNLP/.data --templates templates/ --output paraphrase_corpus
```
will expand the templates using the decaNLP data. You'll end up with the following structure:
```
outputFolder/
├── train/
│   ├── WOZ0
│   │    └── train.jsonl
│   ├── WOZ1
│   │    └── train.jsonl
│   ...
└── test/
    ├── WOZ0
    │    └── val.jsonl
    ├── WOZ1
    │    └── val.jsonl
    ...
```
Each set can be then used for training/evaluating individually, or can be merged together using `makeTraining.sh` to make a single training set per task based on picking a random paraphrase for each training instance.

## Annotated data

`annotated.json` contains paraphrase annotations for each of the examples in the test set.

## Trained T5 checkpoints

Checkpoints for the T5 checkpoints to evaluate this corpus are [here](https://drive.google.com/drive/folders/1RbIrGzfj0LUQ_qGCEVsyUyIf3y3pB3y6?usp=sharing)

## Citation
If you use this dataset in your work, please cite:
```
@article{hudson2021askme,
 title = {Ask me in your own words: paraphrasing for multitask question answering}
 author = {G. Thomas Hudson and Noura Al Moubayed},
 doi = {10.7717/peerj-cs.759},
 year = 2021,
 publisher = {{PeerJ}},
 volume = {7},
 pages = {e759},
} 
```

The dataset in this project (files under the `templates/` dir and the `annotation.json` file) is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/), and the underlying source code used to create and process that data is licensed under the [MIT](https://github.com/github/choosealicense.com/blob/gh-pages/LICENSE.md).

### Dataset Metadata
The following table is necessary for this dataset to be indexed by search
engines such as <a href="https://g.co/datasetsearch">Google Dataset Search</a>.
<div itemscope itemtype="http://schema.org/Dataset">
<table>
  <tr>
    <th>property</th>
    <th>value</th>
  </tr>
  <tr>
    <td>name</td>
    <td><code itemprop="name">PQ-decaNLP</code></td>
  </tr>
  <tr>
    <td>alternateName</td>
    <td><code itemprop="alternateName">Paraphrase Questions - decaNLP</code></td>
  </tr>
  <tr>
    <td>name</td>
    <td><code itemprop="name">PQ-decaNLP</code></td>
  </tr>
  <tr>
    <td>url</td>
    <td><code itemprop="url">https://github.com/ghomasHudson/paraphraseDecanlpCorpus</code></td>
  </tr>
  <tr>
    <td>description</td>
    <td><code itemprop="description">Multitask learning has led to significant advances in Natural Language Processing, including the decaNLP benchmark where question answering is used to frame 10 natural language understanding tasks in a single model. PQ-decaNLP is a crowd-sourced corpus of paraphrased questions, annotated with paraphrase phenomena. This enables analysis of how transformations such as swapping the class labels and changing the sentence modality lead to a large performance degradation.
      
This repository contains question templates and scripts for using this with the decaNLP code.</code></td>
  </tr>
  <tr>
    <td>citation</td>
    <td><code itemprop="citation">https://doi.org/10.7717/peerj-cs.759</code></td>
  </tr>
    
  <tr>
    <td>creator</td>
    <td>
      <div itemscope itemtype="http://schema.org/Person" itemprop="creator">
        <table>
          <tr>
            <th>property</th>
            <th>value</th>
          </tr>
          <tr>
            <td>name</td>
            <td><code itemprop="name">Thomas Hudson</code></td>
          </tr>
          <tr>
            <td>sameAs</td>
            <td><code itemprop="sameAs">https://orcid.org/0000-0003-3562-3593</code></td>
          </tr>
        </table>
      </div>
    </td>
  </tr>

  <tr>
    <td>license</td>
    <td>
      <div itemscope itemtype="http://schema.org/CreativeWork" itemprop="license">
        <table>
          <tr>
            <th>property</th>
            <th>value</th>
          </tr>
          <tr>
            <td>name</td>
            <td><code itemprop="name">CC BY 4.0</code></td>
          </tr>
          <tr>
            <td>url</td>
            <td><code itemprop="url">https://creativecommons.org/licenses/by/4.0/</code></td>
          </tr>
        </table>
      </div>
    </td>
  </tr>
</table>
</div>
