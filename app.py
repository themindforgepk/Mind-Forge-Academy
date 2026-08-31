import streamlit as st
import google.generativeai as genai
import json
import time
import streamlit.components.v1 as components

# ==========================================
# 🛑 SETTINGS 🛑
# ==========================================
MERI_API_KEY = st.secrets["MERI_API_KEY"]
MERA_MODEL = "gemini-3.1-flash-lite"  
# ==========================================

genai.configure(api_key=MERI_API_KEY)
st.set_page_config(page_title="Mind Forge Academy", page_icon="🎓", layout="wide")
# === HIDE STREAMLIT MENU & FOOTER ===
hide_menu_style = """
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)
# === VIP AESTHETIC DESIGN ===
st.set_page_config(page_title="Mind Forge Academy", page_icon="🎓", layout="wide")

# === VIP AESTHETIC DESIGN ===
# (Yahan pehle se jo aesthetic code likha hai, uske bilkul neechay yeh naya Background code paste kar dein):

page_bg_img = '''
<style>
.stApp {
    background-image: linear-gradient(rgba(15, 20, 30, 0.8), rgba(15, 20, 30, 0.8)), url("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=2000&q=80");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
modern_design = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@700&display=swap');

html, body, [class*="css"], h1, h2, h3, h4, h5, h6, p, div, span, button, input, select, textarea {
    font-family: 'Poppins', sans-serif !important;
}
.urdu-text {
    font-family: 'Noto Nastaliq Urdu', serif !important;
    text-align: right;
    direction: rtl;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #e0e0e0;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
button[data-baseweb="tab"] {
    color: white !important;
    font-weight: 600 !important;
    font-size: 18px !important;
}
div.stButton > button:first-child {
    background: linear-gradient(90deg, #1CB5E0 0%, #000851 100%);
    color: white;
    border-radius: 8px;
    border: none;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    font-size: 16px !important;
    padding: 10px 24px;
    font-weight: 600;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 6px 20px rgba(28, 181, 224, 0.6);
}
div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.08);
    padding: 12px 15px;
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid transparent;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}
div[role="radiogroup"] > label:hover {
    background: rgba(28, 181, 224, 0.15);
    border: 1px solid #1CB5E0;
    transform: translateX(5px);
}
</style>
"""
st.markdown(modern_design, unsafe_allow_html=True)

# === LOGO AUR TITLE ===
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=90) 
with col_title:
    st.title("Mind Forge Academy")
    st.markdown("##### Premium Exam Preparation & Typing Engine")
st.write("---")

tab1, tab2 = st.tabs(["📝 AI MCQ Quiz", "⌨️ Typing Speed Test"])

