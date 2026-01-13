import streamlit as st
import time
import os
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import base64

# ============================
# PAGE CONFIG & TRANSLATIONS
# ============================

st.set_page_config(
    page_title="Offline Emergency Triage Agent",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Translation dictionaries
TRANSLATIONS = {
    "en": {
        "title": "🚑 OFFLINE EMERGENCY TRIAGE AGENT",
        "subtitle": "AI-powered medical triage that works 100% offline",
        "settings": "Settings",
        "language": "Language",
        "airplane_mode": "Airplane Mode (100% Offline)",
        "offline_status": "✓ Running 100% offline",
        "online_status": "⚠️ Internet available",
        "voice_input": "Voice Input",
        "upload_audio": "Upload symptom audio (MP3/WAV)",
        "or_select": "OR Select sample symptom for demo:",
        "process_btn": "🚀 PROCESS SYMPTOM",
        "processing_pipeline": "Processing Pipeline",
        "step1": "1. Offline Speech-to-Text",
        "step1_desc": "Whisper Tiny (4-bit quantized) - Transcribed locally",
        "confidence": "Confidence",
        "step2": "2. Symptom Extraction",
        "step2_desc": "Llama 3 8B (4-bit quantized) - Processes locally",
        "step3": "3. Medical Triage Rules Engine",
        "step3_desc": "Deterministic rule-based - No hallucinations",
        "triage_result": "Triage Result",
        "emergency": "EMERGENCY - HIGH URGENCY",
        "high_risk": "HIGH RISK",
        "medium_risk": "MEDIUM RISK",
        "low_risk": "LOW RISK",
        "immediate_actions": "Immediate Actions Required",
        "recommended_actions": "Recommended Actions",
        "tech_specs": "Technical Specifications",
        "platform": "Platform",
        "platform_desc": "Android OS (mid-range devices)\nTensorFlow Lite Runtime\n100% Offline Operation",
        "ai_models": "AI Models",
        "ai_models_desc": "Whisper Tiny (4-bit quantized)\nLlama 3 8B (4-bit quantized)\n< 500MB total size",
        "privacy": "Privacy & Compliance",
        "privacy_desc": "Data never leaves device\nCompliant with Indian data laws\nZero cloud dependency",
        "pipeline_explanation": "Pipeline Explanation",
        "stt_explain": "Voice → Text locally using quantized Whisper model",
        "symptom_explain": "Text → Structured symptoms using quantized Llama",
        "rules_explain": "Symptoms → Urgency level using medical protocols",
        "demo_mode": "DEMO MODE: Simulating offline AI pipeline",
        "real_world": "Real-world deployment uses TensorFlow Lite on Android",
        "symptoms": {
            "s1": "High fever with severe headache",
            "s2": "Difficulty breathing and chest pain",
            "s3": "Minor cough and cold",
            "s4": "Vomiting with dizziness",
            "s5": "Severe injury to leg, cannot walk"
        },
        "actions": {
            "emergency": [
                "🏥 Seek emergency medical care immediately",
                "📞 Call ambulance: 108/102",
                "🛌 Keep patient in recovery position",
                "⏱️ Monitor breathing continuously",
                "🚑 Do not give food or water"
            ],
            "high": [
                "👨‍⚕️ Consult doctor within 2 hours",
                "🌡️ Monitor temperature every 30 minutes",
                "💊 Give paracetamol if no allergies",
                "🚰 Ensure hydration",
                "📝 Record symptom progression"
            ],
            "medium": [
                "📅 Schedule doctor visit within 24 hours",
                "🛌 Rest and monitor symptoms",
                "🚫 Avoid heavy meals",
                "📝 Note any symptom changes",
                "💧 Drink oral rehydration solution"
            ],
            "low": [
                "🏡 Home care recommended",
                "💤 Get adequate rest",
                "🥤 Drink plenty of fluids",
                "📞 Contact doctor if worsens",
                "🌡️ Monitor temperature twice daily"
            ]
        }
    },
    "hi": {
        "title": "🚑 ऑफ़लाइन इमरजेंसी ट्राएज एजेंट",
        "subtitle": "एआई-संचालित चिकित्सा ट्राएज जो 100% ऑफ़लाइन काम करता है",
        "settings": "सेटिंग्स",
        "language": "भाषा",
        "airplane_mode": "एयरप्लेन मोड (100% ऑफ़लाइन)",
        "offline_status": "✓ 100% ऑफ़लाइन चल रहा है",
        "online_status": "⚠️ इंटरनेट उपलब्ध है",
        "voice_input": "वॉयस इनपुट",
        "upload_audio": "लक्षण ऑडियो अपलोड करें (MP3/WAV)",
        "or_select": "या डेमो के लिए नमूना लक्षण चुनें:",
        "process_btn": "🚀 लक्षण प्रोसेस करें",
        "processing_pipeline": "प्रोसेसिंग पाइपलाइन",
        "step1": "1. ऑफ़लाइन स्पीच-टू-टेक्स्ट",
        "step1_desc": "व्हिस्पर टाइनी (4-बिट क्वांटाइज्ड) - स्थानीय रूप से ट्रांसक्राइब किया गया",
        "confidence": "विश्वास स्तर",
        "step2": "2. लक्षण निष्कर्षण",
        "step2_desc": "लामा 3 8बी (4-बिट क्वांटाइज्ड) - स्थानीय रूप से प्रोसेस करता है",
        "step3": "3. चिकित्सा ट्राएज नियम इंजन",
        "step3_desc": "निर्धारक नियम-आधारित - कोई हेलुसिनेशन नहीं",
        "triage_result": "ट्राएज परिणाम",
        "emergency": "आपातकाल - उच्च तात्कालिकता",
        "high_risk": "उच्च जोखिम",
        "medium_risk": "मध्यम जोखिम",
        "low_risk": "कम जोखिम",
        "immediate_actions": "तत्काल कार्रवाई आवश्यक",
        "recommended_actions": "अनुशंसित कार्रवाइयाँ",
        "tech_specs": "तकनीकी विशिष्टताएँ",
        "platform": "प्लेटफॉर्म",
        "platform_desc": "Android OS (मिड-रेंज डिवाइस)\nTensorFlow Lite रनटाइम\n100% ऑफ़लाइन ऑपरेशन",
        "ai_models": "एआई मॉडल",
        "ai_models_desc": "व्हिस्पर टाइनी (4-बिट क्वांटाइज्ड)\nलामा 3 8बी (4-बिट क्वांटाइज्ड)\n< 500MB कुल आकार",
        "privacy": "गोपनीयता और अनुपालन",
        "privacy_desc": "डेटा डिवाइस से बाहर नहीं जाता\nभारतीय डेटा कानूनों के अनुरूप\nशून्य क्लाउड निर्भरता",
        "pipeline_explanation": "पाइपलाइन स्पष्टीकरण",
        "stt_explain": "आवाज → पाठ (क्वांटाइज्ड व्हिस्पर मॉडल का उपयोग करके)",
        "symptom_explain": "पाठ → संरचित लक्षण (क्वांटाइज्ड लामा का उपयोग करके)",
        "rules_explain": "लक्षण → तात्कालिकता स्तर (चिकित्सा प्रोटोकॉल का उपयोग करके)",
        "demo_mode": "डेमो मोड: ऑफ़लाइन एआई पाइपलाइन सिम्युलेट कर रहा है",
        "real_world": "वास्तविक दुनिया में तैनाती Android पर TensorFlow Lite का उपयोग करती है",
        "symptoms": {
            "s1": "तेज बुखार और गंभीर सिरदर्द",
            "s2": "सांस लेने में तकलीफ और सीने में दर्द",
            "s3": "हल्की खांसी और जुकाम",
            "s4": "उल्टी और चक्कर आना",
            "s5": "पैर में गंभीर चोट, चल नहीं सकते"
        },
        "actions": {
            "emergency": [
                "🏥 तुरंत आपातकालीन चिकित्सा देखभाल लें",
                "📞 एम्बुलेंस कॉल करें: 108/102",
                "🛌 मरीज को रिकवरी पोजीशन में रखें",
                "⏱️ लगातार सांस पर निगरानी रखें",
                "🚑 भोजन या पानी न दें"
            ],
            "high": [
                "👨‍⚕️ 2 घंटे के भीतर डॉक्टर से परामर्श करें",
                "🌡️ हर 30 मिनट में तापमान की निगरानी करें",
                "💊 कोई एलर्जी न हो तो पेरासिटामोल दें",
                "🚰 हाइड्रेशन सुनिश्चित करें",
                "📝 लक्षण प्रगति रिकॉर्ड करें"
            ],
            "medium": [
                "📅 24 घंटे के भीतर डॉक्टर के पास जाएँ",
                "🛌 आराम करें और लक्षणों पर नजर रखें",
                "🚫 भारी भोजन से बचें",
                "📝 किसी भी लक्षण परिवर्तन को नोट करें",
                "💧 ओरल रिहाइड्रेशन सॉल्यूशन पिएँ"
            ],
            "low": [
                "🏡 घर पर देखभाल की सिफारिश की गई है",
                "💤 पर्याप्त आराम लें",
                "🥤 भरपूर तरल पदार्थ पिएँ",
                "📞 बिगड़ने पर डॉक्टर से संपर्क करें",
                "🌡️ दिन में दो बार तापमान की निगरानी करें"
            ]
        }
    }
}

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'offline_mode' not in st.session_state:
    st.session_state.offline_mode = True
if 'processing' not in st.session_state:
    st.session_state.processing = False

def get_text(key):
    return TRANSLATIONS[st.session_state.lang][key]

# ============================
# SIDEBAR
# ============================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/stethoscope.png", width=80)
    
    # Language selection
    lang_options = {
        "English": {"icon": "🇺🇸", "code": "en"},
        "Hindi": {"icon": "🇮🇳", "code": "hi"}
    }
    
    selected_lang = option_menu(
        menu_title=get_text("language"),
        options=list(lang_options.keys()),
        icons=[lang_options[lang]["icon"] for lang in lang_options],
        menu_icon="translate",
        default_index=0 if st.session_state.lang == "en" else 1,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )
    
    st.session_state.lang = lang_options[selected_lang]["code"]
    
    st.markdown("---")
    
    # Airplane Mode Toggle
    st.markdown(f"### ✈️ {get_text('airplane_mode')}")
    offline_mode = st.toggle("", value=st.session_state.offline_mode, key="offline_toggle")
    st.session_state.offline_mode = offline_mode
    
    if offline_mode:
        st.success(f"**{get_text('offline_status')}**")
        st.caption("No internet connectivity required")
    else:
        st.warning(f"**{get_text('online_status')}**")
        st.caption("Internet available for updates")
    
    st.markdown("---")
    
    # Demo instructions
    st.markdown("### 🎯 Demo Guide")
    st.markdown("""
    1. Select Hindi language
    2. Ensure Airplane Mode is ON
    3. Select: **"Difficulty breathing and chest pain"**
    4. Click **PROCESS SYMPTOM**
    5. Watch the pipeline execute
    """)
    
    st.markdown("---")
    
    # Team info
    st.markdown("### 👥 Team CODENOVA")
    st.markdown("**Snowfrost Hackathon 2026**")
    st.markdown("Theme: **AI for Social Innovation**")

# ============================
# MAIN CONTENT
# ============================

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"<h1 style='text-align: center; color: #1E3A8A;'>{get_text('title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #64748B;'>{get_text('subtitle')}</p>", unsafe_allow_html=True)

