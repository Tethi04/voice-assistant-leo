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

# HTML/JavaScript for Voice (FIXED - will render properly)
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .voice-container {
            text-align: center;
            margin: 20px auto;
            padding: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            color: white;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .voice-btn {
            background: white;
            color: #667eea;
            border: none;
            padding: 18px 36px;
            font-size: 20px;
            border-radius: 50px;
            cursor: pointer;
            font-weight: bold;
            margin: 15px;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 12px;
            min-width: 250px;
        }
        .voice-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
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
            margin-top: 15px;
            font-size: 16px;
            color: rgba(255,255,255,0.9);
            min-height: 24px;
        }
        .result-box {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            border: 2px dashed rgba(255,255,255,0.3);
        }
        .mic-icon {
            font-size: 24px;
        }
    </style>
</head>
<body>
    <div class="voice-container">
        <h2 style="margin-bottom: 20px;">🎤 Voice Control Panel</h2>
        <button id="voiceBtn" class="voice-btn" onclick="toggleVoice()">
            <span id="micIcon" class="mic-icon">🎤</span>
            <span id="btnText">Start Voice Command</span>
        </button>
        <div id="status" class="status">Click microphone button and speak</div>
        <div id="result" class="result-box">
            Your voice command will appear here...
        </div>
    </div>

    <script>
    let isListening = false;
    let recognition = null;
    
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
                document.getElementById('result').innerHTML = `<strong>You said:</strong> "${transcript}"`;
                document.getElementById('status').textContent = "✅ Command captured!";
                
                // Send to Streamlit
                sendToStreamlit(transcript);
            };
            
            recognition.onerror = function(event) {
                document.getElementById('status').textContent = "❌ Error: " + event.error;
                updateUI(false);
            };
            
            recognition.onend = function() {
                isListening = false;
                updateUI(false);
                if (!document.getElementById('status').textContent.includes('Error')) {
                    document.getElementById('status').textContent = "Ready for next command";
                }
            };
            
            return true;
        } else {
            document.getElementById('status').textContent = "❌ Voice not supported. Use Chrome.";
            document.getElementById('voiceBtn').disabled = true;
            return false;
        }
    }
    
    function toggleVoice() {
        if (!recognition) {
            if (!initSpeechRecognition()) return;
        }
        
        if (isListening) {
            recognition.stop();
        } else {
            // Request microphone permission
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function(stream) {
                    stream.getTracks().forEach(track => track.stop());
                    recognition.start();
                })
                .catch(function(err) {
                    document.getElementById('status').textContent = "❌ Microphone access denied";
                });
        }
    }
    
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
    
    function sendToStreamlit(command) {
        // Update URL parameter
        const url = new URL(window.location);
        url.searchParams.set('voice_command', encodeURIComponent(command));
        window.history.pushState({}, '', url);
        
        // Reload to trigger Streamlit
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }
    
    function speakWithMaleVoice(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Find male voice
            const voices = window.speechSynthesis.getVoices();
            for (let voice of voices) {
                if (voice.name.toLowerCase().includes('male') || 
                    voice.name.toLowerCase().includes('david')) {
                    utterance.voice = voice;
                    break;
                }
            }
            
            // Male voice settings
            utterance.pitch = 0.8;
            utterance.rate = 0.9;
            utterance.volume = 1.0;
            utterance.lang = 'en-US';
            
            window.speechSynthesis.speak(utterance);
        }
    }
    
    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        initSpeechRecognition();
        
        // Check for existing voice command
        const params = new URLSearchParams(window.location.search);
        const voiceCmd = params.get('voice_command');
        if (voiceCmd) {
            document.getElementById('result').innerHTML = 
                `<strong>Last command:</strong> "${decodeURIComponent(voiceCmd)}"`;
        }
    });
    
    // Expose functions
    window.speakWithMaleVoice = speakWithMaleVoice;
    window.toggleVoice = toggleVoice;
    </script>