# ==========================================
# TAB 1: MCQ QUIZ LOGIC (SMART EXAMINER)
# ==========================================
with tab1:
    
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

    dept_post_map = {
        "Ministry of Defence (MOD / GHQ)": ["LDC (BPS-11)", "UDC (BPS-13)", "Assistant (BPS-15)", "Data Entry Operator", "Naib Qasid (BPS-01)"],
        "Airport Security Force (ASF)": ["Corporal (BPS-07)", "ASI (BPS-11)", "Assistant (BPS-15)", "LDC (BPS-11)", "UDC (BPS-13)"],
        "Federal Investigation Agency (FIA)": ["Constable (BPS-05)", "ASI (BPS-09)", "Sub-Inspector (BPS-14)", "Inspector (BPS-16)", "Assistant Director"],
        "Police (Punjab / Islamabad / NHMP)": ["Constable (BPS-07)", "Head Constable (BPS-09)", "ASI (BPS-11)", "Sub-Inspector (BPS-14)", "Inspector (BPS-16)"],
        "Auqaf & Religious Affairs": ["Khateeb (BPS-16)", "Imam / Moazzin", "Manager Auqaf"],
        "Punjab Land Records Authority (PLRA)": ["Service Center Official - SCO (BPS-14)", "Land Record Officer - LRO (BPS-16)", "Assistant Director"],
        "Irrigation Department": ["Canal Patwari", "Zilladar (BPS-14)", "Sub Engineer (BPS-11)", "Naib Qasid (BPS-01)"],
        "WAPDA / NADRA": ["Junior Executive", "Data Entry Operator", "Assistant", "Meter Reader", "LDC", "UDC"],
        "Public Service Commission (PPSC/FPSC)": ["Tehsildar", "Assistant Director (AD)", "Inspector", "Lecturer", "Assistant (BPS-16)"],
        "Education Department": ["PST (Primary School Teacher)", "EST (Elementary School Teacher)", "SST (Secondary School Teacher)", "Headmaster"]
    }
    
    all_subjects = [
        "Current Affairs", "Pakistan Studies", "Islamiat", "General Knowledge", 
        "Islamic Jurisprudence (Fiqh / Khateeb)", "Everyday Science", "Basic Math", 
        "English Grammar", "Computer / IT", "Intelligence / IQ", "Pedagogy"
    ]

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_dept = st.selectbox("Select Department:", list(dept_post_map.keys()))
    with col2:
        selected_post = st.selectbox("Select Post (with BPS):", dept_post_map[selected_dept])
    with col3:
        subject = st.selectbox("Select Subject:", all_subjects)
    
    num_questions = st.selectbox("Number of Questions:", [5, 10, 15, 20, 25, 30])

    if st.button("Generate Test"):
        with st.spinner(f"Mind Forge Academy AI is extracting {num_questions} authentic past-paper questions..."):
            try:
                model = genai.GenerativeModel(MERA_MODEL) 
                
                # Sirf in makhsoos posts par Urdu chalegi (Primary/Religious base)
                urdu_posts = ["Naib Qasid", "Imam", "Moazzin", "Khateeb"]
                needs_urdu = any(p in selected_post for p in urdu_posts)
                
                lang_instruction = "The questions, options, and explanations MUST be completely in URDU." if needs_urdu else "The questions, options, and explanations MUST be entirely in ENGLISH."
                
                prompt = f"""You are an expert exam setter for testing agencies (FPSC, PPSC, NTS, OTS) in Pakistan. 
                Task: Generate {num_questions} authentic, frequently REPEATED past-paper MCQs for the subject of '{subject}'.
                Target Post: '{selected_post}' in '{selected_dept}'.
                
                CRITICAL INSTRUCTIONS:
                1. Difficulty Level: Match the educational criteria of the BPS scale. 
                   - BPS-01 to 05: Primary/Middle level.
                   - BPS-07 to 11 (Constable, LDC, ASI): F.A. / F.Sc. / Intermediate level.
                   - BPS-14 to 16 (Sub-Inspector, Assistant): Graduation (B.A. / B.Com / B.Sc.) level.
                   - BPS-17+: CSS / Master's Advanced level.
                2. Authenticity: Use real MCQs that appear in actual Pakistani govt exams. No random or fake questions.
                3. Current Affairs: If the subject is 'Current Affairs', use accurate data from Pakistani government sites up to August 2026.
                4. Language: {lang_instruction}
                
                Provide the response ONLY in this strict JSON array format, no extra text:
                [
                  {{"question": "Question text?", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "Option A", "explanation": "Detailed explanation..."}}
                ]"""
                
                response = model.generate_content(prompt)
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                
                st.session_state.quiz_data = json.loads(clean_text)
                st.session_state.submitted = False
                st.session_state.score = 0
                st.session_state.user_answers = {}
                st.session_state.is_urdu = needs_urdu
                st.rerun()
            except Exception as e:
                st.error(f"Error generating test: {e}")

    if st.session_state.quiz_data:
        st.write("---")
        
        text_class = "urdu-text" if st.session_state.get('is_urdu', False) else ""
        
        if not st.session_state.submitted:
            st.subheader("📝 Answer the Questions Below:")
            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"<h3 class='{text_class}'>Q{i+1}: {q['question']}</h3>", unsafe_allow_html=True)
                st.session_state.user_answers[i] = st.radio("Options:", q['options'], key=f"q_{i}", label_visibility="collapsed", index=None)
                st.write("")
                
            st.write("---")
            if st.button("Submit Test"):
                unanswered = [k for k, v in st.session_state.user_answers.items() if v is None]
                if unanswered:
                    st.warning("⚠️ Please answer all questions before submitting!")
                else:
                    st.session_state.submitted = True
                    st.session_state.score = 0
                    for i, q in enumerate(st.session_state.quiz_data):
                        if st.session_state.user_answers[i] == q['answer']:
                            st.session_state.score += 1
                    st.rerun()
        else:
            st.success(f"🏆 Final Score: {st.session_state.score} / {len(st.session_state.quiz_data)}")
            st.write("### Detailed Review:")
            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers[i]
                if user_ans == q['answer']:
                    st.info(f"✅ **Q{i+1}: {q['question']}** \n\n**Your Answer:** {user_ans} (Correct) \n\n*Explanation:* {q['explanation']}")
                else:
                    st.error(f"❌ **Q{i+1}: {q['question']}** \n\n**Your Answer:** {user_ans} | **Correct Answer:** {q['answer']} \n\n*Explanation:* {q['explanation']}")
            st.write("---")
            if st.button("Start a New Test"):
                st.session_state.quiz_data = None
                st.session_state.submitted = False
                st.rerun()

