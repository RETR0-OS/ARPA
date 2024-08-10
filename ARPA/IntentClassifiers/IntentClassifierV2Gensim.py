import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression
import spacy
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load spacy model
nlp = spacy.load("en_core_web_lg")

# Intent mapper
intent_mapper = {"introduce_yourself": 0, "web_search": 1, "wiki_search": 2, "exit": 3}

# Preprocess function
def preprocess(text):
    doc = nlp(text)
    processed_data = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(processed_data)

# Load data
data = pd.read_csv("D:/ARPA/ARPA/IntentClassifiers/train_data.csv")

# Preprocess and map intents
data["clean_text"] = data["Prompt"].apply(preprocess)
data["Intent"] = data["Intent"].map(intent_mapper)

# Split data
x_train, x_test, y_train, y_test = train_test_split(data["clean_text"], data["Intent"], test_size=0.1, random_state=50, stratify=data["Intent"])

print(y_train.value_counts())
print(y_test.value_counts())

# Tagging the training data
tagged_train_data = [TaggedDocument(words=word_tokenize(doc), tags=[str(i)]) for i, doc in enumerate(x_train)]

# Train Doc2Vec model
doc2vec_model = Doc2Vec(vector_size=300, window=5, min_count=1, workers=4, epochs=20, dm=1)
doc2vec_model.build_vocab(tagged_train_data)
doc2vec_model.train(tagged_train_data, total_examples=doc2vec_model.corpus_count, epochs=doc2vec_model.epochs)

# Create document vectors
train_vectors = [doc2vec_model.dv[str(i)] for i in range(len(x_train))]
test_vectors = [doc2vec_model.infer_vector(word_tokenize(doc)) for doc in x_test]

# Train classifier
classifier = LogisticRegression(max_iter=1000)
classifier.fit(train_vectors, y_train)

# Predict and evaluate
predictions = classifier.predict(test_vectors)
print(classification_report(y_test, predictions, zero_division=0))
