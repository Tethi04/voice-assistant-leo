# streamlit_app.py - MINIMAL WORKING VERSION
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Leo Voice Assistant", layout="centered")

# Title
st.title("🎤 Leo Voice Assistant")
st.write("Speak or type commands. Leo will respond with voice!")

# JavaScript for voice
st.markdown("""
<script>
// Simple voice function
function startVoice() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            document.getElementById('status').innerText = '🎤 Listening...';
        };
        
        recognition.onresult = function(event) {
            const command = event.results[0][0].transcript;
            document.getElementById('commandInput').value = command;
            document.getElementById('voiceForm').submit();
        };
        
        recognition.onend = function() {
            document.getElementById('status').innerText = 'Click to speak';
        };
        
        recognition.start();
    } else {
        alert('Voice not supported. Use Chrome or Edge.');
    }
}

// Text-to-speech
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
}
</script>

<style>
.voice-btn {
    background: #4CAF50;
    color: white;
    padding: 15px 30px;
    border: none;
    border-radius: 50px;
    font-size: 18px;
    cursor: pointer;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)

# Voice interface
st.markdown("""
<div style="text-align: center;">
    <button class="voice-btn" onclick="startVoice()">🎤 Click to Speak</button>
    <div id="status" style="color: #666;">Click button and speak</div>
</div>
""", unsafe_allow_html=True)

# Command input
with st.form("voiceForm"):
    command = st.text_input("Command:", key="commandInput")
    submitted = st.form_submit_button("Submit")
    
    if submitted and command:
        try:
            from src.commands import CommandHandler
            handler = CommandHandler()
            response = handler.handle_command(command)
            
            st.success("✅ Command received!")
            st.info(f"**Leo:** {response}")
            
            # Speak response
            safe_response = response.replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <script>
                speakText('{safe_response}');
            </script>
            <button onclick="speakText('{safe_response}')" 
                    style="background: #2196F3; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer;">
                🔊 Speak Again
            </button>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# Quick commands
st.subheader("Quick Commands:")
cols = st.columns(3)
commands = ["Hello", "Time", "Joke", "Weather", "News", "Exit"]

for i, cmd in enumerate(commands):
    with cols[i % 3]:
        if st.button(cmd):
            st.session_state.commandInput = cmd.lower()
            st.rerun()

st.markdown("---")
st.markdown("[GitHub Repository](https://github.com/Tethi04/voice-assistant-leo)")
