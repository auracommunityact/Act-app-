# ============================================================
# 🎓 EduBot — Education App Chatbot
# College Project Demo | Streamlit Version
# Features: Handles typos, incomplete questions, any case
# ============================================================

import re
import difflib
import streamlit as st

# ------------------------------------------------------------
# 1. KNOWLEDGE BASE
# ------------------------------------------------------------
KB = [
    {
        "patterns": ["hi", "hello", "hey", "hii", "good morning", "good evening",
                     "namaste", "greetings"],
        "keywords": ["hi", "hello", "hey", "greetings", "morning", "evening",
                     "afternoon", "namaste", "hii", "helo"],
        "answer": "👋 Hello! I'm **EduBot**, your Education App assistant.\n\n"
                  "Ask me about **courses, fees, admission, exams, syllabus, "
                  "timetable, scholarships, placements, library, certificates** and more!"
    },
    {
        "patterns": ["what courses do you offer", "which courses are available",
                     "list of courses", "courses", "programs"],
        "keywords": ["course", "courses", "program", "programs", "stream",
                     "streams", "branch", "branches"],
        "answer": "📚 **Courses we offer:**\n\n"
                  "- Science – PCM / PCB\n"
                  "- Commerce\n"
                  "- Arts & Humanities\n"
                  "- Computer Science & IT\n"
                  "- Competitive Exam Prep (JEE / NEET / UPSC)\n\n"
                  "Ask me about the **fees** or **syllabus** of any course!"
    },
    {
        "patterns": ["what is the fee structure", "how much are the fees",
                     "fees", "fee details", "course fees"],
        "keywords": ["fee", "fees", "cost", "price", "pricing", "charge",
                     "charges", "payment", "amount", "expensive"],
        "answer": "💰 **Fee Structure (per year):**\n\n"
                  "- Science (PCM/PCB): ₹45,000\n"
                  "- Commerce: ₹35,000\n"
                  "- Arts: ₹28,000\n"
                  "- Computer Science: ₹55,000\n"
                  "- Competitive Exam Prep: ₹30,000\n\n"
                  "💡 Scholarships up to **50%** are available!"
    },
    {
        "patterns": ["admission process", "how to apply", "admission", "apply"],
        "keywords": ["admission", "admissions", "apply", "application", "enroll",
                     "enrol", "enrollment", "register", "registration", "join", "form"],
        "answer": "📝 **Admission Process:**\n\n"
                  "1. Open the app → tap **Admission**\n"
                  "2. Fill the online application form\n"
                  "3. Upload documents (10th/12th marksheet, ID proof, photo)\n"
                  "4. Pay the registration fee\n"
                  "5. Receive confirmation on email/SMS\n\n"
                  "⏰ Admissions are open till **31st July**."
    },
    {
        "patterns": ["when are the exams", "exam schedule", "exam dates", "exams"],
        "keywords": ["exam", "exams", "test", "tests", "assessment", "paper",
                     "papers", "result", "results", "marks", "score"],
        "answer": "📅 **Examinations:**\n\n"
                  "- Mid-Term: September\n"
                  "- Pre-Final: December\n"
                  "- Final Exam: March\n\n"
                  "📊 Results are published within **15 days** of the exam."
    },
    {
        "patterns": ["what is the syllabus", "syllabus details", "syllabus"],
        "keywords": ["syllabus", "curriculum", "topic", "topics", "chapter",
                     "chapters", "portion"],
        "answer": "📖 **Syllabus:**\n\n"
                  "Complete subject-wise syllabus is available in the app under "
                  "**Courses → Select Course → Syllabus**.\n\n"
                  "Includes unit-wise topics, chapter weightage and reference books."
    },
    {
        "patterns": ["class timetable", "class schedule", "timetable"],
        "keywords": ["timetable", "schedule", "timing", "timings", "class",
                     "classes", "batch", "batches"],
        "answer": "🗓️ **Class Timetable:**\n\n"
                  "- Morning batch: 7:00 AM – 11:00 AM\n"
                  "- Evening batch: 4:00 PM – 8:00 PM\n"
                  "- Weekend doubt sessions: Sat & Sun, 10:00 AM\n\n"
                  "Personalised timetable in the app under **My Schedule**."
    },
    {
        "patterns": ["how to get certificate", "certificate", "completion certificate"],
        "keywords": ["certificate", "certificates", "certification", "diploma",
                     "degree", "document", "documents", "marksheet"],
        "answer": "🏅 **Certificates:**\n\n"
                  "A **course completion certificate** is issued after you finish "
                  "the course and clear the final assessment.\n\n"
                  "Go to **Profile → My Certificates → Download**."
    },
    {
        "patterns": ["how to get refund", "refund policy", "refund"],
        "keywords": ["refund", "refunds", "cancel", "cancellation", "money",
                     "back", "return"],
        "answer": "💸 **Refund Policy:**\n\n"
                  "- Within 7 days of payment → **100% refund**\n"
                  "- Within 8–30 days → **50% refund**\n"
                  "- After 30 days → no refund\n\n"
                  "Raise a request via **Help → Refund Request**."
    },
    {
        "patterns": ["how to contact support", "contact details", "contact",
                     "customer care", "helpline"],
        "keywords": ["contact", "support", "help", "helpline", "phone", "number",
                     "email", "mail", "call", "whatsapp", "complaint"],
        "answer": "📞 **Contact Support:**\n\n"
                  "- Helpline: **1800-123-4567** (Mon–Sat, 9 AM – 6 PM)\n"
                  "- Email: **support@eduapp.com**\n"
                  "- WhatsApp: **+91-98765-43210**\n"
                  "- In-app: **Help → Raise a Ticket**"
    },
    {
        "patterns": ["i forgot my password", "unable to login", "login problem",
                     "how to login", "password reset"],
        "keywords": ["login", "log", "sign", "password", "username", "account",
                     "otp", "forgot", "blocked"],
        "answer": "🔐 **Login Help:**\n\n"
                  "1. Tap **Forgot Password** on the login screen\n"
                  "2. Enter your registered email / mobile number\n"
                  "3. Enter the OTP you receive\n"
                  "4. Set a new password\n\n"
                  "Still stuck? Call **1800-123-4567**."
    },
    {
        "patterns": ["study material", "study notes", "notes pdf"],
        "keywords": ["material", "materials", "notes", "note", "pdf", "resources",
                     "content", "videos", "video"],
        "answer": "📥 **Study Material:**\n\n"
                  "All notes, PDFs and recorded video lectures are in the app "
                  "under **Study Material**.\n\n"
                  "Filter by course, subject and chapter, and download PDFs for offline use."
    },
    {
        "patterns": ["library", "library timings", "digital library"],
        "keywords": ["library", "book", "books", "journal", "journals",
                     "reading", "ebook"],
        "answer": "📚 **Library:**\n\n"
                  "- Physical library: 8:00 AM – 9:00 PM (Mon–Sat)\n"
                  "- Digital library: 24×7 in the app\n"
                  "- 5,000+ books, journals and e-books available\n\n"
                  "Your library card is your student ID."
    },
    {
        "patterns": ["scholarship", "how to apply for scholarship", "scholarship details"],
        "keywords": ["scholarship", "scholarships", "financial", "aid",
                     "concession", "discount", "free", "waiver"],
        "answer": "🎓 **Scholarships:**\n\n"
                  "- Merit Scholarship — up to **50% fee waiver** (90%+ marks)\n"
                  "- Sports Scholarship — up to **30%**\n"
                  "- Need-based Aid — up to **40%**\n\n"
                  "Apply via **Admission → Scholarship Form**."
    },
    {
        "patterns": ["placement", "do you provide placement", "placement details",
                     "job assistance"],
        "keywords": ["placement", "placements", "job", "jobs", "internship",
                     "internships", "career", "hiring", "company", "companies", "salary"],
        "answer": "💼 **Placements:**\n\n"
                  "- 150+ partner companies\n"
                  "- Average package: **₹4.5 LPA**\n"
                  "- Highest package: **₹18 LPA**\n"
                  "- 92% placement rate last year\n\n"
                  "Training, mock interviews and resume workshops included."
    },
    {
        "patterns": ["faculty", "who are the teachers", "faculty details", "teachers"],
        "keywords": ["faculty", "teacher", "teachers", "professor", "professors",
                     "tutor", "tutors", "mentor", "staff", "instructor"],
        "answer": "👩‍🏫 **Our Faculty:**\n\n"
                  "We have **80+ expert teachers** with an average of 10+ years "
                  "of teaching experience.\n\n"
                  "See profiles and demo lectures in the app under **Faculty**."
    },
    {
        "patterns": ["attendance", "minimum attendance", "my attendance"],
        "keywords": ["attendance", "present", "absent", "leave", "leaves"],
        "answer": "📊 **Attendance:**\n\n"
                  "- Minimum **75%** attendance required to appear for exams\n"
                  "- Track daily attendance under **Profile → Attendance**\n"
                  "- Leave requests must be approved by your class teacher"
    },
    {
        "patterns": ["who are you", "what can you do", "app features", "how to use this app"],
        "keywords": ["app", "feature", "features", "use", "download", "install"],
        "answer": "📱 **About EduBot:**\n\n"
                  "I'm **EduBot**, the assistant of your Education App.\n\n"
                  "The app lets you:\n"
                  "- Browse courses & enrol online\n"
                  "- Watch video lessons & download notes\n"
                  "- Take mock tests and view results\n"
                  "- Pay fees and download receipts\n"
                  "- Chat with EduBot 24×7"
    },
    {
        "patterns": ["thank you", "thanks", "thank u", "thx"],
        "keywords": ["thank", "thanks", "thankyou", "thx", "grateful"],
        "answer": "😊 You're welcome! Happy learning. Ask me anything else anytime."
    },
    {
        "patterns": ["bye", "goodbye", "see you", "exit", "quit"],
        "keywords": ["bye", "goodbye", "exit", "quit", "later"],
        "answer": "👋 Goodbye! Keep learning and come back whenever you need help. 🎓"
    },
]

