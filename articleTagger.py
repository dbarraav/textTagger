import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import time
import os
# Download NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')

parDirPath = os.path.dirname(os.path.abspath(__file__))
nltkDataPath = os.path.join(parDirPath, 'nltk_data')
nltk.data.path.append(nltkDataPath)

def extract_text_from_pdf(pdf_path, numPages):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ''
    # Extract text from the first 'numPages' pages
    for page_num in range(min(numPages, len(doc))):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_words = [word.lower() for word in word_tokens if word.isalpha() and word.lower() not in stop_words]
    return filtered_words

def get_top_keywords(words, num_keywords=10):
    word_freq = Counter(words)
    common_words = word_freq.most_common(num_keywords)
    return [word for word, freq in common_words]

def generate_tags(pdf_path, numPages, num_keywords=10):
    text = extract_text_from_pdf(pdf_path, numPages)
    filtered_words = preprocess_text(text)
    tags = get_top_keywords(filtered_words, num_keywords)
    return tags

numPages = 4
# Example usage
startTime = time.time()
pdf_path = '/mnt/d/OneDrive - Washington University in St. Louis/Research_PathakLab/scientificarticles/0824/PIIS0960982219316203.pdf'
tags = generate_tags(pdf_path, numPages)
stopTime = time.time()

print('It took {} seconds to find these tags'.format(stopTime - startTime))
print("Generated Tags:", tags)
