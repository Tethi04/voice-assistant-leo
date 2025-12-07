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

# Custom CSS - NO F-STRINGS
st.markdown("""
<style>
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
        background: white;
        border: 2px solid #4CAF50;
        color: #4CAF50;
        padding: 10px 15px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        margin: 5px;
        font-weight: bold;
        width: 100%;
    }
    
    .quick-btn:hover {
        background: #4CAF50;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Chat bubbles */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin: 20px 0;
    }
    
    .user-msg {
        align-self: flex-end;
        background: #e3f2fd;
        padding: 10px 15px;
        border-radius: 15px 15px 3px 15px;
        max-width: 70%;
    }
    
    .leo-msg {
        align-self: flex-start;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 3px;
        max-width: 70%;
    }
    
    .time-stamp {
        font-size: 11px;
        opacity: 0.7;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for Voice - SEPARATE SECTION
voice_js = """
<script>
// Global variables
let recognition = null;
let isListening = false;

// Initialize speech recognition
function initVoiceRecognition() {
    // Check browser support
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        document.getElementById('voiceStatus').textContent = 
            'Voice recognition not supported in this browser. Use Chrome or Edge.';
        document.getElementById('voiceBtn').disabled = true;
        document.getElementById('voiceBtn').style.opacity = '0.5';
        return false;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    recognition.onstart = function() {
        isListening = true;
        document.getElementById('voiceBtn').classList.add('listening');
        document.getElementById('voiceBtn').innerHTML = '🛑 Stop Listening';
        document.getElementById('voiceStatus').innerHTML = '<span style="color:#4CAF50">🎤 Listening... Speak now!</span>';
    };
    
    recognition.onresult = function(event) {
        const command = event.results[0][0].transcript;
        document.getElementById('commandInput').value = command;
        
        // Trigger form submission
        setTimeout(() => {
            document.querySelector('button[type="submit"]').click();
        }, 100);
    };
    
    recognition.onerror = function(event) {
        console.log('Speech error:', event.error);
        stopListening();
    };
    
    recognition.onend = function() {
        stopListening();
    };
    
    return true;
}

// Start voice recognition
function startListening() {
    if (!recognition && !initVoiceRecognition()) {
        return;
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
                '<span style="color:red">❌ Microphone access denied. Please allow permission.</span>';
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
    document.getElementById('voiceStatus').innerHTML = 'Click microphone and speak';
}

// Toggle listening
function toggleVoice() {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

// Text-to-Speech function
function speakText(text) {
    if (!('speechSynthesis' in window)) {
        alert('Text-to-speech not supported in this browser.');
        return;
    }
    
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    // Try to get male voice
    const voices = window.speechSynthesis.getVoices();
    const maleVoices = voices.filter(voice => 
        voice.name.toLowerCase().includes('male') || 
        voice.name.toLowerCase().includes('david') ||
        voice.name.toLowerCase().includes('mark') ||
        !voice.name.toLowerCase().includes('female')
    );
    
    if (maleVoices.length > 0) {
        utterance.voice = maleVoices[0];
    }
    
    utterance.onstart = function() {
        console.log('Speaking:', text);
    };
    
    utterance.onerror = function(event) {
        console.error('Speech error:', event);
    };
    
    window.speechSynthesis.speak(utterance);
}

// Quick command handler
function sendQuickCommand(command) {
    document.getElementById('commandInput').value = command;
    setTimeout(() => {
        document.querySelector('button[type="submit"]').click();
    }, 100);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    initVoiceRecognition();
    
    // Add event listener to voice button
    document.getElementById('voiceBtn').addEventListener('click', toggleVoice);
    
    // Load voices for TTS
    if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
    }
});

// Test voice function
function testVoice() {
    speakText("Hello! I am Leo, your voice assistant. Try saying a command.");
}
</script>
"""

# Inject JavaScript
st.markdown(voice_js, unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.title("🎤 Leo Voice Assistant")
st.markdown("**Speak, type, or click commands. Leo will respond with voice!**")

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    # Voice Control Section
    st.subheader("🎙️ Voice Control")
    
    # Voice button and status
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <button id="voiceBtn" class="voice-btn">
            🎤 Start Voice Command
        </button>
        <div id="voiceStatus" style="margin-top: 10px; color: #666; font-size: 14px;">
            Click microphone and speak
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Test voice button
    if st.button("🔊 Test Voice", key="test_voice"):
        st.markdown("""
        <script>
            testVoice();
        </script>
        """, unsafe_allow_html=True)
        st.success("Playing test voice...")
    
    # Command Input Form
    with st.form("command_form", clear_on_submit=True):
        command_input = st.text_input(
            "📝 Or type command here:",
            placeholder="e.g., 'What time is it?' or 'Tell me a joke'",
            key="command_input"
        )
        
        submit_col1, submit_col2 = st.columns(2)
        with submit_col1:
            submitted = st.form_submit_button("🚀 Send Command", use_container_width=True)
        with submit_col2:
            clear_history = st.form_submit_button("🗑️ Clear History", use_container_width=True)
    
    # Process Command
    if submitted and command_input:
        try:
            # Import Leo modules
            from src.commands import CommandHandler
            
            handler = CommandHandler()
            response = handler.handle_command(command_input)
            
            # Add to chat history
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "user",
                "content": command_input
            })
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "leo",
                "content": response
            })
            
            # Display response
            st.markdown(f"""
            <div class="response-box">
                <h4>🤖 Leo says:</h4>
                <p>{response}</p>
                <button onclick="speakText('{response.replace("'", "\\\\'")}')" 
                        style="background: #4CAF50; color: white; border: none; 
                               padding: 10px 20px; border-radius: 5px; cursor: pointer;
                               margin-top: 10px; font-size: 16px;">
                    🔊 Speak This Response
                </button>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-speak the response
            st.markdown(f"""
            <script>
                setTimeout(function() {{
                    speakText("{response.replace('"', '\\\\"').replace("'", "\\\\'")}");
                }}, 300);
            </script>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure all files exist in src/ folder")
    
    # Clear history
    if clear_history:
        st.session_state.chat_history = []
        st.rerun()

with col2:
    # Quick Commands Section
    st.subheader("🎯 Quick Commands")
    
    # Define quick commands
    quick_commands = [
        ("👋 Hello Leo", "hello"),
        ("🕒 What time is it?", "what time is it"),
        ("😄 Tell me a joke", "tell me a joke"),
        ("🌤️ Weather", "what's the weather"),
        ("📰 News", "what's the news"),
        ("📝 Remember milk", "remember buy milk"),
        ("🔍 Search Python", "search python tutorials"),
        ("🚪 Exit", "exit")
    ]
    
    # Display quick command buttons
    for display_text, command_text in quick_commands:
        if st.button(display_text, key=f"qc_{command_text}", use_container_width=True):
            # Update command input
            st.session_state.command_input = command_text
            st.rerun()
    
    # Process quick command from session state
    if 'command_input' in st.session_state and st.session_state.command_input:
        cmd = st.session_state.command_input
        st.session_state.command_input = ""  # Clear after processing
        
        try:
            from src.commands import CommandHandler
            handler = CommandHandler()
            response = handler.handle_command(cmd)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
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
            
            # Auto-speak response
            st.markdown(f"""
            <script>
                speakText("{response.replace('"', '\\\\"').replace("'", "\\\\'")}");
            </script>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# Conversation History
st.markdown("---")
st.subheader("💬 Conversation History")

if st.session_state.chat_history:
    # Display in reverse order (newest first)
    for msg in reversed(st.session_state.chat_history[-8:]):  # Last 8 messages
        if msg["type"] == "user":
            st.markdown(f"""
            <div class="user-msg">
                <strong>You:</strong> {msg['content']}
                <div class="time-stamp">{msg['time']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="leo-msg">
                <strong>Leo:</strong> {msg['content']}
                <div class="time-stamp">{msg['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Clear history button
    if st.button("Clear All History", key="clear_all"):
        st.session_state.chat_history = []
        st.rerun()
else:
    st.info("No conversation yet. Try speaking or typing a command!")

# Features Section
st.markdown("---")
st.subheader("✨ Features")

features_cols = st.columns(4)
features = [
    ("🎤", "Voice Commands", "Speak naturally"),
    ("🔊", "Male Voice", "Clear human voice"),
    ("⌨️", "Text Input", "Type commands"),
    ("⚡", "Quick Commands", "One-click actions"),
]

for idx, (icon, title, desc) in enumerate(features):
    with features_cols[idx]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 10px; height: 120px;">
            <h2 style="margin: 10px 0;">{icon}</h2>
            <h4 style="margin: 5px 0;">{title}</h4>
            <p style="font-size: 14px; color: #666;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use", expanded=True):
    st.markdown("""
    ### **Voice Commands:**
    1. **Click the 🎤 microphone button**
    2. **Allow microphone permission** (browser will ask)
    3. **Speak your command** clearly
    4. **Wait for Leo's response** (text + voice)
    
    ### **Text Commands:**
    1. **Type** in the text box
    2. **Press Enter** or click "Send Command"
    3. **Leo responds** with voice
    
    ### **Quick Commands:**
    - Click any quick command button
    - Leo responds instantly with voice
    
    ### **Browser Support:**
    - ✅ **Chrome** (best)
    - ✅ **Edge** (good)
    - ✅ **Safari** (good)
    - ❌ **Firefox** (limited)
    
    ### **Troubleshooting:**
    - Ensure microphone is connected
    - Allow microphone permission
    - Use Chrome for best results
    - Speak clearly
    - Refresh page if issues
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>
        🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" target="_blank" 
           style="color: #4CAF50; text-decoration: none; font-weight: bold;">
           View Source Code on GitHub
        </a>
    </p>
    <p>🎤 Powered by Web Speech API | 🚀 Deployed on Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)

# Test voice on load
st.markdown("""
<script>
    // Test voice on page load
    window.addEventListener('load', function() {
        setTimeout(function() {
            if ('speechSynthesis' in window) {
                // Load voices
                window.speechSynthesis.getVoices();
            }
        }, 1000);
    });
</script>
""", unsafe_allow_html=True)
