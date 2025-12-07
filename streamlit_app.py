                                    # streamlit_app.py - FINAL WORKING VERSION
import streamlit as st
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Leo Voice Assistant 🎤",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'voice_command' not in st.session_state:
    st.session_state.voice_command = ""

# Main title
st.title("🎤 Leo Voice Assistant")
st.markdown("### Speak commands and hear responses in male voice!")

# Inject HTML/JavaScript for Web Speech API
st.markdown("""
<style>
    .voice-container {
        text-align: center;
        margin: 20px 0;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
    }
    .voice-btn {
        background: white;
        color: #667eea;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 50px;
        cursor: pointer;
        font-weight: bold;
        margin: 10px;
        transition: all 0.3s;
        display: inline-flex;
        align-items: center;
        gap: 10px;
    }
    .voice-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .voice-btn.listening {
        background: #FF6B6B;
        color: white;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .status {
        margin-top: 10px;
        font-size: 14px;
        color: rgba(255,255,255,0.8);
    }
    .result-box {
        margin-top: 15px;
        padding: 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    .speak-btn {
        background: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
        width: 100%;
    }
</style>

<div class="voice-container">
    <h3>🎤 Voice Control</h3>
    <button id="voiceBtn" class="voice-btn" onclick="toggleVoice()">
        <span id="micIcon">🎤</span>
        <span id="btnText">Start Voice Command</span>
    </button>
    <div id="status" class="status">Click microphone and speak</div>
    <div id="result" class="result-box"></div>
</div>

<script>
// Global variables
let isListening = false;
let recognition = null;

// Initialize speech recognition
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isListening = true;
            updateUI(true);
            document.getElementById('status').textContent = "🎤 Listening... Speak now!";
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('result').innerHTML = `<strong>You said:</strong> ${transcript}`;
            document.getElementById('status').textContent = "Processing...";
            
            // Send to Streamlit via window message
            window.parent.postMessage({
                type: 'LEO_VOICE_COMMAND',
                command: transcript
            }, '*');
            
            // Also update input field
            setTimeout(() => {
                const inputs = document.getElementsByTagName('input');
                for(let input of inputs) {
                    if(input.type === 'text') {
                        input.value = transcript;
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                        break;
                    }
                }
            }, 100);
        };
        
        recognition.onerror = function(event) {
            console.error('Speech error:', event.error);
            document.getElementById('status').textContent = "Error: " + event.error;
            updateUI(false);
        };
        
        recognition.onend = function() {
            isListening = false;
            updateUI(false);
            document.getElementById('status').textContent = "Click microphone to speak";
        };
        
        return true;
    } else {
        document.getElementById('status').textContent = "❌ Voice not supported. Use Chrome.";
        document.getElementById('voiceBtn').disabled = true;
        return false;
    }
}

// Toggle voice listening
function toggleVoice() {
    if (!recognition) {
        if (!initSpeechRecognition()) return;
    }
    
    if (isListening) {
        recognition.stop();
    } else {
        // Request microphone permission
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(() => recognition.start())
            .catch(() => alert('Please allow microphone access'));
    }
}

// Update UI
function updateUI(listening) {
    const btn = document.getElementById('voiceBtn');
    const icon = document.getElementById('micIcon');
    const text = document.getElementById('btnText');
    
    if (listening) {
        btn.classList.add('listening');
        icon.textContent = '🛑';
        text.textContent = 'Stop Listening';
    } else {
        btn.classList.remove('listening');
        icon.textContent = '🎤';
        text.textContent = 'Start Voice Command';
    }
}

// Text-to-Speech with MALE voice
function speakWithMaleVoice(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Get available voices
        const voices = window.speechSynthesis.getVoices();
        let maleVoice = null;
        
        // Try to find a male voice
        for (let voice of voices) {
            if (voice.name.toLowerCase().includes('male') || 
                voice.name.toLowerCase().includes('david') ||
                voice.name.toLowerCase().includes('microsoft')) {
                maleVoice = voice;
                break;
            }
        }
        
        // Configure voice
        if (maleVoice) utterance.voice = maleVoice;
        utterance.pitch = 0.8;  // Lower pitch for male voice
        utterance.rate = 0.9;   // Slightly slower
        utterance.volume = 1.0;
        utterance.lang = 'en-US';
        
        // Speak
        window.speechSynthesis.speak(utterance);
        return true;
    }
    return false;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initSpeechRecognition();
    
    // Listen for messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:setComponentValue') {
            // Handle Streamlit messages
        }
    });
});

// Make functions globally available
window.speakWithMaleVoice = speakWithMaleVoice;
window.toggleVoice = toggleVoice;
</script>
""", unsafe_allow_html=True)

# Create columns
col1, col2 = st.columns([2, 1])

with col1:
    # Manual input section
    st.subheader("📝 Type Command (or use voice above)")
    
    # Listen for voice commands from JavaScript
    import streamlit.components.v1 as components
    
    components.html("""
    <script>
    // Listen for voice commands and forward to Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'LEO_VOICE_COMMAND') {
            // Send to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: event.data.command
            }, '*');
        }
    });
    </script>
    """, height=0)
    
    # Text input for commands
    command = st.text_input("Enter your command:", key="command_input", 
                           placeholder="Type here or use voice above...")
    
    # Process button
    if st.button("🚀 Process Command", type="primary"):
        if command:
            st.session_state.voice_command = command
    
    # Also process if command is received from voice
    if st.session_state.voice_command:
        command = st.session_state.voice_command
        st.session_state.voice_command = ""  # Clear after processing

    # Process the command
    if command:
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
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        color: white; padding: 20px; border-radius: 10px; margin: 15px 0;">
                <h4>🤖 Leo's Response:</h4>
                <p style="font-size: 16px; line-height: 1.5;">{response}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add speak button
            safe_response = response.replace("'", "&#39;").replace('"', "&quot;")
            st.markdown(f"""
            <button onclick="speakWithMaleVoice('{safe_response}')" 
                    class="speak-btn">
                🔊 Hear Leo's Response (Male Voice)
            </button>
            """, unsafe_allow_html=True)
            
            # Visual effects based on command
            if "weather" in command.lower():
                st.balloons()
                st.success("🌤️ Weather data retrieved!")
            elif "joke" in command.lower():
                st.balloons()
                st.success("😄 Hope you enjoyed the joke!")
            elif "news" in command.lower():
                st.success("📰 Latest headlines fetched!")
            
        except ImportError as e:
            st.error(f"❌ Import error: {e}")
            st.info("Make sure all Python modules are installed in requirements.txt")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Try commands like: hello, time, joke, weather, news, remember [note]")

with col2:
    # Quick commands
    st.subheader("🎯 Quick Commands")
    
    quick_commands = [
        ("👋 Hello Leo", "hello"),
        ("🕒 Current Time", "what time is it"),
        ("😄 Tell a Joke", "tell me a joke"),
        ("🌤️ Weather", "what's the weather"),
        ("📰 Latest News", "what's the news"),
        ("📝 Add Note", "remember buy milk"),
        ("🔍 Search Web", "search for Python"),
        ("🧮 Calculator", "open calculator"),
    ]
    
    for display, cmd in quick_commands:
        if st.button(display, key=f"quick_{cmd}"):
            # Update the command input
            st.session_state.command_input = cmd
            st.rerun()
    
    st.markdown("---")
    
    # Conversation history
    st.subheader("📜 Conversation History")
    
    if st.session_state.chat_history:
        for msg in reversed(st.session_state.chat_history[-5:]):
            if msg["type"] == "user":
                st.markdown(f"**You ({msg['time']}):** {msg['content']}")
            else:
                content = msg['content']
                if len(content) > 60:
                    content = content[:60] + "..."
                st.markdown(f"**Leo ({msg['time']}):** {content}")
    else:
        st.info("No conversation yet. Try speaking or typing!")

# Features section
st.markdown("---")
st.subheader("✨ Features")

features = st.columns(3)
feature_data = [
    ("🎤", "Voice Input", "Speak commands naturally"),
    ("🔊", "Male Voice Output", "Hear responses in masculine tone"),
    ("🌐", "Browser-Based", "Works in Chrome/Edge/Safari"),
    ("📱", "Mobile Friendly", "Works on phones and tablets"),
    ("⚡", "Fast Response", "Instant command processing"),
    ("🔧", "System Control", "Open apps, search web, more")
]

for i in range(3):
    with features[i]:
        for j in range(2):
            idx = i * 2 + j
            if idx < len(feature_data):
                icon, title, desc = feature_data[idx]
                st.markdown(f"""
                <div style="padding: 15px; background: #f8f9fa; border-radius: 10px; margin-bottom: 10px;">
                    <h4>{icon} {title}</h4>
                    <p style="color: #666; font-size: 14px;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use", expanded=True):
    st.markdown("""
    ### **Using Voice:**
    1. **Click** 🎤 **"Start Voice Command"** button
    2. **Allow** microphone access when browser asks
    3. **Speak** your command clearly (e.g., "Hello Leo", "What time is it?")
    4. **Wait** for Leo's text response
    5. **Click** 🔊 **"Hear Leo's Response"** to listen
    
    ### **Using Text:**
    1. **Type** your command in the text box
    2. **Click** 🚀 **"Process Command"** button
    3. **Click** 🔊 button to hear response
    
    ### **Quick Commands:**
    - **Hello Leo** - Greeting
    - **What time is it?** - Current time
    - **Tell me a joke** - Random joke
    - **What's the weather?** - Weather info
    - **What's the news?** - Latest headlines
    - **Remember [note]** - Save a note
    - **Search for [topic]** - Web search
    
    ### **Best Results:**
    - Use **Google Chrome** (best voice support)
    - **Allow microphone** permissions
    - Speak **clearly** in quiet environment
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" 
           style="color: #4CAF50; text-decoration: none; font-weight: bold;">
        View Full Source Code on GitHub
    </a></p>
    <p>🎤 Voice Assistant Project | 🤖 Python + Streamlit | 🚀 Deployed on Cloud</p>
</div>
""", unsafe_allow_html=True)

# Add JavaScript listener for voice commands
components.html("""
<script>
// Listen for voice commands and update Streamlit
window.addEventListener('message', function(event) {
    if (event.data.type === 'LEO_VOICE_COMMAND') {
        // Store command in session storage
        sessionStorage.setItem('last_voice_command', event.data.command);
        
        // Show a notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;
        notification.innerHTML = `🎤 Voice command: "${event.data.command}"`;
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => notification.remove(), 3000);
    }
});

// Check for stored voice command on page load
document.addEventListener('DOMContentLoaded', function() {
    const lastCommand = sessionStorage.getItem('last_voice_command');
    if (lastCommand) {
        // Auto-fill the input field
        const inputs = document.getElementsByTagName('input');
        for(let input of inputs) {
            if(input.type === 'text') {
                input.value = lastCommand;
                input.dispatchEvent(new Event('input', {bubbles: true}));
                break;
            }
        }
        sessionStorage.removeItem('last_voice_command');
    }
});
</script>
""", height=0)
