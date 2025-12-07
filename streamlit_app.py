# streamlit_app.py - ERROR FREE VERSION
import streamlit as st
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Leo Voice Assistant",
    page_icon="🎤",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_command' not in st.session_state:
    st.session_state.current_command = ""

# JavaScript for Web Speech API - EXTERNAL FILE STYLE
javascript_code = """
<script>
// Web Speech API Functions
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;

// Initialize speech recognition
function initSpeechRecognition() {
    if (!SpeechRecognition) {
        document.getElementById('voiceStatus').innerHTML = 
            '<span style="color:red">❌ Voice not supported. Use Chrome/Edge.</span>';
        document.getElementById('voiceBtn').disabled = true;
        return false;
    }
    
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    recognition.onstart = function() {
        isListening = true;
        document.getElementById('voiceBtn').className = 'voice-btn listening';
        document.getElementById('voiceBtn').innerHTML = '🛑 Stop Listening';
        document.getElementById('voiceStatus').innerHTML = '<span style="color:green">🎤 Listening... Speak now!</span>';
    };
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('commandInput').value = transcript;
        document.getElementById('commandForm').submit();
    };
    
    recognition.onerror = function(event) {
        console.log('Speech error:', event.error);
        stopListening();
        if (event.error === 'not-allowed') {
            document.getElementById('voiceStatus').innerHTML = 
                '<span style="color:red">❌ Microphone access denied. Allow permission.</span>';
        }
    };
    
    recognition.onend = function() {
        stopListening();
    };
    
    return true;
}

// Start listening
function startListening() {
    if (!recognition && !initSpeechRecognition()) {
        return;
    }
    
    // Check microphone permission
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function(stream) {
                stream.getTracks().forEach(track => track.stop());
                recognition.start();
            })
            .catch(function(err) {
                document.getElementById('voiceStatus').innerHTML = 
                    '<span style="color:red">❌ Microphone error. Check permissions.</span>';
            });
    } else {
        recognition.start();
    }
}

// Stop listening
function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
    }
    isListening = false;
    document.getElementById('voiceBtn').className = 'voice-btn';
    document.getElementById('voiceBtn').innerHTML = '🎤 Start Voice Command';
    document.getElementById('voiceStatus').innerHTML = 'Click microphone to speak';
}

// Toggle listening
function toggleListening() {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

// Text-to-Speech with male voice
function speakText(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // Try to find male voice
        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
            // Prefer male-sounding voices
            const maleVoice = voices.find(v => 
                v.name.includes('Male') || 
                v.name.includes('David') ||
                v.name.includes('Mark') ||
                !v.name.includes('Female') &&
                !v.name.includes('Zira')
            );
            if (maleVoice) utterance.voice = maleVoice;
        }
        
        utterance.onstart = function() {
            console.log('Speaking:', text);
        };
        
        utterance.onend = function() {
            console.log('Finished speaking');
        };
        
        window.speechSynthesis.speak(utterance);
    } else {
        alert('Text-to-speech not supported. Use Chrome, Edge, or Safari.');
    }
}

// Quick command
function sendQuickCommand(command) {
    document.getElementById('commandInput').value = command;
    document.getElementById('commandForm').submit();
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initSpeechRecognition();
    document.getElementById('voiceBtn').addEventListener('click', toggleListening);
});
</script>

<style>
.voice-btn {
    background: linear-gradient(45deg, #FF6B6B, #FF8E53);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 50px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s;
}
.voice-btn:hover {
    transform: scale(1.05);
}
.voice-btn.listening {
    background: linear-gradient(45deg, #4CAF50, #8BC34A);
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
.response-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
}
.speak-btn {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
}
.chat-bubble {
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    max-width: 80%;
}
.user-bubble {
    background: #e3f2fd;
    margin-left: auto;
    border-bottom-right-radius: 3px;
}
.leo-bubble {
    background: #667eea;
    color: white;
    margin-right: auto;
    border-bottom-left-radius: 3px;
}
</style>
"""

# Inject JavaScript
st.markdown(javascript_code, unsafe_allow_html=True)

# Title
st.title("🎤 Leo Voice Assistant")
st.markdown("**Speak commands or type them. Leo will respond with voice!**")

# Voice Control Section
st.subheader("🎙️ Voice Control")

# Voice button
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <button id="voiceBtn" class="voice-btn">🎤 Start Voice Command</button>
    <div id="voiceStatus" style="margin-top: 10px; color: #666;">
        Click microphone to speak
    </div>