st.markdown("---")

# Main columns
input_col, result_col = st.columns([1, 1])

# ============================
# LEFT COLUMN - INPUT
# ============================

with input_col:
    st.markdown(f"### 🎤 {get_text('voice_input')}")
    
    # Show connectivity status
    if st.session_state.offline_mode:
        status_html = """
        <div style='background-color: #0F766E; color: white; padding: 10px; border-radius: 10px; text-align: center;'>
        <h4>📴 OFFLINE MODE ACTIVE</h4>
        <p>All processing happens locally on device</p>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)
    else:
        status_html = """
        <div style='background-color: #D97706; color: white; padding: 10px; border-radius: 10px; text-align: center;'>
        <h4>📶 ONLINE MODE</h4>
        <p>Cloud connectivity available</p>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)
    
    st.markdown(f"**{get_text('upload_audio')}**")
    audio_file = st.file_uploader("", type=["mp3", "wav", "m4a"], label_visibility="collapsed")
    
    st.markdown(f"**{get_text('or_select')}**")
    
    # Symptom selection
    symptoms = get_text("symptoms")
    symptom_options = list(symptoms.values())
    
    selected_symptom = st.selectbox(
        "",
        symptom_options,
        index=1 if "breathing" in symptom_options[1].lower() or "सांस" in symptom_options[1] else 0,
        label_visibility="collapsed"
    )
    
    # Map symptom to risk level
    symptom_to_risk = {
        symptom_options[0]: "high",
        symptom_options[1]: "emergency",
        symptom_options[2]: "low",
        symptom_options[3]: "medium",
        symptom_options[4]: "emergency"
    }
    
    # Process button
    if st.button(f"**{get_text('process_btn')}**", type="primary", use_container_width=True):
        st.session_state.processing = True
        st.session_state.selected_symptom = selected_symptom
        st.session_state.risk_level = symptom_to_risk[selected_symptom]
        st.rerun()