# ==========================================
# TAB 2: TYPING TEST LOGIC 
# ==========================================
with tab2:
    st.subheader("⌨️ Clerical Typing Speed Test")
    st.write("Target: 30 WPM (Words Per Minute) - LDC/UDC Standard")
    
    if 'typing_text' not in st.session_state:
        st.session_state.typing_text = ""
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0
        
    if st.button("Generate Typing Paragraph"):
        with st.spinner("Generating official clerical paragraph..."):
            try:
                model = genai.GenerativeModel(MERA_MODEL)
                prompt = "Write exactly 50-60 words of a normal English paragraph suitable for an official LDC/UDC clerical typing test. No formatting, no bullets, just plain text."
                resp = model.generate_content(prompt)
                
                st.session_state.typing_text = resp.text.strip()
                st.session_state.start_time = time.time() 
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.typing_text:
            custom_typing_html = f"""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; color: white; font-family: 'Poppins', sans-serif; margin-top: 20px;">
                <h4 style="color: #4da6ff;">Type the paragraph below (30 WPM Target):</h4>
                <p style="font-size: 18px; color: #e2e8f0; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px;">{st.session_state.typing_text}</p>
                
                <textarea id="typingBox" placeholder="Start typing here... Timer will start automatically!" style="width: 100%; height: 120px; font-size: 16px; padding: 15px; border-radius: 8px; margin-top: 10px; background: rgba(255,255,255,0.9); color: #000; border: none;"></textarea>
                
                <div style="margin-top: 20px; font-size: 22px; font-weight: bold; display: flex; justify-content: space-between;">
                    <span>⏱ Time: <span id="timer" style="color: #ff4d4d;">00:00</span></span>
                    <span>⌨️ WPM: <span id="wpm" style="color: #00e676;">0</span></span>
                </div>
            </div>

            <script>
                let timer = document.getElementById("timer");
                let wpmDisplay = document.getElementById("wpm");
                let typingBox = document.getElementById("typingBox");
                
                let time = 0;
                let timerInterval = null;
                let idleTimeout = null;
                let isRunning = false;

                function updateTime() {{
                    time++;
                    let m = Math.floor(time / 60).toString().padStart(2, '0');
                    let s = (time % 60).toString().padStart(2, '0');
                    timer.innerText = m + ":" + s;
                    
                    let textEntered = typingBox.value.trim();
                    let words = textEntered === "" ? 0 : textEntered.split(/\s+/).length;
                    let minutes = time / 60;
                    let wpm = minutes > 0 ? Math.round(words / minutes) : 0;
                    wpmDisplay.innerText = wpm;
                }}

                typingBox.addEventListener('input', () => {{
                    if (!isRunning) {{
                        timerInterval = setInterval(updateTime, 1000);
                        isRunning = true;
                    }}
                    clearTimeout(idleTimeout);
                    idleTimeout = setTimeout(() => {{
                        clearInterval(timerInterval);
                        isRunning = false;
                    }}, 3000);
                }});
            </script>
            """
            
            components.html(custom_typing_html, height=450)
                
            # === VIP AESTHETIC FOOTER ===
footer = """
<style>
.aesthetic-footer {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(30, 34, 45, 0.8);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 10px 25px;
    border-radius: 50px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    text-align: center;
    z-index: 999;
    transition: all 0.3s ease;
}
.aesthetic-footer:hover {
    background: rgba(40, 45, 60, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(77, 166, 255, 0.2);
}
.aesthetic-footer p {
    margin: 0;
    font-size: 14px;
    color: #e2e8f0;
    font-family: 'Poppins', sans-serif;
    letter-spacing: 0.5px;
}
.aesthetic-footer span {
    color: #4da6ff;
    font-weight: 600;
}
</style>
<div class="aesthetic-footer">
  <p>Developed by <span>Hafiz Muzammil</span> | 03079078917</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)