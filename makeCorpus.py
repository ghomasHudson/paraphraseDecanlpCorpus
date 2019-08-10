#!/bin/python3
'''Expands data set with paraphrases'''

import sys
import json
import os
import csv
from tqdm import tqdm
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--data', type=str,required=True, help='DecaNLP data dir')
parser.add_argument('--output', type=str,required=True, help='Paraphrase output dir')
parser.add_argument('--templates',type=str,default="templates",help='Template input dir')
args = parser.parse_args()

if  os.path.exists(args.output):
    raise Exception("Output dir already exists")
os.makedirs(args.output)
os.makedirs(os.path.join(args.output,"train"))
os.makedirs(os.path.join(args.output,"test"))

import mmap
def get_num_lines(file_path):
    '''Count the number of lines in a file'''
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines

def loadDataFromPath(path):
    existingData = open(os.path.join(args.data,path),'r').readlines()
    outputLines = []
    for line in existingData:
        line = preprocessLine(line)
        outputLines.append(line)
    return outputLines

def preprocessLine(line):
    '''Fix data line object'''
    line = json.loads(line.rstrip())
    for key in ["question","context","answer"]:
        if key+"Raw" in line.keys():
            line[key] = line[key+"Raw"]
            del line[key+"Raw"]
    return line


def preprocessTemplates(templateLines):
    '''Remove comments and blank lines in template lists'''
    import re
    regex = re.compile(r"(?m) *#.*$", re.IGNORECASE)
    templates = []
    for line in templateLines:
        line = line.replace("\n","")
        lines = line.rstrip()
        if line != "":
            templates.append(line)
    return templates


def simpleReplacementLine(line,paraphrases):
    '''Simply expands line with the paraphrases in paraphrasesFile.
        Returns lists for each version'''
    outputLines = []
    for i,paraphrase in enumerate(paraphrases):
        newLine = line.copy()
        newLine["question"] = paraphrase #overwrite the question
        outputLines.append(json.dumps(newLine,ensure_ascii=False))
    return outputLines


def simpleReplacement(existingData,paraphrases):
    '''Simply expands existingDataFile with the paraphrases in paraphrasesFile.
        Returns lists for each version'''

    #paraphrases = [l.rstrip() for l in paraphrases] #remove trailing \n

    #read in existing data
    outputLines = []
    for i,paraphrase in enumerate(paraphrases):
        outputLines.append([])
        for line in existingData:
            newLine = line.copy()
            newLine["question"] = paraphrase #overwrite the question
            outputLines[-1].append(json.dumps(newLine,ensure_ascii=False))
    return outputLines


def writeLine(datasets,output_dir,name,output_file_name):
    '''Saves each nested list of datasets into name0,name1 etc...'''
    for i in range(len(datasets)):
        dataName = name+str(i)
        task_dir = os.path.join(output_dir, dataName)
        if not os.path.exists(task_dir):
            os.mkdir(task_dir)

        with open(os.path.join(output_dir,dataName,output_file_name),'a') as f3:
            f3.write(datasets[i]+"\n")
"""
def writeLine(datasets,output_dir,name,output_file_name):
    '''Saves each nested list of datasets into name0,name1 etc...'''
    for i in range(len(datasets)):
        dataName = name+str(i)
        task_dir = os.path.join(output_dir, dataName)
        if not os.path.exists(task_dir):
            os.mkdir(task_dir)
        with open(os.path.join(output_dir,dataName,output_file_name),'w') as f3:
            f3.write("\n".join(datasets[i]))
"""

def standardReplace(original_data_file, template_file,output_dir, output_task_name,output_file_name):
    '''loads data, preprocesses, replaces question, writes output'''
    templates = preprocessTemplates(open(template_file,'r').readlines())
    with open(original_data_file,'r') as f:
        for line in tqdm(f,total=get_num_lines(original_data_file)):
            line = preprocessLine(line)
            lines = simpleReplacementLine(line,templates)
            writeLine(lines,output_dir,output_task_name,output_file_name)

