# streamlit_app.py - WORKING VOICE VERSION
import streamlit as st
import sys
import os
import json
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
if 'last_command' not in st.session_state:
    st.session_state.last_command = ""

# Inject HTML/JavaScript for Web Speech API
st.markdown("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
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
        .speak-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="voice-container">
        <h3>🎤 Voice Control</h3>
        <button id="voiceBtn" class="voice-btn" onclick="toggleVoice()">
            <span id="micIcon">🎤</span>
            <span id="btnText">Start Voice Command</span>
        </button>
        <div id="status" class="status">Click microphone and speak</div>
        <div id="result" style="margin-top: 15px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px;"></div>
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
                document.getElementById('status').textContent = "Processing your command...";
                
                // Send to Streamlit
                sendCommandToPython(transcript);
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                document.getElementById('status').textContent = "Error: " + event.error;
                updateUI(false);
            };
            
            recognition.onend = function() {
                isListening = false;
                updateUI(false);
                document.getElementById('status').textContent = "Click microphone to speak again";
            };
            
            return true;
        } else {
            document.getElementById('status').textContent = "❌ Voice not supported in this browser. Use Chrome.";
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
            recognition.start();
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
    
    // Send command to Streamlit
    function sendCommandToPython(command) {
        // Create a hidden form to submit the command
        const form = document.createElement('form');
        form.method = 'POST';
        form.style.display = 'none';
        
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'voice_command';
        input.value = command;
        
        form.appendChild(input);
        document.body.appendChild(form);
        
        // Submit to Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: JSON.stringify({command: command})
        }, '*');
        
        // Also update URL parameter
        const url = new URL(window.location);
        url.searchParams.set('voice_cmd', encodeURIComponent(command));
        window.history.pushState({}, '', url);
    }
    
    // Text-to-Speech with MALE voice
    function speakWithMaleVoice(text) {
        if ('speechSynthesis' in window) {
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Try to get a male voice
            const voices = window.speechSynthesis.getVoices();
            let maleVoice = null;
            
            for (let voice of voices) {
                // Look for male voices (some browsers label them)
                if (voice.name.toLowerCase().includes('male') || 
                    voice.name.toLowerCase().includes('microsoft david') ||
                    voice.name.toLowerCase().includes('google uk male')) {
                    maleVoice = voice;
                    break;
                }
            }
            
            // If no male voice found, use default but adjust pitch
            if (maleVoice) {
                utterance.voice = maleVoice;
            } else {
                // Lower pitch for more masculine sound
                utterance.pitch = 0.8;  // Lower than default 1.0
                utterance.rate = 0.9;   // Slightly slower
            }
            
            utterance.volume = 1.0;
            utterance.lang = 'en-US';
            
            // Speak
            window.speechSynthesis.speak(utterance);
            
            return true;
        } else {
            alert('Text-to-speech not supported in this browser');
            return false;
        }
    }
    
    // Initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
        initSpeechRecognition();
        
        // Load voices for TTS
        if ('speechSynthesis' in window) {
            window.speechSynthesis.onvoiceschanged = function() {
                console.log('Voices loaded:', window.speechSynthesis.getVoices().length);
            };
        }
        
        // Check for voice command in URL
        const urlParams = new URLSearchParams(window.location.search);
        const voiceCmd = urlParams.get('voice_cmd');
        if (voiceCmd) {
            document.getElementById('result').innerHTML = `<strong>Command received:</strong> ${decodeURIComponent(voiceCmd)}`;
        }
    });
    
    // Make functions available globally
    window.speakWithMaleVoice = speakWithMaleVoice;
    window.sendCommandToPython = sendCommandToPython;
    window.toggleVoice = toggleVoice;
    
    </script>
