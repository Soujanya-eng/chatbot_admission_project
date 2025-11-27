from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random
from typing import Dict, List, Callable
from fuzzywuzzy import fuzz

# --- CONFIGURATION ---
FUZZY_THRESHOLD = 75 

# --- 1. COLLEGE KNOWLEDGE BASE (Data Storage) ---

COLLEGE_DATA: Dict[str, any] = {
    "name": "P D A ENGINEERING COLLEGE KALABURAGI",
    "official_website": "https://www.pdacek.ac.in/",
    "address": "Street: Aiwan-E-Shahi Area,City: Kalaburagi (formerly Gulbarga),State: Karnataka,PIN Code: 585102 ",
    "photo_query": "https://www.collegebatch.com/2696-pda-college-of-engineering-campus-tour-gulbarga",
    "admission_mode": {
        "text": "Admission to PDA College of Engineering, Kalaburagi is based on performance in entrance exams like the CET (Common Entrance Test) for undergraduate programs and the GATE (Graduate Aptitude Test in Engineering) for postgraduate programs. The college conducts its own entrance exams and interviews for some programs. Applicants must also meet the specific academic requirements for their chosen program, and the college may also consider factors such as the results of the CET and other entrance exams for admission. ",
        "link": "https://www.tech-uni.edu.in/admission-guide"
    },
    "fees": {
        "BTech": "₹1,50,000 per year, excluding hostel fees. Scholarships are available. depends on Aided ,Unaided,and Payment seats",
        "MTech": "₹1,80,000 per year. Check the finance portal for payment dates.depends on Aided ,Unaided,and Payment seats,kindly visit our college to know more information ",
        "link": "https://www.tech-uni.edu.in/fee-structure"
    },
    "placements": {
        "average": "Our average placement package for B.Tech CSE graduates is **8.5 LPA** (Lakhs Per Annum).",
        "companies": "Top recruiters include TCS, Infosys, Wipro, and various startups.",
        "report_link": "https://www.tech-uni.edu.in/placement-report"
    },
    "courses": {
        "departments": ["Computer Science (CSE)", "Electronics and Communication (ECE)", "Mechanical Engineering (ME)", "Electrical&Electronics(EEE)","Industrial&Production(IP)","Electronics&Instrumentation(EI)","Information Science&Engineering(IS),Cement and Ceramics Technology(CCT)",],
        "software": ["Data Science", "Artificial Intelligence", "Cloud Computing", "Cyber Security"],
        "hardware": ["VLSI Design", "Robotics and Automation", "Embedded Systems"],
        "full_list_link": "https://www.tech-uni.edu.in/course-catalogue"
    }
}

# --- 2. INTENT & PATTERN MAPPING ---
INTENT_PATTERNS: Dict[str, List[str]] = {
    "greet": ['hi', 'hello', 'hey'],
    "admission_mode": ['admission mode', 'how to apply', 'entry procedure', 'admission'],
    "fees": ['fee structure', 'how much', 'fees', 'cost'],
    "departments": ['departments', 'courses', 'programs'],
    "software": ['software courses', 'coding',"high demanding",],
    "hardware": ['hardware courses', 'electronics'],
    "address": ['address', 'location', 'where'],
    "website": ['official website', 'site link', 'website'],
    "photo": ['college photo', 'pics', 'image'],
    "placement_details": ['placement details', 'average salary', 'top companies', 'jobs'],
    "goodbye": ['bye', 'exit', 'thank you', 'thanks']
}

# --- 3. RESPONSE GENERATION FUNCTIONS (Feature Handlers) ---
# ... (Functions handle_admission_mode, handle_fees, etc. remain the same) ...

def handle_admission_mode() -> str:
    data = COLLEGE_DATA["admission_mode"]
    return f"**Admission Mode:** {data['text']} For the full step-by-step guide, visit: {data['link']}"

def handle_fees() -> str:
    msg = f"**Fee Structure Overview:**\n* B.Tech: {COLLEGE_DATA['fees']['BTech']}\n* MTech: {COLLEGE_DATA['fees']['MTech']}\n"
    msg += f"You can view the complete, detailed fee table here: {COLLEGE_DATA['fees']['link']}"
    return msg

