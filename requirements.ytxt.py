# PHASE 1: Core UI & State Management (Current)
# ==========================================
streamlit>=1.27.0
pandas>=2.1.1
numpy>=1.26.0

# ==========================================
# PHASE 2: ML & Computer Vision Models (December Release)
# ==========================================
opencv-python>=4.8.1
mediapipe>=0.10.5        # For 468-point facial mesh tracking
torch>=2.1.0             # PyTorch backend for NLP/Audio models
transformers>=4.34.0     # HuggingFace for transcript Context Engine
librosa>=0.10.1          # Audio extraction for pitch/tone variation
pyaudio>=0.2.13          # Real-time audio stream handling