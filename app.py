import streamlit as st
from rapidfuzz import process
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Custom FAQ knowledge base
faq = {
    "where is the library": "📚 The library is located in the Main Academic Building, 2nd floor.",
    "how do i register for exams": "📝 You can register for exams via the Student Portal under 'Exam Services'.",
    "what are cafeteria hours": "🍴 The cafeteria is open from 8 AM to 8 PM, Monday to Saturday.",
    "how do i contact my lecturer": "📧 You can contact your lecturer via university email or during office hours.",
    "is there a gym on campus": "💪 Yes! The campus gym is next to the sports complex and open daily 6 AM – 10 PM.",
}

# Function to query Gemini
def ask_gemini(user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Sorry, I couldn't get a response from Gemini. Error: {str(e)}"

# Function to find best FAQ response or fallback to Gemini
def get_response(user_input):
    questions = list(faq.keys())
    best_match, score, _ = process.extractOne(user_input.lower(), questions)

    if score > 70:  # confident FAQ match
        return faq[best_match]
    else:  # fallback to Gemini AI
        return ask_gemini(user_input)

# Streamlit UI
st.title("🎓 University Chatbot (Hybrid)")
st.write("Ask me anything about campus life!")

# Store conversation history
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", "")

if st.button("Ask"):
    if user_input.strip():
        response = get_response(user_input)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", response))

# Display conversation history
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**👤 {sender}:** {message}")
    else:
        st.markdown(f"**🤖 {sender}:** {message}")
