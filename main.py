from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# --- Initialization ---
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Initialize NLTK tools
lemmatizer = WordNetLemmatizer()

# --- 1. KNOWLEDGE BASE (Using specific PDA College details) ---
ADMISSION_FACTS = {
    "GREETING": "Hello! I am the PDA College Admission Assistant. I can help with information on **Courses, Eligibility, and Fees**. How can I assist you?",
    
    "BE_COURSES": "PDA College offers **11 B.E. programs** including Civil, Mechanical, EEE, ECE, CSE, AI & ML, Computer Science & Design, and more. Which stream interests you?",
    
    "PG_COURSES": "We offer 10 M.Tech programs like Structural Engineering, Thermal Power Engineering, and Computer Science & Engineering.",

    "ELIGIBILITY_BE": "For the B.E. program, candidates must have passed **10+2 with a minimum of 45% aggregate** (40% for reserved categories) in PCM. Admission is through **KCET/COMEDK UGET** scores.",
    
    "FEES": "Fees vary by course and quota. The total tuition fee for B.E. ranges from **₹1.6 Lakh to ₹7.4 Lakh**. Please check the official 'Fee Structure' link on the college website for the latest breakdown.",
    
    "CONTACT": "You can reach the Admissions Office directly at **Ph: 08472 - 224360** (9 AM to 5 PM).",

    "DEFAULT": "I apologize, I can only assist with admission queries right now. Try asking about **Courses, Eligibility, or Fees**."
}

# --- 2. KEYWORD MAPPING (Base forms for Lemmatizer) ---
KEYWORD_MAP = {
    'hello': 'GREETING', 'hi': 'GREETING', 'greet': 'GREETING',
    'course': 'BE_COURSES', 'branch': 'BE_COURSES', 'ug': 'BE_COURSES', 'be': 'BE_COURSES',
    'pg': 'PG_COURSES', 'm.tech': 'PG_COURSES',
    'fee': 'FEES', 'cost': 'FEES', 'money': 'FEES',
    'eligible': 'ELIGIBILITY_BE', 'criteria': 'ELIGIBILITY_BE', 'admission': 'ELIGIBILITY_BE', 
    'kcet': 'ELIGIBILITY_BE', 'comedk': 'ELIGIBILITY_BE',
    'contact': 'CONTACT', 'phone': 'CONTACT', 'call': 'CONTACT', 'email': 'CONTACT',
}

# --- 3. CHATBOT LOGIC FUNCTION ---
def chatbot_logic(query):
    query_lower = query.lower()
    
    # NLTK Processing: Tokenize and Lemmatize the query
    tokens = word_tokenize(query_lower)
    lemmas = [lemmatizer.lemmatize(word) for word in tokens]

    # Check for keywords in the lemmatized list
    for lemma in lemmas:
        if lemma in KEYWORD_MAP:
            fact_key = KEYWORD_MAP[lemma]
            # Handle specific priority for PG queries
            if fact_key == 'PG_COURSES' and 'ug' not in query_lower:
                return ADMISSION_FACTS['PG_COURSES']
            
            return ADMISSION_FACTS[fact_key]
    
    return ADMISSION_FACTS['DEFAULT']

# --- 4. FLASK API ENDPOINT ---
# NOTE: The route is clean and simple. The POST method is explicitly defined.
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = data.get('query', '')
    
    response_text = chatbot_logic(user_query)
    
    # Return the response as JSON
    return jsonify({'response': response_text})

# --- 5. RUN THE SERVER ---
if __name__ == '__main__':
    # Run Flask on port 5000
    print("Starting Flask server on http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)