</body>
</html>
""", unsafe_allow_html=True)

# Main interface
st.title("🎤 Leo Voice Assistant")
st.markdown("### Speak commands and hear responses in male voice!")

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Check for voice command from URL
    query_params = st.experimental_get_query_params()
    voice_command = ""
    
    if 'voice_cmd' in query_params:
        voice_command = query_params['voice_cmd'][0]
        st.success(f"🎤 Voice command detected: **{voice_command}**")
    
    # Manual input as fallback
    st.subheader("📝 Or type command manually:")
    manual_command = st.text_input("Enter command:", key="manual_input", value=voice_command)
    
    # Process command
    current_command = voice_command or manual_command
    
    if current_command:
        try:
            from src.commands import CommandHandler
            from src.utils import Utils
            
            handler = CommandHandler()
            response = handler.handle_command(current_command)
            
            # Add to chat history
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "user",
                "content": current_command
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
                <p style="font-size: 16px;">{response}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add speak button with male voice
            safe_response = response.replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <button onclick="speakWithMaleVoice('{safe_response}')" 
                    style="background: #2196F3; color: white; border: none; 
                           padding: 12px 24px; border-radius: 8px; cursor: pointer;
                           font-size: 16px; margin-top: 10px; display: block; width: 100%;">
                🔊 Hear Leo's Response (Male Voice)
            </button>
            """, unsafe_allow_html=True)
            
            # Visual feedback
            if "weather" in current_command.lower():
                st.balloons()
                st.success("🌤️ Weather data fetched!")
            elif "joke" in current_command.lower():
                st.balloons()
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Try commands like: 'hello', 'time', 'joke', 'weather london', 'news', 'remember note'")

with col2:
    st.subheader("🎯 Quick Commands")
    
    # Quick command buttons
    commands = [
        ("👋 Hello Leo", "hello"),
        ("🕒 Current Time", "what time is it"),
        ("😄 Tell a Joke", "tell me a joke"),
        ("🌤️ Weather", "what's the weather"),
        ("📰 Latest News", "what's the news"),
        ("📝 Add Note", "remember buy milk"),
        ("🔍 Search Web", "search for AI"),
        ("🧮 Open Calculator", "open calculator"),
    ]
    
    for display, cmd in commands:
        if st.button(display, key=f"btn_{cmd}"):
            # Set command in URL
            st.experimental_set_query_params(voice_cmd=cmd)
            st.rerun()
    
    st.markdown("---")
    st.subheader("📜 Recent Conversation")
    
    if st.session_state.chat_history:
        for msg in reversed(st.session_state.chat_history[-5:]):
            if msg["type"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Leo:** {msg['content'][:50]}...")
    else:
        st.info("No conversation yet. Try speaking or typing!")

# Features section
st.markdown("---")
st.subheader("✨ Voice Features")

features = st.columns(3)
with features[0]:
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
        <h3>🎤 Voice Input</h3>
        <p>Speak naturally in English</p>
    </div>
    """, unsafe_allow_html=True)

with features[1]:
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
        <h3>🎧 Male Voice</h3>
        <p>Responses in masculine tone</p>
    </div>
    """, unsafe_allow_html=True)

with features[2]:
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
        <h3>🌐 Browser-Based</h3>
        <p>No installation needed</p>
    </div>
    """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use Voice", expanded=True):
    st.markdown("""
    1. **Click the 🎤 "Start Voice Command" button**
    2. **Allow microphone access** when browser asks
    3. **Speak clearly** your command (e.g., "Hello Leo", "What time is it?")
    4. **Wait for Leo's response** to appear
    5. **Click 🔊 "Hear Leo's Response"** to listen in male voice
    
    **Best with:** Google Chrome on desktop
    **Commands to try:** hello, time, joke, weather london, news, remember [note]
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" style="color: #4CAF50; text-decoration: none; font-weight: bold;">
        View Full Project on GitHub
    </a></p>
    <p>🎤 Powered by Web Speech API | 🤖 Python Voice Assistant | 🚀 Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)

# Additional JavaScript for better voice handling
st.components.v1.html("""
<script>
// Listen for messages from parent
window.addEventListener('message', function(event) {
    if (event.data.type === 'streamlit:setComponentValue') {
        // Command received from voice input
        console.log('Command received:', event.data.value);
    }
});

// Test microphone permission
async function testMicrophone() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop());
        return true;
    } catch (err) {
        console.error('Microphone error:', err);
        alert('Please allow microphone access to use voice features.');
        return false;
    }
}

// Add permission test to voice button
document.getElementById('voiceBtn')?.addEventListener('click', async function(e) {
    if (!isListening) {
        const hasPermission = await testMicrophone();
        if (!hasPermission) {
            e.preventDefault();
            return;
        }
    }
});
</script>
""", height=0)
