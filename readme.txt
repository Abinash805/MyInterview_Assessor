# MyInterview.Assessor 🧿 

An AI-powered intelligence platform designed to bridge the gap between interviewers and interviewees by providing comprehensive, real-time assessment and predictive analytics for mock and live interviews. 

## 🚀 Core Capabilities
* **Dynamic Interview Setup:** Tailored interview generation based on specific roles (e.g., Senior Software Engineer, Product Manager) and difficulty levels.
* **Multimodal Behavioural Analysis:** Real-time tracking of 468 facial landmarks, posture alignment, and nervous habits via live webcam feed.
* **Speech & Vocal Diagnostics:** Tracks Words Per Minute (WPM), filler word frequency, and tone variation.
* **Predictive Scoring Engine:** Generates a selection probability score and compares it against dynamic, role-specific baseline targets.
* **Context Evaluation (STAR Method):** Evaluates candidate transcripts for depth, business impact, and relevance using an AI contextual engine.
* **Session History Tracking:** Long-term score progression tracking across multiple mock sessions.

## 📂 Project Structure (Phase 1 Prototype)
This iteration acts as a highly interactive "Wizard of Oz" prototype utilizing Streamlit's Session State to demonstrate the full application lifecycle and business logic prior to final ML integration.

* `app.py`: The main 5-page Streamlit dashboard (Home, Setup, Live Session, Analytics, History).
* `requirements.txt`: Project dependencies for UI and future ML models.
* `models/`: Placeholder directory for December's compiled model weights.

## 🛠️ How to Run the Application
1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt