# paraphraseDecanlpCorpus
Paraphrases of the decanlp questions gathered from Amazon Mechanical Turk

## Recreating the data
The `templates` folder contains the question paraphrases gathered from mechanical turk, one-per-line. These have already been split 70:30 into train/test sets.

To use the dataset with decaNLP, you first need to slightly modify the decaNLP code to dump the task data as jsonl files. First apply the patch:
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

## Annotated data

`annotated.json` contains paraphrase annotations for each of the examples in the test set.

## Trained T5 checkpoints

Checkpoints for the T5 checkpoints to evaluate this corpus are [here](https://drive.google.com/drive/folders/1RbIrGzfj0LUQ_qGCEVsyUyIf3y3pB3y6?usp=sharing)
