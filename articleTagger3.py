import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import Counter
from nltk.util import ngrams
import os

parDirPath = os.path.dirname(os.path.abspath(__file__))
nltkDataPath = os.path.join(parDirPath, 'nltk_data')
nltk.data.path.append(nltkDataPath)

def extract_text_from_pdf(pdf_path, num_pages=3):
    doc = fitz.open(pdf_path)
    text = ''
    for page_num in range(min(num_pages, len(doc))):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

def preprocess_text(text):
    custom_stopwords = set(stopwords.words('english')).union({'figure', 'pressure', 'activity'})
    word_tokens = word_tokenize(text)
    filtered_words = [word.lower() for word in word_tokens if word.isalpha() and word.lower() not in custom_stopwords]
    return filtered_words

def filter_nouns_adjectives(words):
    pos_tags = pos_tag(words)
    filtered_words = [word for word, pos in pos_tags if pos.startswith('NN') or pos.startswith('JJ')]
    return filtered_words

def get_top_keywords_and_phrases(words, num_keywords=10, num_phrases=5):
    word_freq = Counter(words)
    common_words = word_freq.most_common(num_keywords)
    
    bigrams = ngrams(words, 2)
    trigrams = ngrams(words, 3)
    phrases = list(bigrams) + list(trigrams)
    phrase_freq = Counter(phrases)
    common_phrases = phrase_freq.most_common(num_phrases)
    
    # Combine single words with phrases
    tags = [word for word, freq in common_words] + [' '.join(phrase) for phrase, freq in common_phrases]
    return tags

def generate_tags(pdf_path, num_pages=3, num_keywords=5, num_phrases=5):
    text = extract_text_from_pdf(pdf_path, num_pages)
    filtered_words = preprocess_text(text)
    filtered_words = filter_nouns_adjectives(filtered_words)
    tags = get_top_keywords_and_phrases(filtered_words, num_keywords, num_phrases)
    return tags


# Example usage
pdf_path = '/mnt/d/OneDrive - Washington University in St. Louis/Research_PathakLab/scientificarticles/0824/PIIS0960982219316203.pdf'
tags = generate_tags(pdf_path)
print("Generated Tags:", tags)