FALLBACK = ("🤔 Hmm, I'm not fully sure about that.\n\n"
            "Try asking about any of these:\n"
            "- Courses\n- Fees\n- Admission\n- Exams\n- Syllabus\n"
            "- Timetable\n- Scholarship\n- Placement\n- Library\n"
            "- Certificate\n- Refund\n- Login\n- Contact Support")

# ------------------------------------------------------------
# 2. TEXT NORMALIZATION + SPELL CORRECTION
# ------------------------------------------------------------
def normalize(text: str) -> str:
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str):
    return normalize(text).split()


EXTRA_WORDS = {
    "what", "which", "how", "when", "where", "why", "who", "is", "are", "was",
    "were", "the", "a", "an", "of", "to", "for", "in", "on", "at", "do", "does",
    "did", "can", "could", "you", "your", "me", "my", "i", "we", "our", "please",
    "tell", "about", "give", "need", "want", "there", "and", "or", "it", "this",
    "that", "with", "from", "will", "be", "have", "has", "any", "some", "more",
    "info", "information", "details", "know", "get", "take", "much", "many",
    "also", "not", "no", "yes", "ok", "okay", "am", "if", "so", "us", "them",
    "they", "he", "she", "his", "her", "new", "now", "time", "day", "date",
    "good", "best", "all", "list", "available",
}

