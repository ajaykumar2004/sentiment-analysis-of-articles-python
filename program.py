import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import syllapy
from datetime import datetime
# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load data
articles_df = pd.read_excel('Input.xlsx')
# articles_df = pd.read_excel('onelink.xlsx')
with open('MasterDictionary/positive-words.txt', 'r') as f:
    positive_words = set(f.read().split())
with open('MasterDictionary/negative-words.txt', 'r') as f:
    negative_words = set(f.read().split())
# with open('StopWords/StopWords_DatesandNumbers.txt', 'r') as f:
#     stop_words = set(f.read().split())

print("Done1")
def stopwords(file_path):
    with open(file_path, 'r') as f:
        stop_words = set(f.read().split())
    return stop_words

# Initialize an empty set for all stop words
stop_words = set()

# Update the set with stop words from each file
stop_words.update(stopwords("StopWords/StopWords_Auditor.txt"))
stop_words.update(stopwords("StopWords/StopWords_Currencies.txt"))
stop_words.update(stopwords("StopWords/StopWords_DatesandNumbers.txt"))
stop_words.update(stopwords("StopWords/StopWords_Generic.txt"))
stop_words.update(stopwords("StopWords/StopWords_GenericLong.txt"))
stop_words.update(stopwords("StopWords/StopWords_Geographic.txt"))
stop_words.update(stopwords("StopWords/StopWords_Names.txt"))

print(len(stop_words))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', '', text)
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    return words

# Function to calculate metrics
def calculate_metrics(text):
    words = preprocess(text)
    word_count = len(words)
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / word_count

    sentences = sent_tokenize(text)
    avg_sentence_length = word_count / len(sentences)
    
    complex_words = [word for word in words if syllapy.count(word) > 2]
    complex_word_count = len(complex_words)
    percentage_complex_words = complex_word_count / word_count * 100

    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    personal_pronouns = len([word for word in words if re.match(r'\b(I|we|my|ours|us)\b', word)])

    avg_word_length = sum(len(word) for word in words) / word_count
    syllables_per_word = sum(syllapy.count(word) for word in words) / word_count

    return {
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score,
        'Avg Sentence Length': avg_sentence_length,
        'Percentage of Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Avg Number of Words per Sentence': avg_sentence_length,
        'Complex Word Count': complex_word_count,
        'Word Count': word_count,
        'Syllables per Word': syllables_per_word,
        'Personal Pronouns': personal_pronouns,
        'Avg Word Length': avg_word_length,
    }

# Scrape articles and calculate metrics
results = []
for link in articles_df['URL']:
    print(link)
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = ' '.join(p.get_text() for p in soup.find_all('p'))
        if article_text:
            metrics = calculate_metrics(article_text)
            metrics['Link'] = link
            results.append(metrics)
        else:
            print(f"No text found for {link}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {link}: {e}")
    except Exception as e:
        print(f"Error processing {link}: {e}")

# Convert results to DataFrame
results_df = pd.DataFrame(results)
results_df.to_excel('results.xlsx', index=False)