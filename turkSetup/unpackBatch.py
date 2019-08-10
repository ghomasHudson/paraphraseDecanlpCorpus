"""Take Amazon turk batch and save to text files"""
import csv
import argparse
import re
import os
from pathlib import Path

# Input Args
parser = argparse.ArgumentParser(description='Convert Amazon turk batches to txt files')
parser.add_argument('inputFile',type=argparse.FileType('r'))
parser.add_argument('--include-rejected',action='store_true')
args = parser.parse_args()

formattedOutputs = {}

# Merge all answers for the same task
csvreader = csv.DictReader(args.inputFile)
for row in csvreader:
    if args.include_rejected or row["AssignmentStatus"] != "Rejected":
        prompt = row["Input.prompt"]
        for k in row:
            if "Answer.para" in k:
                formattedOutputs[prompt] = formattedOutputs.get(prompt,[]) + [row[k]]

# Output
dir_name = Path(args.inputFile.name).stem
os.mkdir(dir_name)

regex = re.compile('[^a-zA-Z_]')
for k in formattedOutputs:
    #strip stuff out of prompt for filename
    kFormatted = k.replace(" ","_").lower()
    kFormatted = regex.sub('',kFormatted)
    formattedOutputs[k] = [l+"\n" for l in formattedOutputs[k]]
    with open(os.path.join(dir_name,kFormatted+".txt"),'w') as f:
        f.writelines(formattedOutputs[k])
    