def handle_departments() -> str:
    depts = ', '.join(COLLEGE_DATA["courses"]["departments"])
    return f"We currently offer courses across these major departments: **{depts}**."

def handle_software_courses() -> str:
    sw_courses = ', '.join(COLLEGE_DATA["courses"]["software"])
    link = COLLEGE_DATA["courses"]["full_list_link"]
    return f"**Specialized Software Courses:** {sw_courses}. View the full catalogue: {link}"

def handle_hardware_courses() -> str:
    hw_courses = ', '.join(COLLEGE_DATA["courses"]["hardware"])
    link = COLLEGE_DATA["courses"]["full_list_link"]
    return f"**Specialized Hardware Courses:** {hw_courses}. View the full catalogue: {link}"

def handle_address() -> str:
    address = COLLEGE_DATA["address"]
    map_link = f"https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')}"
    # Using a placeholder image tag
    return f"Here is the college **address**: **{address}**." + " [Image of the college location on a map] \n\n" + f"Click here for directions: {map_link}"

def handle_website_link() -> str:
    return f"The **Official Website** is: {COLLEGE_DATA['official_website']}"

def handle_college_photo() -> str:
    return f"Here is a photo of the main campus: {COLLEGE_DATA['photo_query']}"

def handle_placement_details() -> str:
    avg = COLLEGE_DATA["placements"]["average"]
    companies = COLLEGE_DATA["placements"]["companies"]
    link = COLLEGE_DATA["placements"]["report_link"]
    msg = f"**Placement Highlights:**\n* Average Package: {avg}\n* Top Recruiters: {companies}\n"
    msg += f"View the detailed placement report here: {link}"
    return msg

INTENT_HANDLERS: Dict[str, Callable[[], str]] = {
    "admission_mode": handle_admission_mode,
    "fees": handle_fees,
    "departments": handle_departments,
    "software": handle_software_courses,
    "hardware": handle_hardware_courses,
    "address": handle_address,
    "website": handle_website_link,
    "photo": handle_college_photo,
    "placement_details": handle_placement_details,
}

# --- 4. CORE CHATBOT LOGIC (Intent Recognition with Fuzzy Matching) ---

def get_bot_response(user_input: str) -> str:
    cleaned_input = re.sub(r'[^\w\s]', ' ', user_input).lower()
    words = cleaned_input.split()
    
    # Check for greetings and goodbyes
    for intent in ["greet", "goodbye"]:
        for pattern in INTENT_PATTERNS[intent]:
            if pattern in cleaned_input:
                if intent == "greet":
                    return random.choice(["Hello! Welcome to PDA ENGINEERING COLLEGE CHATBOT.I can provide details on admission, courses, fees, and more.", "Hi there! What can I help you find today?"])
                else:
                    return random.choice(["Thank you for chatting. Goodbye!", "Feel free to reach out if you have any other questions!,if you want reach out through call then kindly call this number 1234-5678-9173"])

    # Fuzzy Matching for Feature Intents
    best_match_intent = None
    max_score = 0
    
    for intent, patterns in INTENT_PATTERNS.items():
        if intent in INTENT_HANDLERS:
            for user_word in words:
                for target_pattern in patterns:
                    score = fuzz.ratio(user_word, target_pattern)
                    partial_score = fuzz.partial_ratio(cleaned_input, target_pattern)
                    
                    current_score = max(score, partial_score)
                    
                    if current_score > max_score and current_score >= FUZZY_THRESHOLD:
                        max_score = current_score
                        best_match_intent = intent

    if best_match_intent and best_match_intent in INTENT_HANDLERS:
        return INTENT_HANDLERS[best_match_intent]()
        
    # Fallback
    return "I'm sorry, I don't have enough information on that. I can assist with **admission mode**, **courses (software/hardware)**, **fees**, **address**, **placements**, and the **website link**."


# --- 5. FLASK SERVER IMPLEMENTATION ---
app = Flask(__name__)
CORS(app) 

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'Please provide a message.'}), 400

        bot_response = get_bot_response(user_message)
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'response': 'An internal server error occurred. Check the server terminal.'}), 500

if __name__ == '__main__':
    print("🎓 Starting Flask server for chatbot backend on http://127.0.0.1:5000/ ...")
    app.run(debug=True, port=5000)