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
        st.markdown(f"""
        <div style="background-color: rgba(0, 0, 0, 0.3); padding: 25px; border-radius: 12px; border: 2px solid #1CB5E0; font-size: 22px; color: #ffffff; letter-spacing: 1px; line-height: 1.6; margin-bottom: 15px;">
        {st.session_state.typing_text}
        </div>
        """, unsafe_allow_html=True)
        
        components.html("""
        <div style="font-family: 'Poppins', sans-serif; color: #1CB5E0; font-size: 18px; font-weight: bold; text-align: right; padding-right: 10px;">
            ⏱️ Timer: <span id="clock">0</span> Seconds
        </div>
        <script>
            let sec = 0;
            setInterval(() => {
                sec++;
                document.getElementById('clock').innerText = sec;
            }, 1000);
        </script>
        """, height=35)
        
        user_typing = st.text_area("Start typing exactly as above:", height=150, placeholder="Timer has started! Start typing here...")
        
        if st.button("Check My Speed"):
            if user_typing:
                end_time = time.time()
                time_taken = end_time - st.session_state.start_time
                minutes = time_taken / 60
                
                typed_words = len(user_typing.split())
                wpm = round(typed_words / minutes)
                
                original_words = st.session_state.typing_text.split()
                user_words = user_typing.split()
                correct_words = sum(1 for o, u in zip(original_words, user_words) if o == u)
                accuracy = round((correct_words / max(len(original_words), 1)) * 100)
                
                st.write("---")
                st.subheader("📊 Performance Report")
                
                if wpm >= 30:
                    st.success(f"🔥 Outstanding! Speed: **{wpm} WPM**. You passed the clerical requirement!")
                else:
                    st.warning(f"⚠️ Speed: **{wpm} WPM**. You need a bit more practice to hit 30 WPM.")
                    
                st.write(f"- **Total Time Taken:** {round(time_taken)} seconds")
                st.write(f"- **Accuracy:** {accuracy}%")
            else:
                st.error("Please type something first!")
                # === CUSTOM FOOTER ===
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    text-align: center;
    padding: 10px;
    font-size: 15px;
    color: #a0a0a0;
}
</style>
<div class="footer">
  <p>Developed with 💻 & ❤️ by <b>03079078917 Muzammal</b></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)