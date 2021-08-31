import spacy
import nltk
spacy_nlp = None

def initialize_models():
    global spacy_nlp
    # load spacy
    spacy_nlp = spacy.load("en_core_web_sm")
    nltk.download('stopwords')