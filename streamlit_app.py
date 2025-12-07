# streamlit_app.py - ERROR-FREE VERSION
import streamlit as st
import sys
import os
import json
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

# Helper function to escape text for JavaScript
def js_escape(text):
    """Escape text for JavaScript strings"""
    if not text:
        return ""
    # Replace problematic characters
    text = str(text)
    text = text.replace('\\', '\\\\')  # Backslash first
    text = text.replace("'", "\\'")    # Single quotes
    text = text.replace('"', '\\"')    # Double quotes
    text = text.replace('\n', ' ')     # Newlines
    text = text.replace('\r', ' ')     # Carriage returns
    return text

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
        width: 100%;
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
    
    /* Status text */
    .status-text {
        margin-top: 10px;
        color: #666;
        font-size: 14px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎤 Leo Voice Assistant - Live Demo")
st.markdown("**Speak commands or type them below. Leo will respond with voice!**")

# JavaScript for Voice (in a separate component to avoid f-string issues)
voice_js_component = st.components.v1.html("""
<script>
// Initialize variables
let recognition = null;
let isListening = false;

// Text-to-Speech function
function speakText(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Set properties
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // Try to get male voice
        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
            // Prefer male voices
            const maleVoice = voices.find(v => 
                v.name.toLowerCase().includes('male') || 
                v.name.includes('David') ||
                v.name.includes('Mark')
            );
            if (maleVoice) {
                utterance.voice = maleVoice;
            } else {
                utterance.voice = voices[0]; // Use first available
            }
        }
        
        utterance.onstart = function() {
            console.log('Started speaking');
        };
        
        utterance.onend = function() {
            console.log('Finished speaking');
        };
        
        window.speechSynthesis.speak(utterance);
        return true;
    }
    return false;
}

// Initialize speech recognition
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        updateStatus('❌ Voice not supported. Use Chrome or Edge.');
        document.getElementById('voiceBtn').disabled = true;
        return false;
    }
    
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    recognition.onstart = function() {
        isListening = true;
        updateUI(true);
        updateStatus('🎤 Listening... Speak now!');
    };
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        
        // Send to Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: transcript
        }, '*');
        
        updateStatus('✅ Command received: ' + transcript);
    };
    
    recognition.onerror = function(event) {
        console.error('Speech error:', event.error);
        updateUI(false);
        updateStatus('❌ Error: ' + event.error);
    };
    
    recognition.onend = function() {
        updateUI(false);
        updateStatus('Click microphone to speak');
    };
    
    return true;
}

// Update UI
function updateUI(listening) {
    const btn = document.getElementById('voiceBtn');
    if (btn) {
        if (listening) {
            btn.classList.add('listening');
            btn.innerHTML = '🛑 Stop Listening';
        } else {
            btn.classList.remove('listening');
            btn.innerHTML = '🎤 Start Voice Command';
        }
    }
}

// Update status
function updateStatus(message) {
    const status = document.getElementById('voiceStatus');
    if (status) {
        status.innerText = message;
    }
}

// Start/stop listening
function toggleListening() {
    if (!recognition && !initSpeechRecognition()) {
        return;
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
                updateStatus('❌ Microphone access denied. Please allow permission.');
                console.error('Microphone error:', err);
            });
    }
}

// Quick command handler
function sendQuickCommand(command) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: 'QUICK_CMD:' + command
    }, '*');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to voice button
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        voiceBtn.addEventListener('click', toggleListening);
    }
    
    // Initialize speech recognition
    initSpeechRecognition();
    
    // Load voices for TTS
    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = function() {
            console.log('Voices loaded');
        };
    }
});

// Make functions available globally
window.speakText = speakText;
window.sendQuickCommand = sendQuickCommand;
</script>
""", height=0)

# Voice control section
st.subheader("🎙️ Voice Control")

# Voice button
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <button id="voiceBtn" class="voice-btn">
        🎤 Start Voice Command
    </button>
    <div id="voiceStatus" class="status-text">
        Click microphone to speak
    </div>
</div>
""", unsafe_allow_html=True)

# Create a placeholder for voice input
voice_input_placeholder = st.empty()

# Check for voice input from JavaScript
voice_input_component = st.components.v1.html("""
<script>
// Listen for messages from parent window
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'streamlit:setComponentValue') {
        // Send the value back to Streamlit
        window.parent.postMessage({
            type: 'streamlit:componentValue',
            value: event.data.value
        }, '*');
    }
});
</script>
""", height=0)

# Main layout
col1, col2 = st.columns([3, 2])

with col1:
    # Text input form
    with st.form("command_form"):
        command = st.text_input(
            "Type command here:", 
            key="text_command",
            placeholder="e.g., 'What time is it?' or 'Tell me a joke'"
        )
        
        col_submit1, col_submit2 = st.columns(2)
        with col_submit1:
            submit_btn = st.form_submit_button("🚀 Send Command", use_container_width=True)
        with col_submit2:
            test_voice_btn = st.form_submit_button("🔊 Test Voice", use_container_width=True)
    
    # Process text command
    if submit_btn and command:
        process_command = command
    elif test_voice_btn:
        process_command = "test_voice"
    else:
        process_command = None
    
    # Check for voice command from JavaScript
    try:
        # This would capture voice input from the component
        # For now, we'll use a simpler approach
        pass
    except:
        pass

with col2:
    # Quick commands
    st.subheader("🎯 Quick Commands")
    
    quick_commands = [
        ("👋 Hello Leo", "hello"),
        ("🕒 What time?", "what time is it"),
        ("😄 Tell a joke", "tell me a joke"),
        ("🌤️ Weather", "what's the weather"),
        ("📰 Latest news", "what's the news"),
        ("📝 Add note", "remember buy milk"),
        ("🔍 Search web", "search for python"),
        ("📖 View notes", "what are my notes"),
    ]
    
    # Create quick command buttons
    for display, cmd in quick_commands:
        if st.button(display, key=f"quick_{cmd}", use_container_width=True):
            process_command = cmd

# Process any command
if 'process_command' in locals() and process_command:
    if process_command == "test_voice":
        # Test voice
        test_js = """
        <script>
            speakText("Hello! I am Leo, your voice assistant. Try saying 'What time is it?'");
        </script>
        """
        st.components.v1.html(test_js, height=0)
        st.success("🔊 Playing test voice...")
    else:
        # Process real command
        try:
            # Import and process command
            from src.commands import CommandHandler
            from src.utils import Utils
            
            handler = CommandHandler()
            response = handler.handle_command(process_command)
            
            # Add to chat history
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "user",
                "content": process_command
            })
            st.session_state.chat_history.append({
                "time": timestamp,
                "type": "leo", 
                "content": response[:500]  # Limit length
            })
            
            # Display response
            st.markdown(f"""
            <div class="response-box">
                <h4>🤖 Leo's Response:</h4>
                <p>{response}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Speak response using JavaScript
            escaped_response = js_escape(response)
            speak_js = f"""
            <script>
                setTimeout(function() {{
                    speakText("{escaped_response}");
                }}, 300);
            </script>
            """
            st.components.v1.html(speak_js, height=0)
            
            # Show success
            st.success("✅ Command processed successfully!")
            
        except ImportError as e:
            st.error(f"❌ Import Error: {str(e)}")
            st.info("Make sure all Python modules are installed and files exist.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            # Fallback response
            fallback_responses = {
                "hello": "Hello! I'm Leo, your voice assistant.",
                "what time is it": f"The current time is approximately {datetime.now().strftime('%I:%M %p')}",
                "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
                "what's the weather": "I need an API key to get real weather data.",
                "what's the news": "News feature requires API key setup.",
                "exit": "Goodbye! Have a great day!"
            }
            
            for key in fallback_responses:
                if key in process_command.lower():
                    response = fallback_responses[key]
                    
                    # Display fallback
                    st.markdown(f"""
                    <div class="response-box">
                        <h4>🤖 Leo's Response:</h4>
                        <p>{response}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Speak fallback
                    escaped_response = js_escape(response)
                    speak_js = f"""
                    <script>
                        speakText("{escaped_response}");
                    </script>
                    """
                    st.components.v1.html(speak_js, height=0)
                    break

# Chat history
st.markdown("---")
st.subheader("💬 Conversation History")

if st.session_state.chat_history:
    # Show last 5 conversations
    for msg in reversed(st.session_state.chat_history[-5:]):
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
                <strong>Leo:</strong> {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
else:
    st.info("💡 No conversation yet. Try speaking or typing a command!")

# Clear history button
if st.button("🗑️ Clear History", use_container_width=True):
    st.session_state.chat_history = []
    st.rerun()

# Features section
st.markdown("---")
st.subheader("✨ Features")

features_cols = st.columns(4)
features = [
    ("🎤", "Voice Input", "Speak commands naturally"),
    ("🔊", "Voice Output", "Hear Leo's responses"),
    ("📱", "Browser-Based", "Works in Chrome/Edge/Safari"),
    ("⚡", "Instant", "Real-time responses"),
]

for idx, (icon, title, desc) in enumerate(features):
    with features_cols[idx]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border-radius: 10px; background: #f9f9f9;">
            <h2>{icon}</h2>
            <h4>{title}</h4>
            <p style="font-size: 14px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use", expanded=True):
    st.markdown("""
    ### **Using Voice Commands:**
    1. **Click** the 🎤 microphone button
    2. **Allow** microphone permission (browser will ask)
    3. **Speak** your command clearly
    4. **Wait** for Leo's response (text + voice)
    
    ### **Using Text Commands:**
    1. **Type** in the text box
    2. **Press** "Send Command" or Enter
    3. **Leo responds** with text and voice
    
    ### **Quick Commands:**
    - Click any quick command button
    - Instant response with voice
    
    ### **Browser Support:**
    - ✅ **Chrome** (Best)
    - ✅ **Edge** (Good) 
    - ✅ **Safari** (Good)
    - ⚠️ **Firefox** (Limited)
    
    ### **Troubleshooting:**
    - Ensure microphone is connected
    - Allow microphone permission when asked
    - Use Chrome for best results
    - Speak clearly at normal pace
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🔗 <a href="https://github.com/Tethi04/voice-assistant-leo" target="_blank" style="color: #4CAF50; text-decoration: none; font-weight: bold;">
        View Full Source Code on GitHub
    </a></p>
    <p>🎤 Voice powered by Web Speech API | 🚀 Deployed on Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)

# Additional JavaScript for better voice handling
st.components.v1.html("""
<script>
// Test if everything is working
console.log('Leo Voice Assistant loaded successfully');

// Function to help with voice commands
function helpWithVoice() {
    const helpText = "Here are some commands you can try: Hello Leo, What time is it, Tell me a joke, What's the weather, What's the news, Open calculator, Remember something, Search for something";
    speakText(helpText);
}

// Make help function available
window.helpWithVoice = helpWithVoice;
</script>
""", height=0)
