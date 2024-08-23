import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import Counter
from nltk.util import ngrams
import os
import re
import argparse

parDirPath = os.path.dirname(os.path.abspath(__file__))
nltkDataPath = os.path.join(parDirPath, 'nltk_data')
nltk.data.path.append(nltkDataPath)

ignoredWordsFilePath = os.path.join(parDirPath, 'ignoredWords.txt')

# Stopwords that should be ignored unless part of a phrase
special_stopwords = {'cell', 'cells', 'cellular'}

def extract_text_from_pdf(pdf_path, num_pages=3):
    doc = fitz.open(pdf_path)
    text = ''
    for page_num in range(min(num_pages, len(doc))):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

def read_stopwords_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()  # Read lines and split them into words
    return set(words)

def preprocess_text(text):
    stopWords = read_stopwords_from_file(ignoredWordsFilePath)
    custom_stopwords = set(stopwords.words('english')).union(stopWords) - special_stopwords

    # Tokenize the text and allow hyphenated words
    word_tokens = re.findall(r'\b\w+(?:-\w+)?\b', text.lower())  # This regex captures words and hyphenated words
    filtered_words = [word for word in word_tokens if word.isalpha() and word not in custom_stopwords]
    return filtered_words

def filter_nouns_adjectives(words):
    pos_tags = pos_tag(words)

    greek_letters = {'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 
                     'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 
                     'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'}


    filtered_words = []
    for word, pos in pos_tags:
        # Exclude locations, single letters, and Greek letters or symbols
        if pos.startswith('NN') or pos.startswith('JJ'):  # Check if word is a noun or adjective
            if len(word) > 2 and word not in greek_letters:  # Exclude single letters and Greek letters
                if pos != 'NNP':  # Exclude proper nouns (locations)
                    filtered_words.append(word)
    
    return filtered_words

def get_top_keywords_and_phrases(words, total_tags=20, word_ratio=0.5):
    num_keywords = int(total_tags * word_ratio)
    num_phrases = total_tags - num_keywords
    
    # Single words
    word_freq = Counter(words)
    common_words = word_freq.most_common(num_keywords)
    
    # Phrases (bigrams and trigrams)
    bigrams = ngrams(words, 2)
    trigrams = ngrams(words, 3)
    phrases = list(bigrams) + list(trigrams)
    phrase_freq = Counter(phrases)
    common_phrases = phrase_freq.most_common(num_phrases)
    
    # Combine single words with phrases
    # tags = [word for word, freq in common_words] + [' '.join(phrase) for phrase, freq in common_phrases]
    tags = [(word, freq) for word, freq in common_words] + [(' '.join(phrase), freq) for phrase, freq in common_phrases]

    # Sort tags by frequency in ascending order
    tags_sorted_by_freq = sorted(tags, key=lambda x: x[1])
    return tags_sorted_by_freq

def generate_tags(pdf_path, num_pages=3, total_tags=20, word_ratio=0.5):
    text = extract_text_from_pdf(pdf_path, num_pages)
    filtered_words = preprocess_text(text)
    filtered_words = filter_nouns_adjectives(filtered_words)

    # First attempt:
    # tags = get_top_keywords_and_phrases(filtered_words, total_tags, word_ratio)
    
    # # Print tags sorted by frequency
    # for tag, freq in tags:
    #     print(f"Tag: {tag}, Frequency: {freq}")
    
    # return [tag for tag, freq in tags]  # Return just the tags

    # Second attempt:
    # Handling special stopwords in phrases
    phrases = list(ngrams(filtered_words, 2)) + list(ngrams(filtered_words, 3))
    final_words = [word for word in filtered_words if word not in special_stopwords]
    
    # Include special stopwords if they appear in phrases
    for phrase in phrases:
        if any(word in special_stopwords for word in phrase):
            final_words.append(' '.join(phrase))
    tags_with_freq = get_top_keywords_and_phrases(final_words, total_tags, word_ratio)
    
    # # Print tags sorted by frequency
    # for tag, freq in tags_with_freq:
    #     print(f"Tag: {tag}, Frequency: {freq}")
    
    return tags_with_freq  # Return tags with their frequencies

# parser = argparse.ArgumentParser()
# parser.add_argument("inputPath", type=str, help="convert pdf in input directory to bibtex file")

# args = parser.parse_args()
# pdfPath= args.inputPath 

# Example usage
# pdfPath = '/mnt/d/OneDrive - Washington University in St. Louis/Research_PathakLab/scientificarticles/0824/PIIS0960982219316203.pdf'
# tags = generate_tags(pdfPath, total_tags=15, word_ratio=0.80)  # 20 tags, 60% single words, 40% phrases
# print("Generated Tags:", tags)
# Print tags sorted by frequency
# for tag, freq in tags:
#     print(f"Tag: {tag}, Frequency: {freq}")