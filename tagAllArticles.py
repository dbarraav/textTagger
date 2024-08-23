import articleTagger4
import os
import re
import argparse
import time
import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import Counter
from nltk.util import ngrams


parser = argparse.ArgumentParser()
parser.add_argument("mainDir", type=str, help="convert pdf in input directory to bibtex file")

args = parser.parse_args()
mainDir= args.mainDir 

subdirectories = [os.path.join(mainDir, subdir) for subdir in os.listdir(mainDir) 
                  if os.path.isdir(os.path.join(mainDir, subdir))]

# print(subdirectories)

tagFileName = 'tags.txt'

fileStartTime = time.time()
startTime = time.time()
for subDir in subdirectories:
    files = os.listdir(subDir)
    # file_paths = [os.path.join(subDir, file) for file in files if os.path.isfile(os.path.join(subDir, file))]

    fileNames = [file for file in files if os.path.isfile(os.path.join(subDir, file))]
    # print(file_paths)
    tagsFilePath = os.path.join(subDir, tagFileName)
    startTime = time.time()
    
    with open(tagsFilePath, 'w') as f:
        for fileName in fileNames:
            filePath = os.path.join(subDir, fileName)
            if 'pdf' in filePath:
                tags = articleTagger4.generate_tags(filePath, total_tags=15, word_ratio=1.0) 

                # Format the tags with their frequencies
                tags_formatted = [f'{tag}' for tag, freq in tags]
            

                # Write the filename and tags to the output file
                f.write(f'{fileName}: {", ".join(tags_formatted)}\n')
    
    stopTime = time.time()

    totalTime = stopTime - startTime
    print(f'It took {totalTime} seconds to tag articles in this subdirectory')

fileStopTime = time.time()
fileTotalTime = fileStopTime - fileStartTime
print(f'It took {fileTotalTime} seconds to tag articles in this subdirectory')
