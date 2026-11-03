# SkinInsight - AI-Powered Skin Analysis Platform

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Team Responsibilities](#team-responsibilities)
- [Development Workflow](#development-workflow)
- [API Configuration](#api-configuration)
- [Deployment](#deployment)
- [Documentation](#documentation)

## Project Overview

**SkinInsight** is an AI-powered skincare analysis platform that leverages Large Language Models (LLMs) to provide comprehensive skin quality assessments and personalized recommendations. The platform uses a prompt-driven architecture where the LLM handles all analysis, user simulation, and recommendation logic through structured outputs.

**Key Principle:** This project follows a **LLM-centric approach** - instead of building complex backend logic, we use carefully crafted prompts to make the LLM generate structured outputs that are directly displayed in the UI.

**Course:** COMP4145 - Professional Development 2  
**Platform:** Streamlit Web Application  
**API Endpoint:** https://genai.hkbu.edu.hk/api/v1/chat/completions  
**Model:** gpt-6-luna

## Features

### Core Features
1. **Skin Analysis** (Primary Feature)
   - Image upload and processing
   - AI-powered skin quality assessment
   - KPI scoring: Skin Cleanliness (0-10) and Skin Quality (0-10)
   - Detailed skin condition description
   - Age estimation

2. **Interactive Chatbot**
   - Conversational interface for skincare advice
   - Context-aware responses about skin conditions
   - Follow-up questions and recommendations

### Additional Features (3 Required Enhancements)
3. **Interactive Chatbot**
   - Conversational interface for skincare advice
   - Context-aware responses based on latest skin analysis
   - Chat history management
   - Quick question suggestions

4. **History Analytics Dashboard**
   - Visual timeline of past skin analyses
   - Progress tracking with charts (skin score trends)
   - Comparison view between analyses
   - Export to CSV functionality

5. **Personalized Product Recommendations**
   - AI-generated product suggestions based on skin analysis
   - Categorized recommendations (cleanser, moisturizer, treatment, etc.)
   - Ingredient explanations and usage instructions

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend/UI** | Streamlit | Web interface, no separate frontend needed |
| **Backend Logic** | Python 3.9+ | Application logic |
| **LLM API** | GPT-6-Luna via HKBU endpoint | All AI-powered analysis and generation |
| **Data Storage** | JSON files / Streamlit session_state | Simulated user data and history |
| **Visualization** | Plotly / Matplotlib | Charts and analytics |
| **Deployment** | Streamlit Community Cloud | Free hosting |
| **Version Control** | Git/GitHub | Code collaboration |

## Project Structure

```
COMP-4145-PD2/
│
├── app.py                          # Main Streamlit application entry point
│
├── modules/                        # Modular components
│   ├── __init__.py
│   ├── skin_analysis.py           # Core skin analysis logic (YOUR RESPONSIBILITY)
│   ├── chatbot.py                 # Chatbot interface (YOUR RESPONSIBILITY)
│   ├── auth.py                    # LLM-simulated authentication
│   ├── history.py                 # Analytics dashboard
│   ├── recommendations.py         # Product recommendation system
│   └── api_client.py              # LLM API communication wrapper
│
├── prompts/                       # Prompt templates for LLM
│   ├── skin_analysis_prompt.txt
│   ├── chatbot_prompt.txt
│   ├── auth_prompt.txt
│   ├── recommendation_prompt.txt
│   └── prompt_utils.py
│
├── config/                        # Configuration files
│   ├── config.py                  # API keys, model settings
│   └── ui_config.py               # UI styling and layout settings
│
├── data/                          # Local data storage
│   ├── users/                     # Simulated user profiles (JSON)
│   ├── analyses/                  # Stored analysis results (JSON)
│   └── products.json              # Product database for recommendations
│
├── assets/                        # Static assets
│   ├── images/                    # UI images, logos
│   └── styles/                    # Custom CSS
│
├── docs/                          # Project documentation
│   ├── ARCHITECTURE.md            # System architecture
│   ├── IMPLEMENTATION_PLAN.md     # Detailed implementation guide
│   ├── PROJECT_UPDATE_INITIAL.md  # Initial project update
│   ├── PROJECT_UPDATE_FINAL.md    # Final project update
│   └── VIBE_CODING_REFLECTION.md  # Reflection on vibe coding
│
├── tests/                         # Test files (optional)
│   └── test_api_client.py
│
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
├── .streamlit/                    # Streamlit config
│   └── config.toml
└── README.md                      # This file
```

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Git
- API key for GPT-6-Luna (provided by instructor)
- Internet connection

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd COMP-4145-PD2
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure API Key
Create a `.env` file in the project root (DO NOT commit this file):
```bash
API_KEY=your_api_key_here
API_ENDPOINT=https://genai.hkbu.edu.hk/api/v1/chat/completions
MODEL_NAME=gpt-6-luna
```

Or configure through Streamlit UI on first run (recommended for demo).

### Step 5: Initialize Data Directories
```bash
mkdir -p data/users data/analyses
```

### Step 6: Run Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Team Responsibilities

### Team Member 1 (You)
**Primary Responsibilities:**
- [ ] Core Skin Analysis module (`modules/skin_analysis.py`)
- [ ] Interactive Chatbot module (`modules/chatbot.py`)
- [ ] API client wrapper (`modules/api_client.py`)
- [ ] Skin analysis prompt engineering (`prompts/skin_analysis_prompt.txt`, `prompts/chatbot_prompt.txt`)
- [ ] Main app structure and navigation (`app.py`)
- [ ] Testing and integration

### Team Member 2 (Groupmate)
**Primary Responsibilities:**
- [ ] User Authentication module (`modules/auth.py`)
- [ ] History Analytics module (`modules/history.py`)
- [ ] Product Recommendations module (`modules/recommendations.py`)
- [ ] Data storage utilities (JSON handling)
- [ ] UI/UX polish and styling
- [ ] Documentation and deployment

### Shared Responsibilities
- [ ] Prompt engineering and optimization
- [ ] Project documentation
- [ ] Testing and debugging
- [ ] Final presentation preparation

## Development Workflow

### Phase 1: Setup (Week 1)
1. Initialize GitHub repository
2. Set up project structure
3. Install dependencies
4. Configure API access
5. Create initial Streamlit skeleton

### Phase 2: Core Development (Week 2-3)
1. **Team Member 1:**
   - Build skin analysis module
   - Implement chatbot interface
   - Test API integration

2. **Team Member 2:**
   - Build authentication system
   - Create history dashboard
   - Implement recommendations

### Phase 3: Integration (Week 4)
1. Integrate all modules into main app
2. Test end-to-end workflows
3. Fix bugs and edge cases

### Phase 4: Polish & Deploy (Week 5)
1. UI/UX improvements
2. Documentation completion
3. Deploy to Streamlit Cloud
4. Final testing

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: description of changes"

# Push to remote
git push origin feature/your-feature-name

# Create pull request on GitHub
# After review, merge to main
```

**Commit Message Convention:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` UI/formatting changes
- `refactor:` Code refactoring
- `test:` Adding tests

## API Configuration

### LLM API Details
- **Endpoint:** `https://genai.hkbu.edu.hk/api/v1/chat/completions`
- **Model:** `gpt-6-luna`
- **Authentication:** Bearer token in header
- **Request Format:** OpenAI-compatible

### Example API Call
```python
import requests

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-6-luna",
    "messages": [
        {"role": "system", "content": "You are a skincare expert."},
        {"role": "user", "content": "Analyze this skin image..."}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}

response = requests.post(
    "https://genai.hkbu.edu.hk/api/v1/chat/completions",
    headers=headers,
    json=payload
)

result = response.json()
```

### Rate Limits & Best Practices
- Implement exponential backoff for retries
- Cache responses when possible
- Use appropriate timeout values (30 seconds recommended)
- Handle API errors gracefully with user-friendly messages

## Deployment

### Streamlit Community Cloud (Recommended)
1. Push code to GitHub repository (must be public or have Streamlit access)
2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. Click "New app"
5. Select repository and branch
6. Set main file path: `app.py`
7. Add secrets in Streamlit dashboard:
   - `API_KEY`
   - `API_ENDPOINT`
   - `MODEL_NAME`
8. Deploy

### Alternative: Heroku
```bash
# Install Heroku CLI
heroku create skininsight-app
heroku config:set API_KEY=your_api_key_here
git push heroku main
```

### Alternative: Local Network Access
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## Documentation

All project documentation is in the `docs/` folder:

1. **ARCHITECTURE.md** - System design and component details
2. **IMPLEMENTATION_PLAN.md** - Step-by-step implementation guide
3. **PROJECT_UPDATE_INITIAL.md** - Initial project status (submit this)
4. **PROJECT_UPDATE_FINAL.md** - Final project status (submit this)
5. **VIBE_CODING_REFLECTION.md** - Discussion on AI-assisted coding

### Submission Requirements
- Combine relevant documentation into a **single Word file (max 4 pages)**
- Include:
  - Initial project update
  - Final project update
  - Vibe coding reflection
  - Link to deployed Streamlit app

## Quick Start Commands

```bash
# First time setup
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Run app
streamlit run app.py

# Run with specific port
streamlit run app.py --server.port 8502

# Clear Streamlit cache
streamlit cache clear
```

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'streamlit'`
```bash
# Solution: Activate virtual environment and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

**Issue:** API returns 401 Unauthorized
```bash
# Solution: Check API key in config
# Make sure .env file exists or key is entered in UI
```

**Issue:** Streamlit app won't start
```bash
# Solution: Check if port is already in use
lsof -ti:8501 | xargs kill -9
streamlit run app.py
```

**Issue:** Image upload fails
```bash
# Solution: Check file size (max 200MB) and format (jpg, png, jpeg)
```

## Support & Contact

- **Course:** COMP4145 - Professional Development 2
- **Instructor:** [Your Instructor Name]
- **Team Repository:** [GitHub URL]
- **Deployed App:** [Streamlit URL - to be added]

## License

This project is for educational purposes as part of COMP4145 course requirements.

---

**Last Updated:** 2026-11-03  
**Version:** 1.0  
**Status:** In Development