</body>
</html>
"""

# Display the voice interface
st.components.v1.html(html_code, height=400)

# Main title
st.title("🎤 Leo Voice Assistant - Live Demo")
st.markdown("### Speak commands and hear responses in male voice!")

# Get voice command from URL (FIXED: using st.query_params instead of experimental)
voice_command = ""
if 'voice_command' in st.query_params:
    voice_command = st.query_params['voice_command']

# Create columns
col1, col2 = st.columns([2, 1])

with col1:
    # Manual input fallback
    st.subheader("📝 Type Command (or use voice above):")
    
    # Use the voice command if available, otherwise empty
    command_input = st.text_input(
        "Enter command:", 
        value=voice_command,
        key="command_input",
        placeholder="e.g., 'hello', 'time', 'joke', 'weather london'"
    )
    
    # Process button
    if st.button("🚀 Process Command", type="primary", use_container_width=True):
        command_to_process = command_input.strip()
        
        if command_to_process:
            try:
                from src.commands import CommandHandler
                handler = CommandHandler()
                response = handler.handle_command(command_to_process)
                
                # Add to history
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
                
                # Display response
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                    color: white;
                    padding: 25px;
                    border-radius: 15px;
                    margin: 20px 0;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                ">
                    <h3 style="margin-top: 0;">🤖 Leo's Response</h3>
                    <p style="font-size: 18px; line-height: 1.6;">{response}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Speak button
                safe_response = response.replace("'", "\\'").replace('"', '\\"')
                st.markdown(f"""
                <button onclick="speakWithMaleVoice('{safe_response}')"
                        style="
                            background: linear-gradient(45deg, #FF6B6B, #FF8E53);
                            color: white;
                            border: none;
                            padding: 15px 30px;
                            border-radius: 10px;
                            cursor: pointer;
                            font-size: 18px;
                            font-weight: bold;
                            width: 100%;
                            margin-top: 15px;
                            transition: all 0.3s;
                        "
                        onmouseover="this.style.transform='scale(1.02)'"
                        onmouseout="this.style.transform='scale(1)'">
                    🔊 Hear Leo's Response (Male Voice)
                </button>
                """, unsafe_allow_html=True)
                
                # Visual effects
                if "weather" in command_to_process.lower():
                    st.balloons()
                    st.success("🌤️ Weather information retrieved!")
                elif "joke" in command_to_process.lower():
                    st.snow()
                    st.success("😄 Hope you enjoyed the joke!")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try commands like: hello, time, joke, weather london, news, remember note")
        else:
            st.warning("⚠️ Please enter a command first")

with col2:
    st.subheader("🎯 Quick Commands")
    st.markdown("Click any command below:")
    
    quick_commands = [
        ("👋 Hello Leo", "hello"),
        ("🕒 Current Time", "what time is it"),
        ("😄 Tell a Joke", "tell me a joke"),
        ("🌤️ Weather", "weather in london"),
        ("📰 Latest News", "what's the news"),
        ("📝 Add Note", "remember buy milk"),
        ("🔍 Search Web", "search python tutorials"),
        ("🧮 Open App", "open calculator"),
    ]
    
    for display_text, cmd in quick_commands:
        if st.button(display_text, key=f"quick_{cmd}", use_container_width=True):
            # Update URL with command
            st.query_params['voice_command'] = cmd
            st.rerun()
    
    st.markdown("---")
    st.subheader("📜 Recent Conversation")
    
    if st.session_state.chat_history:
        for msg in reversed(st.session_state.chat_history[-3:]):
            if msg["type"] == "user":
                st.markdown(f"**👤 You ({msg['time']}):** {msg['content']}")
            else:
                content = msg['content']
                if len(content) > 60:
                    content = content[:60] + "..."
                st.markdown(f"**🤖 Leo ({msg['time']}):** {content}")
    else:
        st.info("💬 No conversation yet. Try a command!")

# Features section
st.markdown("---")
st.subheader("✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px;">
        <h3 style="color: #667eea;">🎤 Voice Input</h3>
        <p>Speak commands naturally</p>
        <p style="font-size: 12px; color: #666;">Web Speech API powered</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px;">
        <h3 style="color: #4CAF50;">🎧 Male Voice</h3>
        <p>Masculine tone responses</p>
        <p style="font-size: 12px; color: #666;">Lower pitch settings</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px;">
        <h3 style="color: #FF6B6B;">🚀 Instant</h3>
        <p>No installation needed</p>
        <p style="font-size: 12px; color: #666;">Works in browser</p>
    </div>
    """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use (Click to expand)", expanded=True):
    st.markdown("""
    ### **🎤 Voice Instructions:**
    1. **Click the microphone button** above
    2. **Allow microphone access** when browser asks
    3. **Speak clearly** your command
    4. **Wait for Leo's response** to appear
    5. **Click 🔊 button** to hear in male voice
    
    ### **📝 Text Instructions:**
    1. **Type command** in the text box
    2. **Click "Process Command"** button
    3. **View response** and hear it
    
    ### **🎯 Best Commands to Try:**
    - "hello" - Greeting
    - "what time is it" - Current time
    - "tell me a joke" - Random joke
    - "weather in london" - Weather info
    - "what's the news" - Latest headlines
    - "remember buy milk" - Add note
    - "search python" - Web search
    
    ### **💡 Tips:**
    - Use **Google Chrome** for best voice support
    - Ensure **microphone is connected**
    - Speak in **quiet environment**
    - Allow **browser permissions**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 30px 0; color: #666;">
    <p style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">
        🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" 
           style="color: #4CAF50; text-decoration: none;">
           View Full Project on GitHub
        </a>
    </p>
    <p style="font-size: 14px;">
        🎤 Web Speech API | 🤖 Python Assistant | 🚀 Streamlit Cloud
    </p>
    <p style="font-size: 12px; margin-top: 20px; color: #999;">
        Voice features work best on Chrome/Edge desktop browsers
    </p>
</div>
""", unsafe_allow_html=True)
