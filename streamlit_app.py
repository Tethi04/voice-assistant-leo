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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS
st.markdown("""
<style>
    .voice-btn {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        margin: 10px;
    }
    .voice-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4);
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
        margin: 20px 0;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .quick-btn {
        background: #f0f2f6;
        border: 2px solid #4CAF50;
        color: #4CAF50;
        padding: 10px 15px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        margin: 5px;
        font-weight: bold;
    }
    .quick-btn:hover {
        background: #4CAF50;
        color: white;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🎤 Leo Voice Assistant - Live Demo")
st.markdown("**Speak commands or type them below. Leo will respond with voice!**")

# Main layout
col1, col2 = st.columns([3, 2])

with col1:
    # Voice control section
    st.subheader("🎙️ Voice Control")
    
    # JavaScript for voice
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <button id="voiceBtn" class="voice-btn" onclick="toggleListening()">
            🎤 Start Voice Command
        </button>
        <div id="voiceStatus" style="margin-top: 10px; color: #666; font-size: 14px;">
            Click microphone to speak
        </div>
    </div>
    
    <script>
    let isListening = false;
    let recognition = null;
    
    function speakText(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            
            // Try to get male voice
            const voices = speechSynthesis.getVoices();
            const maleVoices = voices.filter(v => 
                v.name.includes('Male') || 
                v.name.includes('David') ||
                !v.name.includes('Female')
            );
            
            if (maleVoices.length > 0) {
                utterance.voice = maleVoices[0];
            }
            
            speechSynthesis.speak(utterance);
        }
    }
    
    function toggleListening() {
        if (isListening) {
            stopListening();
        } else {
            startListening();
        }
    }
    
    function startListening() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Voice recognition not supported. Use Chrome or Edge.');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            isListening = true;
            document.getElementById('voiceBtn').classList.add('listening');
            document.getElementById('voiceBtn').innerHTML = '🛑 Stop Listening';
            document.getElementById('voiceStatus').innerHTML = '🎤 Listening... Speak now!';
        };
        
        recognition.onresult = function(event) {
            const command = event.results[0][0].transcript;
            document.getElementById('commandInput').value = command;
            document.getElementById('commandForm').submit();
        };
        
        recognition.onend = function() {
            stopListening();
        };
        
        recognition.onerror = function(event) {
            console.log('Speech error:', event.error);
            stopListening();
        };
        
        recognition.start();
    }
    
    function stopListening() {
        if (recognition) {
            recognition.stop();
        }
        isListening = false;
        document.getElementById('voiceBtn').classList.remove('listening');
        document.getElementById('voiceBtn').innerHTML = '🎤 Start Voice Command';
        document.getElementById('voiceStatus').innerHTML = 'Click microphone to speak';
    }
    
    function quickCommand(cmd) {
        document.getElementById('commandInput').value = cmd;
        document.getElementById('commandForm').submit();
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Command input
    with st.form("commandForm", clear_on_submit=True):
        command = st.text_input(
            "Or type your command here:",
            key="command_input",
            placeholder="e.g., 'What time is it?' or 'Tell me a joke'"
        )
        
        submitted = st.form_submit_button("🚀 Send Command", use_container_width=True)
    
    # Process command
    if submitted and command:
        try:
            # Import Leo modules
            from src.commands import CommandHandler
            from src.utils import Utils
            
            # Process command
            handler = CommandHandler()
            response = handler.handle_command(command)
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
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
            
            # Display response
            st.markdown(f"""
            <div class="response-box">
                <h4>🤖 Leo's Response:</h4>
                <p>{response}</p>
                <button onclick="speakText('{response.replace("'", " ")}')" 
                        style="background: #4CAF50; color: white; border: none; 
                               padding: 10px 20px; border-radius: 5px; cursor: pointer;
                               margin-top: 10px; font-size: 16px;">
                    🔊 Speak This Response
                </button>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-speak
            safe_response = response.replace("'", " ").replace('"', ' ')
            st.markdown(f"""
            <script>
                setTimeout(function() {{
                    speakText("{safe_response}");
                }}, 300);
            </script>
            """, unsafe_allow_html=True)
            
        except ImportError as e:
            st.error(f"Missing files: {str(e)}")
            st.info("Make sure src/ folder contains all .py files")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with col2:
    # Quick commands
    st.subheader("🎯 Quick Commands")
    
    quick_commands = [
        ("👋 Hello Leo", "hello"),
        ("🕒 What time?", "what time is it"),
        ("😄 Tell joke", "tell me a joke"),
        ("🌤️ Weather", "weather in london"),
        ("📰 News", "what's the news"),
        ("📝 Notes", "what are my notes"),
        ("🔍 Search", "search python"),
        ("🔧 Calculator", "open calculator"),
        ("🎵 Music", "play music"),
        ("🚪 Exit", "exit")
    ]
    
    # Create buttons
    cols = st.columns(2)
    for i, (display, cmd) in enumerate(quick_commands):
        with cols[i % 2]:
            if st.button(display, key=f"btn_{i}"):
                # Create JavaScript to submit form
                js_code = f"""
                <script>
                document.getElementById('commandInput').value = '{cmd}';
                document.getElementById('commandForm').submit();
                </script>
                """
                st.markdown(js_code, unsafe_allow_html=True)
    
    # Chat history
    st.subheader("📜 Recent Chat")
    if st.session_state.chat_history:
        for msg in reversed(st.session_state.chat_history[-4:]):
            if msg["type"] == "user":
                st.markdown(f"**You:** {msg['content']}")
                st.caption(msg['time'])
            else:
                st.markdown(f"**Leo:** {msg['content'][:50]}...")
                st.caption(msg['time'])
    else:
        st.info("No chat history yet")

# Features
st.markdown("---")
st.subheader("✨ Features")

col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)
with col_feat1:
    st.markdown("""
    <div style="text-align: center;">
        <h2>🎤</h2>
        <h4>Voice Commands</h4>
        <p>Speak naturally to Leo</p>
    </div>
    """, unsafe_allow_html=True)

with col_feat2:
    st.markdown("""
    <div style="text-align: center;">
        <h2>🔊</h2>
        <h4>Male Voice</h4>
        <p>Clear human voice</p>
    </div>
    """, unsafe_allow_html=True)

with col_feat3:
    st.markdown("""
    <div style="text-align: center;">
        <h2>🌐</h2>
        <h4>Browser-Based</h4>
        <p>No installation</p>
    </div>
    """, unsafe_allow_html=True)

with col_feat4:
    st.markdown("""
    <div style="text-align: center;">
        <h2>⚡</h2>
        <h4>Instant</h4>
        <p>Real-time responses</p>
    </div>
    """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Click 🎤 microphone button**
    2. **Allow microphone access**
    3. **Speak your command**
    4. **Wait for Leo's voice response**
    
    **Or:**
    1. **Type** command in text box
    2. **Press Enter** or click Send
    3. **Leo responds** with text + voice
    
    **Browser Support:**
    - ✅ Chrome (best)
    - ✅ Edge
    - ✅ Safari
    - ❌ Firefox (limited)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" style="color: #4CAF50;">View Source Code</a></p>
    <p>🎤 Web Speech API | 🚀 Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)
