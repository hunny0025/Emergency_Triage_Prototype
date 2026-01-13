🆘 OFFLINE EMERGENCY TRIAGE AGENT

Offline Emergency Triage Agent is a 100% offline, AI-powered medical triage system designed to assist during emergencies when internet connectivity is unavailable. In situations such as natural disasters, rural or remote areas, or network outages, the application provides immediate, on-device medical triage using voice-based symptom input.

The system prioritizes speed, privacy, and reliability, ensuring critical health guidance is available anytime, anywhere.

✨ Key Features

🔒 100% Offline Operation
All processing happens locally on the device — no cloud, no internet, no APIs.

🎤 Voice-Based Symptom Input
Upload or record audio files (MP3/WAV/M4A) describing symptoms.

⚡ Instant Triage Assessment
Provides immediate risk classification (Low / Medium / High).

🛡️ Complete Privacy
Medical data never leaves the device. Zero data transmission.

✈️ Airplane Mode Ready
Fully functional in airplane mode or isolated environments.

🎯 How It Works

Voice Input
The user uploads or records an audio describing symptoms.

Offline Processing
On-device AI converts speech to text and extracts medical symptoms.

Triage Engine
Symptoms are analyzed using local medical logic and AI models.

Result Output
The system returns an emergency-level assessment with guidance.

📱 Usage
Voice Input

Click “Browse files” or drag-and-drop an audio file (MP3/WAV/M4A)

Maximum file size: 200MB

Select Airplane Mode (100% Offline) demo to simulate no-internet usage

Sample Audio (for testing)

You may test the system using short symptom recordings such as:

“I have chest pain and shortness of breath that started an hour ago.”

🔧 Technical Specifications

Platform: Cross-platform

Prototype: Streamlit (Python)

Target Deployment: Android (on-device)

AI Models:

Offline Speech-to-Text (quantized Whisper)

Lightweight triage logic / rule-based inference

Supported Audio Formats: MP3, WAV, M4A

Maximum File Size: 200MB per file

Connectivity Requirement: None

🏗️ System Architecture

Edge AI Processing:
Quantized models optimized for local inference

Audio Processing Pipeline:
Speech-to-text → symptom extraction → triage logic

Medical Triage Engine:
Risk stratification aligned with standard emergency triage principles

UI Layer:
User-friendly interface designed for quick emergency interaction

🔒 Privacy & Security

✅ No internet usage

✅ No cloud storage

✅ No external APIs

✅ No data logging

All audio and medical information is processed locally in memory and is not permanently stored.

Designed with HIPAA/GDPR-aligned principles for offline applications.

🚨 Emergency Disclaimer

IMPORTANT NOTICE

This tool is intended for triage assistance only and does not replace professional medical advice, diagnosis, or treatment.

In life-threatening emergencies:

Call your local emergency number immediately (e.g., 112 / 911)

Seek in-person medical attention

Use this tool only as supplementary support

🚀 Getting Started
For Users

Launch the application

Upload a symptom audio file

Receive instant offline triage results

For Developers
git clone https://github.com/hunny0025/Emergency_Triage_Prototype.git
cd Emergency_Triage_Prototype
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

🤝 Contributing

Contributions are welcome to improve offline emergency healthcare technology.

Fork the repository

Create a feature branch

Submit a pull request

Open issues for bugs or enhancements

📄 License

This project is licensed under the MIT License.
See the LICENSE file for more details.

📞 Support & Contact

Emergency: Always contact local emergency services first

Technical Support: Open an issue on GitHub

Medical Questions: Consult a qualified healthcare professional

⚠️ Final Note

In any medical emergency, professional medical help should always be your first response.
Offline Emergency Triage Agent is designed to assist when immediate professional care is not accessible.