</div>
""", unsafe_allow_html=True)

# Main content columns
col1, col2 = st.columns([3, 2])

with col1:
    # Command input
    st.subheader("💬 Send Command")
    
    with st.form("commandForm", clear_on_submit=True):
        command = st.text_input(
            "Type command:",
            key="commandInput",
            placeholder="Example: 'What time is it?' or 'Tell me a joke'"
        )
        
        col_submit, col_clear = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("🚀 Send", use_container_width=True)
        with col_clear:
            cleared = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)
    
    # Process command
    if submitted and command:
        try:
            # Import Leo modules
            from src.commands import CommandHandler
            handler = CommandHandler()
            response = handler.handle_command(command)
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "user",
                "content": command
            })
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "leo",
                "content": response
            })
            
            # Display response - NO F-STRING WITH BACKSLASH
            html_response = response.replace("'", "&#39;").replace('"', "&quot;")
            st.markdown(f"""
            <div class="response-box">
                <h4>🤖 Leo Says:</h4>
                <p>{response}</p>
                <button class="speak-btn" onclick="speakText('{html_response}')">
                    🔊 Speak This Response
                </button>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-speak
            st.markdown(f"""
            <script>
                setTimeout(function() {{
                    speakText("{html_response}");
                }}, 300);
            </script>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    if cleared:
        st.session_state.chat_history = []
        st.rerun()

with col2:
    # Quick commands
    st.subheader("⚡ Quick Commands")
    
    quick_commands = [
        ("👋 Hello", "hello"),
        ("🕒 Time", "what time is it"),
        ("😄 Joke", "tell me a joke"),
        ("🌤️ Weather", "weather in London"),
        ("📰 News", "what's the news"),
        ("📝 Note", "remember buy milk"),
        ("🔍 Search", "search python"),
        ("🔧 Calculator", "open calculator"),
    ]
    
    # Display quick command buttons
    for display, cmd in quick_commands:
        if st.button(display, key=f"cmd_{cmd}", use_container_width=True):
            # Update session state
            st.session_state.current_command = cmd
            st.rerun()
    
    # Process quick command from session state
    if st.session_state.current_command:
        cmd = st.session_state.current_command
        st.session_state.current_command = ""
        
        try:
            from src.commands import CommandHandler
            handler = CommandHandler()
            response = handler.handle_command(cmd)
            
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "user", 
                "content": cmd
            })
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "leo",
                "content": response
            })
            
            # Auto-speak
            html_response = response.replace("'", "&#39;").replace('"', "&quot;")
            st.markdown(f"""
            <script>
                speakText("{html_response}");
            </script>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# Chat History
st.markdown("---")
st.subheader("📜 Conversation")

if st.session_state.chat_history:
    for msg in st.session_state.chat_history[-8:]:  # Show last 8
        if msg["type"] == "user":
            st.markdown(f"""
            <div class="chat-bubble user-bubble">
                <small>{msg['time']}</small><br>
                <strong>You:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bubble leo-bubble">
                <small>{msg['time']}</small><br>
                <strong>Leo:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Start by saying 'Hello Leo' or typing a command!")

# Features
st.markdown("---")
st.subheader("✨ Features")

features_cols = st.columns(4)
features = [
    ("🎤", "Voice Input", "Speak naturally"),
    ("🔊", "Voice Output", "Male voice responses"),
    ("🌐", "Browser-Based", "No installation"),
    ("⚡", "Real-time", "Instant responses"),
]

for idx, (icon, title, desc) in enumerate(features):
    with features_cols[idx]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 10px;">
            <h2>{icon}</h2>
            <h4>{title}</h4>
            <small>{desc}</small>
        </div>
        """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 Instructions", expanded=False):
    st.markdown("""
    **How to use:**
    1. **Voice Command:** Click 🎤 button → Speak → Leo responds with voice
    2. **Text Command:** Type in box → Press Enter → Leo responds
    3. **Quick Command:** Click any quick button
    
    **Best Results:**
    - Use **Chrome** or **Edge** browser
    - Allow microphone permission
    - Speak clearly and slowly
    
    **Voice Commands to Try:**
    - "Hello Leo"
    - "What time is it?"
    - "Tell me a joke" 
    - "Weather in London"
    - "What's the news?"
    - "Open calculator"
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p>🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" target="_blank" style="color: #4CAF50;">
        View Source Code on GitHub
    </a></p>
    <p>Powered by Web Speech API | Deployed on Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)
