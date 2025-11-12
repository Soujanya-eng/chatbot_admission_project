# File: main.py (Top section)

from flask import Flask, request, render_template
import nltk
# NEW IMPORTS: Directly import the required components
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn 
# You need to initialize the WordNet resource early
from nltk.corpus.util import LazyCorpusLoader

app = Flask(__name__) 

# --- Initialization & NLTK Setup (MODIFIED) ---

# Reinitialize WordNet to avoid the 'subdir' error
# This line often resolves the conflict by forcing the correct access method
wn = LazyCorpusLoader(
    'wordnet', nltk.corpus.WordNetCorpusReader, 
    ['NOUN', 'VERB', 'ADJ', 'ADV']
)

try:
    # Initialize the lemmatizer using the correctly set up resource
    lemmatizer = WordNetLemmatizer()
except LookupError:
    print("NLTK data (punkt, wordnet) not found. Please run the download command.")
    exit()

# The rest of your main.py code is UNCHANGED (chatbot_logic, ADMISSION_FACTS, etc.)

# --- KNOWLEDGE BASE (Pure Python Data Structure) ---
ADMISSION_FACTS = {
    "GREETING": "Hello! I am the PDA College Admission Assistant, how can i help you. Ask me about Courses, Eligibility, or Fees.",
    "BE_COURSES": "PDA College offers 11 B.E. programs, including Civil, Mechanical, EEE, ECE, CSE, AI & ML, and others.",
    "ELIGIBILITY_BE": "For the B.E. program, candidates need 10+2 with Physics, Math, and a science subject, achieving 45% aggregate (40% for reserved categories).",
    "FEES": "B.E. tuition ranges from ₹1.6 Lakh to ₹7.4 Lakh depending on the quota.",
    "CONTACT": "You can reach the Admissions Office directly at Ph: 08472 - 224360.",
    "DEFAULT": "I apologize, I can only assist with basic admission queries right now. Please try asking about Courses, Eligibility, or Fees."
}
KEYWORD_MAP = {
    'hello': 'GREETING', 'hi': 'GREETING', 'course': 'BE_COURSES', 
    'branch': 'BE_COURSES', 'be': 'BE_COURSES', 'fee': 'FEES', 
    'eligible': 'ELIGIBILITY_BE', 'criteria': 'ELIGIBILITY_BE', 
    'admission': 'ELIGIBILITY_BE', 'contact': 'CONTACT', 'phone': 'CONTACT'
}

# --- CHATBOT LOGIC FUNCTION (Pure Python NLP) ---
def chatbot_logic(query):
    query_lower = query.lower()
    tokens = word_tokenize(query_lower)
    # Lemmatization: Reduce words to their root form
    lemmas = [lemmatizer.lemmatize(word) for word in tokens]

    for lemma in lemmas:
        if lemma in KEYWORD_MAP:
            return ADMISSION_FACTS[KEYWORD_MAP[lemma]]
    
    return ADMISSION_FACTS['DEFAULT']

# --- FLASK ROUTE: Handles Page Load, Input, and Output ---
@app.route('/')
def index():
    # Retrieve chat query from URL parameters (due to HTML form submission)
    user_query = request.args.get('query', '') 
    
    # Initialize chat history
    history = [
        {"sender": "bot", "text": ADMISSION_FACTS['GREETING']}
    ]

    if user_query:
        # Add user query to history
        history.append({"sender": "user", "text": user_query})
        
        # Process the query using pure Python logic
        bot_response = chatbot_logic(user_query)
        
        # Add bot response to history
        history.append({"sender": "bot", "text": bot_response})

    # Render the template, passing the complete chat history to be displayed
    return render_template('index.html', chat_history=history)

# --- RUN THE SERVER ---
if __name__ == '__main__':
    print("Starting Pure Python Chatbot Server (No JavaScript).")
    app.run(debug=True, port=5000)