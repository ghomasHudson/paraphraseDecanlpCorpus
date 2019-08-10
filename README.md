# paraphraseDecanlpCorpus
Paraphrases of the decanlp questions gathered from Amazon Mechanical Turk

## Usage
The `templates` folder contains the raw question paraphrases gathered from mechanical turk, one-per-line. These have already been split 70:30 into train/test sets.

To use these with decaNLP you need to modify the code to read extra arguments from jsonl files. The `Patches` folder contains modifications for the decaNLP code (tested with commit hash `1e9605f246b9e05199b28bde2a2093bc49feeeaa`)

To evaluate decaNLP on the paraphrase test set run:

`./evaluatePara.sh outputFolder/test`
(You can append any of decanlp's predict.py options too)

This will repeatedly run `python predict.py` specifying the correct metrics (you could also modify predict.py to include this logic)

To train on the paraphrase training set, specify the data path:

`python train.py --data outputFolder/train`...

## Recreating the data
To use the dataset with decaNLP, you first need to slightly modify the decanlp code to dump the task data as jsonl files.

Then run `makeCorpus.py` which will expand out the jsonl file for each task with the paraphrase questions. You'll end up with the following structure:

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

`makeTrain.sh` will randomly select a question for every datapoint in the training corpus.
