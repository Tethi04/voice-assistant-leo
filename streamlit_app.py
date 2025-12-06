
import streamlit as st
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Leo Voice Assistant - LIVE",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject JavaScript for Web Speech API
st.markdown("""
<style>
    /* Custom styling */
    .voice-btn {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 50px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        margin: 5px;
    }
    .voice-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
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
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .mic-icon {
        font-size: 24px;
        margin-right: 10px;
    }
</style>

<script>
// Web Speech API for voice recognition
class VoiceRecognizer {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.finalTranscript = '';
        this.initSpeechRecognition();
    }
    
    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.updateUI(true);
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.finalTranscript = transcript;
                this.sendToPython(transcript);
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateUI(false);
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.updateUI(false);
            };
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    }
    
    startListening() {
        if (this.recognition && !this.isListening) {
            this.finalTranscript = '';
            this.recognition.start();
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }
    
    updateUI(listening) {
        const btn = document.getElementById('voiceBtn');
        const status = document.getElementById('voiceStatus');
        if (btn) {
            if (listening) {
                btn.classList.add('listening');
                btn.innerHTML = '🛑 Stop Listening';
                if (status) status.innerText = '🎤 Listening... Speak now!';
            } else {
                btn.classList.remove('listening');
                btn.innerHTML = '🎤 Start Voice Command';
                if (status) status.innerText = 'Click microphone to speak';
            }
        }
    }
    
    sendToPython(command) {
        // Send command to Streamlit via window.postMessage
        window.parent.postMessage({
            type: 'STREAMLIT_COMMAND',
            command: command
        }, '*');
    }
}

// Initialize when page loads
let voiceRecognizer = null;
document.addEventListener('DOMContentLoaded', () => {
    voiceRecognizer = new VoiceRecognizer();
    
    // Add voice button handler
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        voiceBtn.addEventListener('click', () => {
            if (voiceRecognizer.isListening) {
                voiceRecognizer.stopListening();
            } else {
                voiceRecognizer.startListening();
            }
        });
    }
});

// Text-to-Speech function
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

// Expose functions to window
window.speakText = speakText;
window.VoiceRecognizer = VoiceRecognizer;
</script>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_command' not in st.session_state:
    st.session_state.current_command = ""

# Custom components for voice
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <button id="voiceBtn" class="voice-btn">
        <span class="mic-icon">🎤</span> Start Voice Command
    </button>
    <div id="voiceStatus" style="margin-top: 10px; color: #666; font-size: 14px;">
        Click microphone to speak
    </div>
</div>
""", unsafe_allow_html=True)

# Main layout
st.title("🎤 Leo Voice Assistant - LIVE Voice Demo")
st.markdown("**Real voice recognition in your browser!**")

# Check for voice command from JavaScript
import streamlit.components.v1 as components

# Listen for messages from JavaScript
components.html("""
<script>
// Listen for messages from voice recognizer
window.addEventListener('message', function(event) {
    if (event.data.type === 'STREAMLIT_COMMAND') {
        // Send to Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: event.data.command
        }, '*');
    }
});
</script>
""", height=0)

# Columns layout
col1, col2 = st.columns([2, 1])

with col1:
    # Voice status
    st.subheader("🎙️ Voice Control")
    
    # Browser compatibility check
    with st.expander("🔍 Check Browser Compatibility"):
        st.markdown("""
        **Supported Browsers:**
        - ✅ Chrome (recommended)
        - ✅ Edge
        - ✅ Safari
        - ❌ Firefox (limited support)
        
        **Requirements:**
        - Microphone access permission
        - Modern browser
        - HTTPS connection (Streamlit provides this)
        """)
    
    # Manual command input (fallback) - FIXED: Use different key
    st.subheader("📝 Type Command (Fallback)")
    command_input = st.text_input("Or type command manually:", key="manual_input")
    
    # Process command from either voice or manual input
    command_to_process = ""
    
    # Check for voice command via query params
    query_params = st.experimental_get_query_params()
    if 'voice_command' in query_params:
        command_to_process = query_params['voice_command'][0]
    elif command_input:
        command_to_process = command_input
    
    # Process the command
    if command_to_process:
        try:
            from src.commands import CommandHandler
            from src.utils import Utils
            
            handler = CommandHandler()
            response = handler.handle_command(command_to_process)
            
            # Add to chat history
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "user",
                "content": command_to_process
            })
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "leo",
                "content": response
            })
            
            # Display response with voice button
            safe_response = response.replace("'", "&#39;").replace('"', "&quot;")
            
            st.markdown(f"""
            <div class="response-box">
                <h4>🤖 Leo's Response:</h4>
                <p>{response}</p>
                <button onclick="speakText('{safe_response}')" 
                        style="background: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    🔊 Speak Response
                </button>
            </div>
            """, unsafe_allow_html=True)
            
            # Special features based on command
            if "weather" in command_to_process.lower():
                st.balloons()
                st.success("🌤️ Weather data retrieved successfully!")
            elif "joke" in command_to_process.lower():
                st.snow()
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure all dependencies are installed in requirements.txt")

