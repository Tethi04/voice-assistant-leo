# streamlit_app.py
import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Leo Voice Assistant Demo", page_icon="🎤", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
    }
    .stTextInput input {
        font-size: 16px;
        padding: 10px;
    }
    .demo-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎤 Leo Voice Assistant - Web Demo")
st.markdown("---")

# Sidebar with info
with st.sidebar:
    st.header("📋 About Leo")
    st.markdown("""
    **Features:**
    - 🕒 Time & Date
    - 🌤️ Weather Information
    - 📰 Latest News
    - 😄 Random Jokes
    - 📝 Notes & Reminders
    - 🔍 Web Search
    
    **Tech Stack:**
    - Python 3.10
    - SpeechRecognition
    - Text-to-Speech
    - OpenWeatherMap API
    - NewsAPI
    """)
    
    st.markdown("---")
    st.markdown("[GitHub Repository](https://github.com/Tethi04/voice-assistant-leo)")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔧 Try Leo Commands")
    
    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Command input
    command = st.text_input("Type a command for Leo:", placeholder="e.g., 'What time is it?' or 'Tell me a joke'")
    
    # Quick command buttons
    st.subheader("📋 Quick Commands:")
    quick_commands = [
        ("Hello Leo", "Greeting"),
        ("What time is it?", "Check time"),
        ("Tell me a joke", "Get a joke"),
        ("Weather in London", "Weather"),
        ("Latest news", "News headlines"),
        ("Open calculator", "App control"),
        ("Remember buy milk", "Add note"),
    ]
    
    cols = st.columns(4)
    for i, (cmd, desc) in enumerate(quick_commands):
        with cols[i % 4]:
            if st.button(f"{desc}", key=f"btn_{i}"):
                command = cmd
    
    # Process command
    if command:
        try:
            from src.commands import CommandHandler
            from src.utils import Utils
            
            handler = CommandHandler()
            response = handler.handle_command(command)
            
            # Add to history
            st.session_state.history.insert(0, {"command": command, "response": response})
            
            # Display response
            with st.expander("📝 Leo's Response:", expanded=True):
                st.markdown(f"**Command:** `{command}`")
                st.markdown(f"**Response:** {response}")
                
                # Special formatting for different responses
                if "weather" in command.lower():
                    st.metric("🌤️", "Weather data retrieved")
                elif "news" in command.lower():
                    st.success("📰 Latest headlines fetched")
                elif "joke" in command.lower():
                    st.balloons()
                    st.info("😄 Hope that made you smile!")
                elif "time" in command.lower():
                    st.metric("🕒", "Current time provided")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Note: Some features require API keys in .env file")

with col2:
    st.header("📊 Demo Features")
    
    # Feature showcase
    features = [
        {"icon": "🎤", "title": "Voice Control", "desc": "Works with microphone"},
        {"icon": "🌐", "title": "Online/Offline", "desc": "Functions without internet"},
        {"icon": "🔧", "title": "System Control", "desc": "Opens apps, searches web"},
        {"icon": "📝", "title": "Smart Notes", "desc": "Remembers important things"},
        {"icon": "🤖", "title": "AI-Powered", "desc": "Natural language processing"},
        {"icon": "🚀", "title": "Fast & Light", "desc": "Quick responses, low resource"},
    ]
    
    for feature in features:
        with st.container():
            st.markdown(f"""
            <div class='demo-box'>
                <h4>{feature['icon']} {feature['title']}</h4>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# Command history
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Command History")
    
    for i, item in enumerate(st.session_state.history[:5]):
        with st.expander(f"#{i+1}: {item['command'][:50]}..."):
            st.markdown(f"**Command:** `{item['command']}`")
            st.markdown(f"**Response:** {item['response'][:200]}...")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🔗 <a href='https://github.com/Tethi04/voice-assistant-leo'>View on GitHub</a> | 
    Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