# ============================
# RIGHT COLUMN - PROCESSING & RESULTS
# ============================

with result_col:
    if not st.session_state.get('processing', False):
        # Show waiting state
        st.markdown(f"### 📋 {get_text('triage_result')}")
        st.info(f"👈 {get_text('or_select')} और PROCESS बटन दबाएं")
        
        # Show technical specs
        st.markdown("---")
        st.markdown(f"### 🔧 {get_text('tech_specs')}")
        
        spec_col1, spec_col2, spec_col3 = st.columns(3)
        
        with spec_col1:
            st.markdown(f"**{get_text('platform')}**")
            st.markdown(f"```\n{get_text('platform_desc')}\n```")
        
        with spec_col2:
            st.markdown(f"**{get_text('ai_models')}**")
            st.markdown(f"```\n{get_text('ai_models_desc')}\n```")
        
        with spec_col3:
            st.markdown(f"**{get_text('privacy')}**")
            st.markdown(f"```\n{get_text('privacy_desc')}\n```")
    
    else:
        # Show processing pipeline
        st.markdown(f"### 🔄 {get_text('processing_pipeline')}")
        
        # Progress bar
        progress_bar = st.progress(0)
        
        # Step 1: Offline STT
        with st.expander(f"**{get_text('step1')}**", expanded=True):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{get_text('stt_explain')}**")
                st.code(f"Input: '{st.session_state.selected_symptom}'")
                st.markdown(f"**{get_text('step1_desc')}**")
            
            with col_b:
                st.metric(get_text("confidence"), "94%")
            
            progress_bar.progress(33)
            time.sleep(0.5)
        
        # Step 2: Symptom Extraction
        with st.expander(f"**{get_text('step2')}**", expanded=True):
            # Simulate extracted symptoms based on input
            if "breathing" in st.session_state.selected_symptom.lower() or "सांस" in st.session_state.selected_symptom:
                extracted = ["breathing_difficulty", "chest_pain", "rapid_heart_rate"] if st.session_state.lang == "en" else ["सांस लेने में तकलीफ", "सीने में दर्द", "तेज हृदय गति"]
            elif "fever" in st.session_state.selected_symptom.lower() or "बुखार" in st.session_state.selected_symptom:
                extracted = ["high_fever", "headache", "body_ache"] if st.session_state.lang == "en" else ["तेज बुखार", "सिरदर्द", "शरीर में दर्द"]
            else:
                extracted = ["cough", "cold", "fatigue"] if st.session_state.lang == "en" else ["खांसी", "जुकाम", "थकान"]
            
            st.markdown(f"**{get_text('symptom_explain')}**")
            st.code(f"Extracted: {extracted}")
            st.markdown(f"**{get_text('step2_desc')}**")
            
            progress_bar.progress(66)
            time.sleep(0.5)
        
        # Step 3: Triage Engine
        with st.expander(f"**{get_text('step3')}**", expanded=True):
            st.markdown(f"**{get_text('rules_explain')}**")
            
            # Show rule being triggered
            if st.session_state.risk_level == "emergency":
                rule = "IF breathing_difficulty AND chest_pain → EMERGENCY" if st.session_state.lang == "en" else "IF सांस_लेने_में_तकलीफ AND सीने_में_दर्द → आपातकाल"
                st.error(f"🚨 **Rule Triggered:** {rule}")
            elif st.session_state.risk_level == "high":
                rule = "IF fever > 39°C AND severe_headache → HIGH RISK" if st.session_state.lang == "en" else "IF बुखार > 39°C AND गंभीर_सिरदर्द → उच्च जोखिम"
                st.warning(f"⚠️ **Rule Triggered:** {rule}")
            
            st.code("""
            Medical Protocol Rules:
            1. Airway/Breathing/Circulation issues → EMERGENCY
            2. Severe pain or high fever → HIGH RISK
            3. Vomiting or dizziness → MEDIUM RISK
            4. Mild symptoms → LOW RISK
            """)
            
            st.markdown(f"**{get_text('step3_desc')}**")
            
            progress_bar.progress(100)
            time.sleep(0.5)
        
        st.markdown("---")
        
        # TRIAGE RESULT
        st.markdown(f"### 📋 {get_text('triage_result')}")
        
        risk_level = st.session_state.risk_level
        actions = get_text("actions")[risk_level]
        
        # Color-coded result box
        if risk_level == "emergency":
            color = "#DC2626"
            title = get_text("emergency")
            icon = "🚨"
        elif risk_level == "high":
            color = "#F59E0B"
            title = get_text("high_risk")
            icon = "⚠️"
        elif risk_level == "medium":
            color = "#FBBF24"
            title = get_text("medium_risk")
            icon = "🟡"
        else:
            color = "#10B981"
            title = get_text("low_risk")
            icon = "✅"
        
        # Result box
        result_html = f"""
        <div style='background-color: {color}; padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px;'>
        <h2 style='text-align: center; margin: 0;'>{icon} {title}</h2>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        # Actions
        if risk_level == "emergency":
            st.markdown(f"### 🚑 {get_text('immediate_actions')}")
        else:
            st.markdown(f"### 📝 {get_text('recommended_actions')}")
        
        for action in actions:
            st.markdown(f"- {action}")

# ============================
# BOTTOM SECTION - TECHNICAL DETAILS
# ============================

st.markdown("---")

# Pipeline visualization
st.markdown(f"### 📊 {get_text('pipeline_explanation')}")

# Create pipeline diagram
pipeline_steps = [
    {"icon": "🎤", "name": "Voice Input", "desc": get_text("stt_explain")},
    {"icon": "🤖", "name": "AI Processing", "desc": get_text("symptom_explain")},
    {"icon": "⚕️", "name": "Medical Rules", "desc": get_text("rules_explain")},
    {"icon": "📋", "name": "Triage Output", "desc": "Urgency level + Actions"}
]

# Display pipeline
cols = st.columns(4)
for idx, step in enumerate(pipeline_steps):
    with cols[idx]:
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background-color: #F8FAFC; border-radius: 10px; border: 2px solid #E2E8F0;'>
        <h1>{step['icon']}</h1>
        <h4>{step['name']}</h4>
        <p style='font-size: 0.9em;'>{step['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Real-world deployment info
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📱 Real-World Deployment")
    st.markdown("""
    **Android App Features:**
    - Runs on ₹10,000-15,000 Android phones
    - 100% offline after initial setup
    - Supports 10+ Indian languages
    - 2-3 seconds processing time
    - < 500MB storage required
    
    **Target Devices:**
    - Samsung Galaxy A series
    - Redmi/POCO phones
    - Realme/Narzo series
    - Any Android 10+ device
    """)

with col_right:
    st.markdown("### 🔒 Privacy & Security")
    st.markdown("""
    **Data Protection:**
    - All processing happens on-device
    - No data sent to cloud servers
    - Compliant with India's DPDP Act 2023
    - Patient records stay on device
    
    **Security Measures:**
    - Encrypted local storage
    - No internet permissions required
    - Biometric app lock option
    - Automatic data wipe after 30 days
    """)

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 2])

with footer_col1:
    st.markdown("""
    **⚠️ Medical Disclaimer:**
    This tool assists but does not replace professional medical advice.
    Always consult a healthcare provider for medical decisions.
    """)

with footer_col2:
    st.markdown("""
    **Team CODENOVA**
    Snowfrost Hackathon 2026
    """)

with footer_col3:
    st.markdown("""
    **Contact:**
    📧 contact@codenova.ai
    🌐 www.codenova-ai.in
    """)

# ============================
# CUSTOM CSS
# ============================

st.markdown("""
<style>
    .stButton button {
        background: linear-gradient(45deg, #4F46E5, #7C3AED);
        color: white;
        font-weight: bold;
        font-size: 18px;
        padding: 15px 30px;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(45deg, #4338CA, #6D28D9);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stExpander {
        border: 2px solid #E2E8F0;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .css-1d391kg {
        padding: 20px;
    }
    
    h1, h2, h3 {
        color: #1E3A8A;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
    }
</style>
""", unsafe_allow_html=True)