#*************
#multiNLI
def multinli(original_data_file, template_file,output_dir, output_task_name,output_file_name):
    templates = preprocessTemplates(open(template_file,'r').readlines())
    with open(original_data_file,'r') as f:
        for line in tqdm(f,total=get_num_lines(original_data_file)):
            line = preprocessLine(line)
            hypothesis = line["question"][13:-43]
            lines = simpleReplacementLine(line,templates)
            outputL = []
            for l in lines:
                l = json.loads(l)
                l["question"] = l["question"].format(sent=hypothesis)
                outputL.append(json.dumps(l,ensure_ascii=False))
            writeLine(outputL,output_dir,output_task_name,output_file_name)


#*************
#translation
#as before but replace names of langs
def translation(original_data_file, template_file,output_dir, output_task_name,output_file_name):
    templates = preprocessTemplates(open(template_file,'r').readlines())

    # Replace source and target with English and German
    source = "English"
    target = "German"
    for i in tqdm(range(len(templates))):
        templates[i] = templates[i].format(source="English", target="German").rstrip()


    with open(original_data_file,'r') as f:
        for line in tqdm(f,total=get_num_lines(original_data_file)):
            line = preprocessLine(line)
            lines = simpleReplacementLine(line,templates)
            writeLine(lines,output_dir,output_task_name,output_file_name)


#*************
#schema
def schema(original_data_file, template_file,output_dir, output_task_name,output_file_name):
    templates = preprocessTemplates(open(template_file,'r').readlines())
    with open(original_data_file,'r') as f:
        for line in tqdm(f,total=get_num_lines(original_data_file)):
            line = preprocessLine(line)
            rSplit = line["question"].split("?")
            choiceSplit = rSplit[1].strip().split(" or ")
            lines = simpleReplacementLine(line,templates)
            outputL = []
            for l in lines:
                l = json.loads(l)
                l["question"] = l["question"].format(mainQuestion=rSplit[0]+"?",choice1=choiceSplit[0],choice2=choiceSplit[1])
                outputL.append(json.dumps(l,ensure_ascii=False))
            writeLine(outputL,output_dir,output_task_name,output_file_name)


# *****************************************************************
# Main code

task_map = [
    {
        "templateName": "schema",
        "train": "schema/.cache/train.jsonl/20000000.jsonl",
        "test" : "schema/.cache/validation.jsonl/None.jsonl",
        "function": schema
    },
    {
        "templateName": "translation",
        "train": "iwslt/en-de/.cache/train.en-de/20000000.jsonl",
        "test" : "iwslt/en-de/.cache/IWSLT16.TED.tst2013.en-de/20000000.jsonl",
        "function": translation
    },
    {
        "templateName": "multinli",
        "train": "multinli/multinli_1.0/.cache/train.jsonl/20000000/multinli.in.out.jsonl",
        "test" : "multinli/multinli_1.0/.cache/validation.jsonl/None/multinli.in.out.jsonl",
        "function": multinli
    },
    {
        "templateName": "sentiment",
        "train": "sst/.cache/train_binary_sent.csv/20000000.jsonl",
        "test" : "sst/.cache/dev_binary_sent.csv/None.jsonl",
        "function": standardReplace
    },
    {
        "templateName": "wikisql",
        "train": "wikisql/data/.cache/query_as_context/train.jsonl/20000000.jsonl",
        "test" : "wikisql/data/.cache/query_as_context/dev.jsonl/None.jsonl",
        "function": standardReplace
    },
    {
        "templateName": "woz",
        "train": "woz/.cache/train.jsonl/20000000/woz.en.jsonl",
        "test" : "woz/.cache/validate.jsonl/None/woz.en.jsonl",
        "function": standardReplace
    },
    {
        "templateName": "summarization",
        "train": "cnn/cnn/.cache/training.jsonl/20000000.jsonl",
        "test" : "cnn/cnn/.cache/validation.jsonl/None.jsonl",
        "function": standardReplace
    },
    {
        "templateName": "summarization",
        "train": "dailymail/dailymail/.cache/training.jsonl/20000000.jsonl",
        "test" : "dailymail/dailymail/.cache/validation.jsonl/None.jsonl",
        "function": standardReplace
    },
]

split_to_filename = {
    "train": "train.jsonl",
    "test": "val.jsonl"
}

if __name__ == "__main__":
    for task in task_map:
        for split in split_to_filename:
            task_name = task[split].split("/",1)[0].upper()
            print(task_name, "-", split)
            task["function"](os.path.join(args.data,task[split]), os.path.join(args.templates,task["templateName"]+"."+split), os.path.join(args.output,split),task_name,split_to_filename[split])