with col2:
    # Quick voice commands - FIXED: Don't use session_state for widget keys
    st.subheader("🎯 Quick Voice Commands")
    
    quick_cmds = [
        ("👋 Hello Leo", "hello"),
        ("🕒 What time is it?", "what time is it"),
        ("😄 Tell me a joke", "tell me a joke"),
        ("🌤️ Weather in London", "weather in london"),
        ("📰 Latest news", "what's the news"),
        ("📝 Remember buy milk", "remember buy milk"),
        ("🔍 Search Python", "search for python tutorials"),
        ("🔧 Open calculator", "open calculator"),
    ]
    
    for display_text, cmd_text in quick_cmds:
        if st.button(display_text, key=f"btn_{cmd_text}"):
            # Set query parameter instead of session state
            st.experimental_set_query_params(voice_command=cmd_text)
            st.rerun()
    
    # Chat history
    st.subheader("📜 Conversation History")
    if st.session_state.chat_history:
        for msg in reversed(st.session_state.chat_history[-10:]):  # Show last 10
            if msg["type"] == "user":
                st.markdown(f"**👤 You ({msg['time']}):** {msg['content']}")
            else:
                content = msg['content']
                if len(content) > 100:
                    content = content[:100] + "..."
                st.markdown(f"**🤖 Leo ({msg['time']}):** {content}")
    else:
        st.info("No conversation yet. Try speaking or typing a command!")

# Features showcase
st.markdown("---")
st.subheader("✨ Live Voice Features")

features_cols = st.columns(4)
features = [
    ("🎤", "Real Voice Input", "Speak commands naturally"),
    ("🔊", "Text-to-Speech", "Hear Leo's responses"),
    ("🌐", "Web Integration", "Works in any modern browser"),
    ("🚀", "Instant Response", "No installation needed"),
]

for idx, (icon, title, desc) in enumerate(features):
    with features_cols[idx]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <h3>{icon}</h3>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use Voice Features", expanded=True):
    st.markdown("""
    1. **Click the 🎤 microphone button** (give microphone permission when asked)
    2. **Speak clearly** into your microphone
    3. **Wait for Leo's response** (both text and voice)
    4. **Click 🔊 "Speak Response"** to hear Leo's reply
    5. **Use quick commands** for common tasks
    
    **Troubleshooting:**
    - Ensure microphone is connected and working
    - Grant microphone permission in browser
    - Use Chrome for best compatibility
    - Check browser console for errors (F12)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
    <p>🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" style="color: #4CAF50;">View Full Source Code on GitHub</a></p>
    <p>🎤 Voice powered by Web Speech API | 🚀 Deployed on Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)

# JavaScript to handle voice
components.html("""
<script>
// Check browser support
function checkVoiceSupport() {
    const voiceSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    const ttsSupported = 'speechSynthesis' in window;
    
    if (!voiceSupported) {
        document.getElementById('voiceStatus').innerHTML = 
            '⚠️ Voice recognition not supported in this browser. Try Chrome.';
        document.getElementById('voiceBtn').disabled = true;
        document.getElementById('voiceBtn').style.opacity = '0.5';
    }
    
    return voiceSupported && ttsSupported;
}

// Initialize on load
document.addEventListener('DOMContentLoaded', checkVoiceSupport);
</script>
""", height=0)
