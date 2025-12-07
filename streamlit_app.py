# streamlit_app.py - COMPLETE WORKING VERSION
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
if 'current_command' not in st.session_state:
    st.session_state.current_command = ""

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 20px;
    }
    
    /* Voice button */
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
        display: inline-flex;
        align-items: center;
        justify-content: center;
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
    
    /* Response box */
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
    
    /* Quick command buttons */
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
    
    /* Chat bubbles */
    .user-bubble {
        background: #e3f2fd;
        padding: 10px 15px;
        border-radius: 15px 15px 3px 15px;
        margin: 5px 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    
    .leo-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 3px;
        margin: 5px 0;
        max-width: 80%;
        float: left;
        clear: both;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for Web Speech API
voice_js = """
<script>
// Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;

// Text-to-Speech
function speakText(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Set voice properties
        utterance.rate = 1.0;  // Speed
        utterance.pitch = 1.0; // Pitch
        utterance.volume = 1.0; // Volume
        
        // Try to get male voice
        const voices = window.speechSynthesis.getVoices();
        const maleVoices = voices.filter(voice => 
            voice.name.toLowerCase().includes('male') || 
            voice.name.toLowerCase().includes('david') ||
            voice.name.toLowerCase().includes('mark') ||
            voice.name.toLowerCase().includes('zira') === false
        );
        
        if (maleVoices.length > 0) {
            utterance.voice = maleVoices[0];
        }
        
        utterance.onstart = function() {
            console.log('Started speaking:', text);
        };
        
        utterance.onend = function() {
            console.log('Finished speaking');
        };
        
        window.speechSynthesis.speak(utterance);
    } else {
        alert('Text-to-speech not supported in this browser. Please use Chrome, Edge, or Safari.');
    }
}

// Initialize speech recognition
function initSpeechRecognition() {
    if (!SpeechRecognition) {
        document.getElementById('voiceStatus').innerHTML = 
            '❌ Voice recognition not supported. Please use Chrome or Edge.';
        document.getElementById('voiceBtn').disabled = true;
        return false;
    }
    
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    recognition.onstart = function() {
        isListening = true;
        document.getElementById('voiceBtn').classList.add('listening');
        document.getElementById('voiceBtn').innerHTML = '🛑 Stop Listening';
        document.getElementById('voiceStatus').innerHTML = '🎤 Listening... Speak now!';
    };
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('commandInput').value = transcript;
        
        // Submit the form
        document.getElementById('commandForm').submit();
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        stopListening();
    };
    
    recognition.onend = function() {
        stopListening();
    };
    
    return true;
}

// Start listening
function startListening() {
    if (!recognition) {
        if (!initSpeechRecognition()) {
            return;
        }
    }
    
    // Request microphone permission
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            stream.getTracks().forEach(track => track.stop());
            recognition.start();
        })
        .catch(function(err) {
            console.error('Microphone error:', err);
            document.getElementById('voiceStatus').innerHTML = 
                '❌ Microphone access denied. Please allow microphone permission.';
        });
}

// Stop listening
function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
    }
    isListening = false;
    document.getElementById('voiceBtn').classList.remove('listening');
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

// Quick command handler
function quickCommand(command) {
    document.getElementById('commandInput').value = command;
    document.getElementById('commandForm').submit();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initSpeechRecognition();
    
    // Add event listeners
    document.getElementById('voiceBtn').addEventListener('click', toggleListening);
    
    // Test TTS voices
    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = function() {
            console.log('Voices loaded:', window.speechSynthesis.getVoices().length);
        };
    }
});
</script>
"""

# Inject JavaScript
st.markdown(voice_js, unsafe_allow_html=True)

# Header
st.title("🎤 Leo Voice Assistant - Live Demo")
st.markdown("**Speak commands or type them below. Leo will respond with voice!**")

# Main layout
col1, col2 = st.columns([3, 2])

with col1:
    # Voice control section
    st.subheader("🎙️ Voice Control")
    
    # Voice button
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <button id="voiceBtn" class="voice-btn">
            🎤 Start Voice Command
        </button>
        <div id="voiceStatus" style="margin-top: 10px; color: #666; font-size: 14px;">
            Click microphone to speak
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Command input form
    with st.form("commandForm", clear_on_submit=True):
        command = st.text_input(
            "Or type your command here:", 
            key="commandInput",
            placeholder="e.g., 'What time is it?' or 'Tell me a joke'"
        )
        
        col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
        with col_submit1:
            submit_button = st.form_submit_button("🚀 Send Command", use_container_width=True)
        with col_submit2:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
        with col_submit3:
            speak_button = st.form_submit_button("🔊 Test Voice", use_container_width=True)
    
    # Process command
    if submit_button and command:
        try:
            from src.commands import CommandHandler
            from src.utils import Utils
            
            handler = CommandHandler()
            response = handler.handle_command(command)
            
            # Add to chat history
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
                <button onclick="speakText('{response.replace("'", "\\'")}')" 
                        style="background: #4CAF50; color: white; border: none; 
                               padding: 10px 20px; border-radius: 5px; cursor: pointer;
                               margin-top: 10px; font-size: 16px;">
                    🔊 Speak This Response
                </button>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-speak response
            st.markdown(f"""
            <script>
                setTimeout(function() {{
                    speakText("{response.replace('"', '\\"').replace("'", "\\'")}");
                }}, 500);
            </script>
            """, unsafe_allow_html=True)
            
        except ImportError as e:
            st.error(f"❌ Import Error: {str(e)}")
            st.info("Make sure all Python files exist in the src/ folder.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if speak_button:
        st.markdown("""
        <script>
            speakText("Hello! I am Leo, your voice assistant. Try saying 'What time is it?' or 'Tell me a joke'.");
        </script>
        """, unsafe_allow_html=True)
        st.success("🔊 Playing test voice...")

with col2:
    # Quick commands
    st.subheader("🎯 Quick Commands")
    
    quick_commands = [
        ("👋 Hello Leo", "hello"),
        ("🕒 What time is it?", "what time is it"),
        ("😄 Tell me a joke", "tell me a joke"),
        ("🌤️ Weather in London", "weather in london"),
        ("📰 Latest news", "what's the news"),
        ("📝 Remember milk", "remember buy milk"),
        ("🔍 Search Python", "search for python"),
        ("🔧 Open calculator", "open calculator"),
        ("📖 My notes", "what are my notes"),
        ("🚪 Exit program", "exit")
    ]
    
    # Create quick command buttons
    cols = st.columns(2)
    for i, (display, cmd) in enumerate(quick_commands):
        with cols[i % 2]:
            if st.button(display, key=f"quick_{i}", use_container_width=True):
                # Update command input and submit
                st.session_state.current_command = cmd
                st.rerun()
    
    # Process quick command from session state
    if st.session_state.current_command:
        command = st.session_state.current_command
        st.session_state.current_command = ""
        
        try:
            from src.commands import CommandHandler
            handler = CommandHandler()
            response = handler.handle_command(command)
            
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
            
            # Auto-speak response
            st.markdown(f"""
            <script>
                speakText("{response.replace('"', '\\"').replace("'", "\\'")}");
            </script>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# Chat history
st.markdown("---")
st.subheader("💬 Conversation History")

if st.session_state.chat_history:
    for msg in reversed(st.session_state.chat_history[-6:]):  # Show last 6
        if msg["type"] == "user":
            st.markdown(f"""
            <div class="user-bubble">
                <small style="color: #666;">{msg['time']}</small><br>
                <strong>You:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="leo-bubble">
                <small style="opacity: 0.8;">{msg['time']}</small><br>
                <strong>Leo:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
else:
    st.info("No conversation yet. Try speaking or typing a command!")

# Features section
st.markdown("---")
st.subheader("✨ Features")

features = st.columns(4)
features_data = [
    ("🎤", "Voice Commands", "Speak naturally to Leo"),
    ("🔊", "Male Voice", "Clear male voice responses"),
    ("🌐", "Browser-Based", "No installation needed"),
    ("⚡", "Instant", "Quick responses in real-time"),
]

for idx, (icon, title, desc) in enumerate(features_data):
    with features[idx]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border: 2px solid #e0e0e0; border-radius: 10px;">
            <h2>{icon}</h2>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use", expanded=True):
    st.markdown("""
    ### **Using Voice Commands:**
    1. **Click the 🎤 microphone button**
    2. **Allow microphone permission** when browser asks
    3. **Speak clearly** into your microphone
    4. **Wait for Leo's response** (text + voice)
    
    ### **Using Text Commands:**
    1. **Type** your command in the text box
    2. **Press Enter** or click "Send Command"
    3. **Leo will respond** with text and voice
    
    ### **Quick Commands:**
    - Click any quick command button
    - Leo will respond immediately
    
    ### **Browser Requirements:**
    - ✅ **Chrome** (recommended)
    - ✅ **Edge** 
    - ✅ **Safari**
    - ❌ Firefox (limited voice support)
    
    ### **Troubleshooting:**
    - Ensure microphone is connected
    - Allow microphone permission
    - Use Chrome for best results
    - Speak clearly and slowly
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" target="_blank" style="color: #4CAF50; text-decoration: none; font-weight: bold;">
        View Full Source Code on GitHub
    </a></p>
    <p>🎤 Powered by Web Speech API | 🚀 Deployed on Streamlit Cloud</p>
    <p style="font-size: 12px; margin-top: 20px;">
        Note: This is a web demo. For full desktop features (app opening, etc.), 
        download and run the Python application locally.
    </p>
</div>
""", unsafe_allow_html=True)
