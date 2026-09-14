# 🎓 EduBot — Education App Chatbot

## Project Overview
EduBot is an intelligent rule-based chatbot designed for an Education App.
It answers student queries even when they contain spelling mistakes,
incomplete sentences, or inconsistent letter casing.

## Features
- ✅ Spelling mistake tolerance (fuzzy matching)
- ✅ Incomplete question handling
- ✅ Case-insensitive parsing
- ✅ 20+ education-related topics
- ✅ Real-time chat interface
- ✅ No external API required (fully offline logic)

## Technology Stack
| Component | Technology |
|-----------|------------|
| Language  | Python 3.9+ |
| UI        | Streamlit  |
| Matching  | Difflib (fuzzy string matching) |
| Algorithm | Weighted scoring: string similarity + keyword hits + fuzzy hits |

## How It Works
1. User input is normalized (lowercase, punctuation removed)
2. Each word is spell-corrected using `difflib.get_close_matches`
3. Query is scored against every knowledge-base entry using:
   - 35% — full-string fuzzy similarity
   - 45% — exact keyword match ratio
   - 20% — fuzzy keyword match ratio
4. Best-matching entry above threshold (0.30) returns its answer
5. Otherwise, a fallback suggestion list is shown

## How to Run
```bash
pip install -r requirements.txt
streamlit run edubot.py
