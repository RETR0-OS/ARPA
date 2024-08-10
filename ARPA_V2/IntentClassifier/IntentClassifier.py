import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import spacy
import warnings
import pickle

warnings.filterwarnings("ignore")
# Load SpaCy model
nlp = spacy.load("en_core_web_lg")
pipeline = None

# Define preprocessing function using SpaCy
def spacy_tokenizer(text):
    tokens = nlp(text)
    tokens = [token.lemma_.lower() for token in tokens if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def save_model():
    f = open("D:/ARPA/ARPA_V2/IntentClassifier/IntentClassifier.dat", "wb")
    pickle.dump(pipeline, f)
    #return pipeline

def train_model():
    # Load data from CSV
    global pipeline
    data = pd.read_csv("D:/ARPA/ARPA/IntentClassifiers/train_data.csv")

    # Assuming 'Prompt' is your feature column and 'Intent' is your target column
    x_train = data['Prompt'].values
    y_train = data['Intent'].values

    # Train-test split
    # Define pipeline with TF-IDF vectorizer and SVM classifier
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(tokenizer=spacy_tokenizer)),
        ('clf', SVC(kernel='linear'))
    ])

    # Fit pipeline on training data
    pipeline.fit(x_train, y_train)
    save_model()