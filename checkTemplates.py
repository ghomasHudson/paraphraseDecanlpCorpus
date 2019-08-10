'''Quick sanity check on the templates'''

import os
import csv
import logging
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('templates',type=str,help='Template input dir')
args = parser.parse_args()

logger = logging.getLogger(__name__)

requiredSubstrings = {
    "translation":["{source}", "{target}"],
    "sentiment": ["positive","negative"],
    "schema": ["{mainQuestion}","{choice1}","{choice2}"],
    "multinli":["{sent}","contradiction","entailment","neutral"],
    "wikisql":["English"],
}

# Check for orig prompts
orig_prompts = {
    "multinli": 'Hypothesis: "{sent}" -- entailment, neutral, or contradiction?',
    "sentiment": 'Is this review negative or positive?',
    "translation": 'Translate from {source} to {target}.',
    "woz": 'What is the change in state?',
    "schema": '{mainQuestion} {choice1} or {choice2}?',
    "summarization": 'What is the summary?',
    "wikisql": 'What is the translation from English to SQL?'
    }
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


#Check for required strings
for task in requiredSubstrings.keys():
    for split in ["test","train"]:
        with open(os.path.join(args.templates,task+"."+split)) as f:
            for i,line in enumerate(f.readlines()):
                for substr in requiredSubstrings[task]:
                    if substr not in line:
                        logging.error("'"+substr + "' not in line "+str(i+1)+":'"+line[:-1] +"' of "+task+"."+split)
                if levenshteinDistance(line.lower(),orig_prompts[task].lower()) < 5:
                    logging.error("'"+line[:-1]+ "' is a possible duplicate of the prompt (line "+str(i+1)+" of "+task+"."+split+")")


# Check for duplicates
for task in requiredSubstrings.keys():
    for split in ["test","train"]:
        with open(os.path.join(args.templates,task+"."+split)) as f:
            lines = list(f.readlines())
            for i in range(len(lines)):
                for j in range(i,len(lines)):
                    if i != j:
                        dist = levenshteinDistance(lines[i].lower(),lines[j].lower())
                        if dist == 0:
                            logging.error("'"+lines[i][:-1]+"' appears twice (lines "+str(i+1)+" and "+str(j+1)+")")
                        elif dist < 5:
                            logging.info("'"+lines[i][:-1]+"' is possibly duplicated (lines "+str(i+1)+" and "+str(j+1)+")")