VOCAB = set(EXTRA_WORDS)
for _entry in KB:
    for _p in _entry["patterns"]:
        VOCAB.update(tokenize(_p))
    VOCAB.update(_entry["keywords"])


def correct_word(word: str) -> str:
    if len(word) <= 2 or word.isdigit() or word in VOCAB:
        return word
    match = difflib.get_close_matches(word, VOCAB, n=1, cutoff=0.78)
    return match[0] if match else word


def correct_query(text: str) -> str:
    return " ".join(correct_word(w) for w in tokenize(text))


# ------------------------------------------------------------
# 3. SCORING ENGINE
# ------------------------------------------------------------
def score_entry(query_norm: str, entry: dict) -> float:
    q_tokens = tokenize(query_norm)
    if not q_tokens:
        return 0.0
    q_set = set(q_tokens)

    f1 = 0.0
    for p in entry["patterns"]:
        f1 = max(f1, difflib.SequenceMatcher(None, query_norm, normalize(p)).ratio())

    kws = set(entry["keywords"])
    hits = q_set & kws
    k1 = min(1.0, len(hits) / 2.0)

    fuzzy_hits = 0
    for qt in q_set:
        if qt in kws:
            fuzzy_hits += 1
            continue
        for kw in kws:
            if abs(len(qt) - len(kw)) <= 3:
                if difflib.SequenceMatcher(None, qt, kw).ratio() >= 0.80:
                    fuzzy_hits += 1
                    break
    k2 = fuzzy_hits / len(q_set)

    return 0.35 * f1 + 0.45 * k1 + 0.20 * k2


