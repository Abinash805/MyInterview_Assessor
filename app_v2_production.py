import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIGURATION & SETUP
# ============================================================================
st.set_page_config(
    page_title="MyInterview.Assessor | AI Interview Intelligence",
    layout="wide",
    page_icon="🧿",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL CSS STYLING
# ============================================================================
st.markdown("""
    <style>
    /* Root Variables */
    :root {
        --primary-dark: #0f1419;
        --secondary-dark: #1a1f2e;
        --accent-blue: #4facfe;
        --accent-green: #00ff41;
        --accent-red: #ff5555;
        --text-primary: #e0e0e0;
        --text-secondary: #a0a0a0;
        --border-color: #32324e;
    }
    
    /* Global Styling */
    body {
        background-color: #0f1419;
        color: #e0e0e0;
    }
    
    /* Main Container */
    .main {
        background-color: #0f1419;
    }
    
    /* Custom Card Styling */
    .premium-card {
        background-color: #1a1f2e;
        border: 1px solid #32324e;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border-left: 4px solid #4facfe;
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        border-left-color: #00ff41;
        box-shadow: 0 6px 16px rgba(79, 172, 254, 0.1);
    }
    
    /* Metric Container Override */
    div[data-testid="metric-container"] {
        background-color: #1a1f2e;
        border: 1px solid #32324e;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border-left: 4px solid #4facfe;
    }
    
    /* Terminal Log Box */
    .terminal-box {
        background-color: #0d1117;
        padding: 20px;
        border-radius: 8px;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        color: #00ff41;
        border: 1px solid #30363d;
        line-height: 1.8;
        font-size: 13px;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .terminal-box > div {
        margin: 4px 0;
    }
    
    .log-success { color: #00ff41; }
    .log-warning { color: #ffdd57; }
    .log-error { color: #ff5555; }
    .log-info { color: #4facfe; }
    
    /* Section Headers */
    .section-header {
        font-size: 28px;
        font-weight: 600;
        color: #e0e0e0;
        margin-bottom: 24px;
        padding-bottom: 12px;
        border-bottom: 2px solid #32324e;
    }
    
    /* Subsection Headers */
    .subsection-header {
        font-size: 16px;
        font-weight: 600;
        color: #4facfe;
        margin-top: 20px;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #4facfe;
        color: #0f1419;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #00ff41;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
    }
    
    /* Metric Value Highlighting */
    .metric-highlight {
        font-size: 36px;
        font-weight: 700;
        color: #4facfe;
        font-family: 'Monaco', monospace;
    }
    
    .metric-positive { color: #00ff41; }
    .metric-warning { color: #ffdd57; }
    .metric-negative { color: #ff5555; }
    
    /* Progress Bar Custom */
    .progress-container {
        background-color: #1a1f2e;
        border-radius: 8px;
        overflow: hidden;
        height: 24px;
        margin: 12px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4facfe, #00ff41);
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0f1419;
        font-weight: 600;
        font-size: 12px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f2e;
        border: 1px solid #32324e;
        border-radius: 8px;
        padding: 12px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4facfe;
        color: #0f1419;
    }
    
    /* Score Ring */
    .score-ring-container {
        text-align: center;
        padding: 30px;
    }
    
    .score-value {
        font-size: 64px;
        font-weight: 700;
        color: #4facfe;
        font-family: 'Monaco', monospace;
    }
    
    .score-label {
        font-size: 14px;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Comparison Badge */
    .comparison-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .comparison-positive {
        background-color: rgba(0, 255, 65, 0.2);
        color: #00ff41;
        border: 1px solid #00ff41;
    }
    
    .comparison-negative {
        background-color: rgba(255, 85, 85, 0.2);
        color: #ff5555;
        border: 1px solid #ff5555;
    }
    
    /* Sidebar Styling */
    .stSidebar {
        background-color: #1a1f2e;
        border-right: 1px solid #32324e;
    }
    
    /* Divider */
    .custom-divider {
        border-top: 2px solid #32324e;
        margin: 24px 0;
    }
    
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HARDCODED REALISTIC DATA STRUCTURES
# ============================================================================

# Session mock data
MOCK_SESSIONS = [
    {
        "id": "SES-20261001-001",
        "date": "Oct 1, 2026 @ 2:30 PM",
        "role": "Senior Software Engineer",
        "level": "Advanced",
        "score": 86,
        "target": 80,
        "status": "Passed ✓",
        "duration": "45 mins"
    },
    {
        "id": "SES-20260930-001",
        "date": "Sep 30, 2026 @ 3:15 PM",
        "role": "Product Manager",
        "level": "Intermediate",
        "score": 72,
        "target": 75,
        "status": "Borderline",
        "duration": "38 mins"
    },
    {
        "id": "SES-20260928-001",
        "date": "Sep 28, 2026 @ 10:00 AM",
        "role": "Senior Software Engineer",
        "level": "Advanced",
        "score": 78,
        "target": 80,
        "status": "Close",
        "duration": "42 mins"
    }
]

# Interview questions by role
INTERVIEW_QUESTIONS = {
    "Senior Software Engineer": [
        "Tell me about a time you had to pivot a project last minute. What was the impact?",
        "How do you approach system design? Walk me through your thought process.",
        "Describe your experience with leading technical teams. Any challenges?",
        "What's your approach to code review and maintaining quality standards?"
    ],
    "Product Manager": [
        "Tell me about a product you built from concept to launch.",
        "How do you prioritize features when everything seems urgent?",
        "Walk me through your metrics framework for measuring success.",
        "Describe a time you had to make a decision with incomplete data."
    ],
    "Data Scientist": [
        "Explain your approach to building a predictive model from scratch.",
        "How do you handle imbalanced datasets in classification problems?",
        "Tell me about the most impactful analysis you've done.",
        "How do you communicate technical findings to non-technical stakeholders?"
    ]
}

# Realistic behavioral metrics (hardcoded progression)
def get_behavioral_metrics():
    """Generate realistic behavioral metrics showing progression over interview"""
    base_time = np.arange(0, 31)
    
    # Eye Contact - starts low, improves with confidence
    eye_contact = 65 + (base_time * 0.5) + np.random.normal(0, 2, len(base_time))
    eye_contact = np.clip(eye_contact, 50, 95)
    
    # Confidence - steady increase
    confidence = 60 + (base_time * 0.8) + np.random.normal(0, 2.5, len(base_time))
    confidence = np.clip(confidence, 45, 98)
    
    # Posture Alignment - slight dip mid-interview, recovery
    posture = 75 + (base_time * 0.3) - ((base_time - 15)**2 / 100) + np.random.normal(0, 2, len(base_time))
    posture = np.clip(posture, 55, 95)
    
    return pd.DataFrame({
        'Time (min)': base_time,
        'Eye Contact (%)': eye_contact,
        'Vocal Confidence (%)': confidence,
        'Posture Alignment (%)': posture
    })

# Realistic speech metrics
SPEECH_METRICS = {
    "Pace": {"value": "135 WPM", "target": "120-150 WPM", "status": "optimal"},
    "Filler Words": {"value": "3 instances", "target": "<5 per min", "status": "excellent"},
    "Stuttering": {"value": "0 detected", "target": "Minimal", "status": "excellent"},
    "Tone Variation": {"value": "7.2 semitones", "target": "6-10", "status": "optimal"}
}

# Realistic transcript with evaluation
MOCK_TRANSCRIPT = {
    "question": "Tell me about a time you had to pivot a project last minute. What was the impact?",
    "response": """We were building a web application, and about a week before the scheduled launch, 
    our database architect discovered that our current architecture wouldn't scale to handle the projected 
    user load. Rather than delay the launch, I organized an emergency meeting with the team, reassigned roles 
    to expedite the migration, and we successfully transitioned to AWS managed services within 48 hours. 
    This decision prevented a potential outage and actually improved our performance metrics by 40%.""",
    "evaluation": {
        "depth": {"score": 9, "feedback": "Excellent STAR method application. Clear situation, task, action, result."},
        "relevance": {"score": 9, "feedback": "Directly answered the prompt with technical depth and business impact."},
        "communication": {"score": 8, "feedback": "Well-structured. Minor: reduce 'um' fillers at answer start."},
        "impact": {"score": 10, "feedback": "Quantifiable result (40% improvement) demonstrates leadership and business acumen."}
    }
}

# Environmental metrics
ENV_METRICS = {
    "Camera": {"status": "✓", "detail": "1080p @ 60fps", "color": "green"},
    "Audio": {"status": "✓", "detail": "Noise floor -45dB", "color": "green"},
    "Lighting": {"status": "✓", "detail": "Front-lit, 500+ lux", "color": "green"},
    "Network": {"status": "✓", "detail": "12ms latency, stable", "color": "green"},
    "Background": {"status": "✓", "detail": "Professional, neutral", "color": "green"}
}

# Improvement recommendations
IMPROVEMENT_AREAS = {
    "Technical Vocabulary Integration": 85,
    "Tone Variation & Pitch Control": 70,
    "Leadership Narrative Strength": 78,
    "System Design Communication": 82,
    "Reducing Filler Words": 65
}

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_progress" not in st.session_state:
    st.session_state.interview_progress = 0

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown('<div class="section-header" style="margin-top: 0;">📊 Navigation</div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Select Page",
        ["🏠 Home Dashboard", "🎯 New Interview", "📹 Live Session", "📈 Results & Analytics", "📋 Session History"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown('<div class="subsection-header">Quick Stats</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Score", "79%", "+6%")
    with col2:
        st.metric("Interviews", "12", "this month")
    
    st.markdown("---")
    st.markdown("**MyInterview.Assessor v2.0**  \nAI Interview Intelligence Platform")

# ============================================================================
# PAGE 1: HOME DASHBOARD
# ============================================================================
if page == "🏠 Home Dashboard":
    # Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #4facfe15 0%, #00ff4115 100%); 
                    border-radius: 16px; border: 1px solid #32324e; margin-bottom: 40px;">
            <h1 style="font-size: 42px; margin: 0; color: #e0e0e0;">🧿 MyInterview.Assessor</h1>
            <p style="font-size: 18px; color: #a0a0a0; margin: 12px 0 0 0;">
                AI-Powered Predictive Analytics & Mock Interview Trainer
            </p>
            <p style="font-size: 14px; color: #707080; margin: 12px 0 0 0;">
                Real-time behavioral analysis • Predictive scoring • Comprehensive feedback
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Core Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Avg Score", "79%", "+6% from baseline")
    with col2:
        st.metric("Interviews Completed", "12", "this month")
    with col3:
        st.metric("Positions Mastered", "3", "Advanced level")
    with col4:
        st.metric("Prediction Accuracy", "92%", "based on outcomes")
    
    st.markdown("---")
    
    # Value Proposition
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="subsection-header">Why MyInterview.Assessor?</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="premium-card">
            <p><strong>🎯 Predictive Scoring</strong><br>Know your real interview readiness before you apply. Our AI predicts selection probability with 92% accuracy.</p>
            </div>
            <div class="premium-card">
            <p><strong>🧠 Real-time Behavior Tracking</strong><br>Monitor 468 facial landmarks, vocal patterns, and body language in real-time to identify unconscious habits.</p>
            </div>
            <div class="premium-card">
            <p><strong>📊 Comprehensive Analytics</strong><br>Get detailed breakdowns of your performance across verbal, non-verbal, and environmental dimensions.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="subsection-header">Platform Features</div>', unsafe_allow_html=True)
        
        features = [
            ("🚀", "Mock Interview Trainer", "Practice with AI-generated interview questions tailored to your target role"),
            ("📹", "Live Session Monitoring", "Real-time feedback during interviews with Google Meet & Zoom integration"),
            ("📈", "Score Progression Tracking", "Visual analytics showing your improvement across all competency areas"),
            ("🎓", "Job-Role Customization", "Interview questions and rubrics aligned with actual job postings"),
            ("📥", "Downloadable Reports", "Professional assessment reports to track progress and share insights"),
            ("🔐", "Freemium Model", "Core features free • Premium tier for deep-dive analytics")
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
                <div class="premium-card" style="border-left-color: #00ff41;">
                <p><strong>{icon} {title}</strong><br><span style="font-size: 13px; color: #a0a0a0;">{desc}</span></p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Start New Interview Session", use_container_width=True, type="primary"):
            st.session_state.current_page = "interview_setup"
            st.switch_page("pages/interview_setup.py")

# ============================================================================
# PAGE 2: NEW INTERVIEW SETUP
# ============================================================================
elif page == "🎯 New Interview":
    st.markdown('<div class="section-header">Start New Interview Session</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subsection-header">Step 1: Select Role</div>', unsafe_allow_html=True)
        selected_role = st.selectbox(
            "Target Position",
            ["Senior Software Engineer", "Product Manager", "Data Scientist"],
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="subsection-header">Step 2: Difficulty Level</div>', unsafe_allow_html=True)
        difficulty = st.select_slider(
            "Interview Difficulty",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<div class="subsection-header">Baseline Target</div>', unsafe_allow_html=True)
        
        baseline_scores = {
            "Beginner": 70,
            "Intermediate": 75,
            "Advanced": 80,
            "Expert": 85
        }
        
        target_score = baseline_scores[difficulty]
        
        st.markdown(f"""
            <div class="premium-card">
            <div style="text-align: center;">
                <div class="score-value">{target_score}%</div>
                <div class="score-label">Target Score for {difficulty}</div>
                <p style="font-size: 13px; color: #a0a0a0; margin-top: 16px;">
                    Your AI model predicts you have an 87% chance of exceeding this target based on your recent performance.
                </p>
            </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interview preview
    st.markdown('<div class="subsection-header">Interview Preview</div>', unsafe_allow_html=True)
    
    questions = INTERVIEW_QUESTIONS[selected_role]
    preview_text = f"""
    <div class="premium-card">
    <p><strong>Role:</strong> {selected_role} ({difficulty})</p>
    <p><strong>Duration:</strong> ~40 mins | <strong>Questions:</strong> 4</p>
    <p><strong>Topics Covered:</strong></p>
    <ul style="color: #a0a0a0; font-size: 13px;">
    """
    
    for i, q in enumerate(questions[:2], 1):
        preview_text += f"<li>{q[:60]}...</li>"
    preview_text += "</ul></div>"
    
    st.markdown(preview_text, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Start Interview Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Begin Live Interview", use_container_width=True, type="primary"):
            st.session_state.current_session = {
                "role": selected_role,
                "difficulty": difficulty,
                "target_score": target_score,
                "questions": questions,
                "started_at": datetime.now()
            }
            st.session_state.interview_started = True
            st.switch_page("app")

# ============================================================================
# PAGE 3: LIVE INTERVIEW SESSION
# ============================================================================
elif page == "📹 Live Session":
    if not st.session_state.interview_started:
        st.warning("⚠️ No active interview session. Please start a new interview from the setup page.")
    else:
        session = st.session_state.current_session
        
        st.markdown(f'<div class="section-header">{session["role"]} Interview</div>', unsafe_allow_html=True)
        
        # Progress indicator
        progress = st.session_state.interview_progress
        st.progress(progress / 4, text=f"Question {min(progress + 1, 4)} of 4")
        
        col_camera, col_telemetry = st.columns([1.5, 1])
        
        with col_camera:
            st.markdown('<div class="subsection-header">Camera Feed & Question</div>', unsafe_allow_html=True)
            st.camera_input("Interview Camera")
            
            st.markdown('<div class="subsection-header">Current Question</div>', unsafe_allow_html=True)
            current_q = session["questions"][min(progress, 3)]
            st.markdown(f"""
                <div class="premium-card" style="border-left-color: #00ff41;">
                <p style="font-size: 16px; font-weight: 600; color: #e0e0e0; margin: 0 0 12px 0;">
                Q{min(progress + 1, 4)}: {current_q}
                </p>
                <p style="font-size: 12px; color: #a0a0a0;">
                Take your time. Aim for 2-3 minutes. Use the STAR method (Situation, Task, Action, Result).
                </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_telemetry:
            st.markdown('<div class="subsection-header">🧠 Real-time Telemetry</div>', unsafe_allow_html=True)
            
            # Live metrics
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Eye Contact", "78%", "+4%")
            with col_m2:
                st.metric("Confidence", "82%", "steady")
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Speech Pace", "138 WPM", "optimal")
            with col_m2:
                st.metric("Filler Words", "2", "good")
            
            st.markdown('<div class="subsection-header">System Logs</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="terminal-box">
                <div class="log-info">> [SYS] Interview session initialized</div>
                <div class="log-success">> [VIS] Face mesh locked. Tracking 468 points</div>
                <div class="log-success">> [VIS] Posture alignment: Optimal</div>
                <div class="log-info">> [AUD] Baseline established. Monitoring for filler words</div>
                <div class="log-warning">> [AUD] Detected micro-pause (2.3s) → processing context</div>
                <div class="log-success">> [NLP] Keywords extracted: 'leadership', 'scale', 'impact'</div>
                <div class="log-info">> [SYS] Generating real-time transcription...</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⏸️ Pause", use_container_width=True):
                st.info("Interview paused. Take your time to collect thoughts.")
        
        with col2:
            if st.button("✓ Next Question", use_container_width=True):
                if st.session_state.interview_progress < 3:
                    st.session_state.interview_progress += 1
                    st.rerun()
                else:
                    st.session_state.interview_progress = 4
                    st.success("All questions completed! Generating analysis...")
                    time.sleep(1)
                    st.switch_page("app")
        
        with col3:
            if st.button("🛑 End Interview", use_container_width=True):
                st.session_state.interview_started = False
                st.session_state.interview_progress = 0
                st.info("Interview ended. Redirecting to results...")
                time.sleep(1)
                st.switch_page("app")

# ============================================================================
# PAGE 4: RESULTS & ANALYTICS DASHBOARD
# ============================================================================
elif page == "📈 Results & Analytics":
    st.markdown('<div class="section-header">Post-Interview Analytics Report</div>', unsafe_allow_html=True)
    
    # Score Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Predictive Score", "86%", "+6% above target")
    with col2:
        st.metric("Speech Pace", "135 WPM", "Optimal")
    with col3:
        st.metric("Eye Contact", "82%", "Strong")
    with col4:
        st.metric("Context Match", "92%", "Excellent")
    
    st.markdown("---")
    
    # Tabs for detailed analysis
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Behavioral Dynamics", "🗣️ Speech Analysis", "🎯 Transcript Eval", "📈 Improvement Plan"])
    
    with tab1:
        st.markdown('<div class="subsection-header">Visual & Speech Dynamics Over Time</div>', unsafe_allow_html=True)
        
        chart_data = get_behavioral_metrics()
        st.line_chart(chart_data.set_index('Time (min)'), use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="subsection-header">Key Observations</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="premium-card">
                <p><strong style="color: #00ff41;">✓ Strong Opening</strong><br>Excellent posture and eye contact in first 5 minutes set positive tone.</p>
                <p><strong style="color: #00ff41;">✓ Consistent Confidence</strong><br>Vocal confidence increased steadily, peaking at 95% after question 2.</p>
                <p><strong style="color: #ffdd57;">⚠️ Mid-Interview Dip</strong><br>Slight posture slouch detected at minute 18, corrected within 2 minutes.</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="subsection-header">Gesture Analysis</div>', unsafe_allow_html=True)
            
            gesture_data = {
                "Hand Gestures (constructive)": 8,
                "Nervous Habits": 2,
                "Face Touches": 1,
                "Head Nods (engaged)": 12
            }
            
            for gesture, count in gesture_data.items():
                if "nervous" in gesture.lower() or "face" in gesture.lower():
                    color = "rgb(255, 85, 85)"
                else:
                    color = "rgb(0, 255, 65)"
                
                st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                    <p style="margin: 0 0 6px 0; font-size: 13px; color: #a0a0a0;">{gesture}</p>
                    <div class="progress-container">
                        <div class="progress-fill" style="width: {min(count * 10, 100)}%; background: {color};">{count}</div>
                    </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="subsection-header">Detailed Speech Metrics</div>', unsafe_allow_html=True)
        
        for metric_name, metric_data in SPEECH_METRICS.items():
            st.markdown(f"""
                <div class="premium-card">
                <p style="margin: 0; font-weight: 600; color: #e0e0e0;">{metric_name}</p>
                <p style="margin: 4px 0 8px 0; font-size: 24px; font-weight: 700; color: #4facfe; font-family: 'Monaco', monospace;">
                {metric_data['value']}
                </p>
                <p style="margin: 0; font-size: 13px; color: #a0a0a0;">
                Target: {metric_data['target']} • Status: <span style="color: #00ff41; font-weight: 600;">{metric_data['status'].upper()}</span>
                </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="subsection-header">Vocal Confidence Progression</div>', unsafe_allow_html=True)
        
        vocal_data = pd.DataFrame({
            'Minute': [0, 5, 10, 15, 20, 25, 30],
            'Confidence (%)': [62, 68, 75, 82, 88, 92, 95]
        })
        
        st.line_chart(vocal_data.set_index('Minute'), use_container_width=True)
    
    with tab3:
        st.markdown('<div class="subsection-header">Question Evaluation</div>', unsafe_allow_html=True)
        
        with st.expander(f"Q1: {MOCK_TRANSCRIPT['question']}", expanded=True):
            st.markdown("""
                **Your Response:**
            """)
            st.markdown(f"> {MOCK_TRANSCRIPT['response']}")
            
            st.markdown("---")
            st.markdown("**🤖 AI Contextual Analysis:**")
            
            eval_data = MOCK_TRANSCRIPT['evaluation']
            
            col1, col2 = st.columns(2)
            with col1:
                for metric, data in list(eval_data.items())[:2]:
                    st.markdown(f"""
                        <div class="premium-card">
                        <p style="margin: 0 0 8px 0; font-weight: 600; color: #4facfe;">{metric.replace('_', ' ').title()}</p>
                        <p style="margin: 0 0 8px 0; font-size: 24px; color: #00ff41;">
                        {data['score']}/10 <span style="font-size: 12px; color: #a0a0a0;">Score</span>
                        </p>
                        <p style="margin: 0; font-size: 12px; color: #a0a0a0;">{data['feedback']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                for metric, data in list(eval_data.items())[2:]:
                    st.markdown(f"""
                        <div class="premium-card">
                        <p style="margin: 0 0 8px 0; font-weight: 600; color: #4facfe;">{metric.replace('_', ' ').title()}</p>
                        <p style="margin: 0 0 8px 0; font-size: 24px; color: #00ff41;">
                        {data['score']}/10 <span style="font-size: 12px; color: #a0a0a0;">Score</span>
                        </p>
                        <p style="margin: 0; font-size: 12px; color: #a0a0a0;">{data['feedback']}</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        with st.expander("Q2: How do you approach system design?"):
            st.markdown("""
                **Status:** Analysis in progress...
                
                AI is currently processing your response for depth, relevance, and business impact.
            """)
    
    with tab4:
        st.markdown('<div class="subsection-header">Recommended Focus Areas</div>', unsafe_allow_html=True)
        
        for area, score in IMPROVEMENT_AREAS.items():
            color = "rgb(0, 255, 65)" if score >= 75 else "rgb(255, 221, 87)" if score >= 60 else "rgb(255, 85, 85)"
            
            st.markdown(f"""
                <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span style="color: #e0e0e0; font-weight: 500;">{area}</span>
                    <span style="color: {color}; font-weight: 600;">{score}%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-fill" style="width: {score}%; background: {color};"></div>
                </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="subsection-header">Next Steps</div>', unsafe_allow_html=True)
        
        recommendations = [
            ("📝", "Review Filler Words", "Practice removing 'um', 'uh', 'you know' through mirror exercises"),
            ("🎤", "Tone Variation Drills", "Record yourself answering questions with intentional pitch variation"),
            ("💪", "Leadership Narratives", "Collect 3-4 strong stories demonstrating team leadership impact"),
            ("🔧", "System Design Practice", "Work through design problems focusing on clarity and structure")
        ]
        
        for icon, title, desc in recommendations:
            st.markdown(f"""
                <div class="premium-card">
                <p style="margin: 0 0 6px 0;"><strong>{icon} {title}</strong></p>
                <p style="margin: 0; font-size: 12px; color: #a0a0a0;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export Options
    st.markdown('<div class="subsection-header">Export & Share</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📄 Download PDF Report", use_container_width=True):
            st.success("✓ Report generated! Downloading...")
    with col2:
        if st.button("📊 Export Data (CSV)", use_container_width=True):
            st.success("✓ Data exported successfully")
    with col3:
        if st.button("🔗 Share Results", use_container_width=True):
            st.info("Results link copied to clipboard")

# ============================================================================
# PAGE 5: SESSION HISTORY
# ============================================================================
elif page == "📋 Session History":
    st.markdown('<div class="section-header">Interview Session History</div>', unsafe_allow_html=True)
    
    # Summary Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sessions", "12", "this month")
    with col2:
        st.metric("Average Score", "79%", "+6% trend")
    with col3:
        st.metric("Roles Practiced", "3", "different roles")
    with col4:
        st.metric("Pass Rate", "75%", "vs 50% baseline")
    
    st.markdown("---")
    
    # Session Table
    st.markdown('<div class="subsection-header">Recent Sessions</div>', unsafe_allow_html=True)
    
    for session in MOCK_SESSIONS:
        status_color = "00ff41" if "Passed" in session["status"] else "ffdd57"
        
        st.markdown(f"""
            <div class="premium-card">
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 20px; align-items: center;">
                <div>
                    <p style="margin: 0 0 4px 0; font-weight: 600; font-size: 15px; color: #e0e0e0;">{session['role']}</p>
                    <p style="margin: 0; font-size: 12px; color: #a0a0a0;">
                    {session['date']} • {session['duration']}
                    </p>
                </div>
                <div style="text-align: center;">
                    <p style="margin: 0 0 4px 0; font-size: 24px; font-weight: 700; color: #4facfe; font-family: 'Monaco', monospace;">
                    {session['score']}%
                    </p>
                    <p style="margin: 0; font-size: 11px; color: #a0a0a0;">Target: {session['target']}%</p>
                </div>
                <div style="text-align: center;">
                    <p style="margin: 0; padding: 6px 12px; display: inline-block; background-color: rgba({status_color[0:2]}, {status_color[2:4]}, {status_color[4:6]}, 0.2); 
                    border-radius: 6px; color: #{status_color}; font-weight: 600; font-size: 12px;">
                    {session['status']}
                    </p>
                </div>
                <div style="text-align: right;">
                    <button style="background-color: #4facfe; color: #0f1419; border: none; padding: 8px 16px; border-radius: 6px; 
                    cursor: pointer; font-size: 12px; font-weight: 600;">View Details</button>
                </div>
            </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Score Trend Chart
    st.markdown('<div class="subsection-header">Score Progression</div>', unsafe_allow_html=True)
    
    trend_data = pd.DataFrame({
        'Session': ['Sep 28', 'Sep 30', 'Oct 1'],
        'Score': [78, 72, 86],
        'Target': [80, 75, 80]
    })
    
    st.line_chart(trend_data.set_index('Session'), use_container_width=True)
    
    st.markdown("---")
    
    # Role Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subsection-header">Performance by Role</div>', unsafe_allow_html=True)
        
        role_perf = pd.DataFrame({
            'Role': ['Senior Software Engineer', 'Product Manager', 'Data Scientist'],
            'Avg Score': [82, 74, 78],
            'Sessions': [5, 4, 3]
        })
        
        st.bar_chart(role_perf.set_index('Role')[['Avg Score']], use_container_width=True)
    
    with col2:
        st.markdown('<div class="subsection-header">Performance by Level</div>', unsafe_allow_html=True)
        
        level_perf = pd.DataFrame({
            'Level': ['Beginner', 'Intermediate', 'Advanced'],
            'Avg Score': [81, 78, 79]
        })
        
        st.bar_chart(level_perf.set_index('Level')[['Avg Score']], use_container_width=True)