def get_answer(raw_query: str) -> str:
    if raw_query is None or not str(raw_query).strip():
        return "Please type a question 🙂"

    query_norm = normalize(raw_query)
    corrected = correct_query(raw_query)

    best_idx, best_score = -1, 0.0
    for i, entry in enumerate(KB):
        s = max(score_entry(query_norm, entry), score_entry(corrected, entry))
        if s > best_score:
            best_score, best_idx = s, i

    if best_idx >= 0 and best_score >= 0.30:
        return KB[best_idx]["answer"]
    return FALLBACK


# ------------------------------------------------------------
# 4. STREAMLIT UI
# ------------------------------------------------------------
st.set_page_config(
    page_title="EduBot — Education App Assistant",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for a nice chat look
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 10px 0;
        background: linear-gradient(90deg, #0b93f6, #6a11cb);
        color: white;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .main-header h1 { color: white; margin: 0; font-size: 26px; }
    .main-header p { color: #e0e0e0; margin: 4px 0 0 0; font-size: 13px; }
    .stChatMessage { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎓 EduBot</h1>
    <p>Education App Assistant — Ask me anything about your studies!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("### 📌 About This Project")
    st.markdown(
        "**EduBot** is a smart chatbot for an Education App.\n\n"
        "**Features:**\n"
        "- ✅ Handles spelling mistakes (`fes` → fees)\n"
        "- ✅ Handles incomplete questions\n"
        "- ✅ Case-insensitive\n"
        "- ✅ Fuzzy keyword matching\n"
        "- ✅ 20+ topics covered\n\n"
        "**Tech Stack:** Python, Streamlit, Difflib"
    )
    st.markdown("---")
    st.markdown("### 💡 Try These:")
    st.code("hi\nfes kitni hai\nadmision\nwat is timetabl\nscholrship", language="text")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Hi! I'm **EduBot**. Ask me about courses, fees, admission, exams, "
                        "syllabus, timetable, scholarships, placements, library, certificates..."}
        ]
        st.rerun()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "👋 Hi! I'm **EduBot**, your Education App assistant.\n\n"
                    "Ask me about **courses, fees, admission, exams, syllabus, timetable, "
                    "scholarships, placements, library, certificates** and more!\n\n"
                    "💡 Typos are fine — try `fes` or `admision`!"}
    ]

# Render all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "🧑"):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    reply = get_answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant", avatar="🎓"):
        st.markdown(reply)
