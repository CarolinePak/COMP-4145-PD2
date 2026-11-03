# SkinInsight - Implementation Plan

## Table of Contents
- [Overview](#overview)
- [Development Phases](#development-phases)
- [Phase 1: Project Setup](#phase-1-project-setup)
	- [Step 1.1: Repository Initialization](#step-11-repository-initialization)
	- [Step 1.2: Directory Structure Creation](#step-12-directory-structure-creation)
	- [Step 1.3: Dependencies Installation](#step-13-dependencies-installation)
	- [Step 1.4: Configuration Setup](#step-14-configuration-setup)
	- [Step 1.5: Git Configuration](#step-15-git-configuration)
- [Phase 2: Core API Integration](#phase-2-core-api-integration)
	- [Step 2.1: API Client Module](#step-21-api-client-module)
	- [Step 2.2: Prompt Templates](#step-22-prompt-templates)
	- [Step 2.3: API Testing](#step-23-api-testing)
- [Phase 3: Skin Analysis Feature](#phase-3-skin-analysis-feature)
	- [Step 3.1: Basic UI Layout](#step-31-basic-ui-layout)
	- [Step 3.2: Image Upload Handler](#step-32-image-upload-handler)
	- [Step 3.3: LLM Integration](#step-33-llm-integration)
	- [Step 3.4: Response Parsing](#step-34-response-parsing)
	- [Step 3.5: Results Display](#step-35-results-display)
	- [Step 3.6: Data Persistence](#step-36-data-persistence)
- [Phase 4: Chatbot Feature](#phase-4-chatbot-feature)
	- [Step 4.1: Chat UI Components](#step-41-chat-ui-components)
	- [Step 4.2: Conversation History](#step-42-conversation-history)
	- [Step 4.3: Context Integration](#step-43-context-integration)
	- [Step 4.4: Quick Questions](#step-44-quick-questions)
- [Phase 5: User Authentication](#phase-5-user-authentication)
	- [Step 5.1: Profile Data Structure](#step-51-profile-data-structure)
	- [Step 5.2: Login/Registration Forms](#step-52-loginregistration-forms)
	- [Step 5.3: Session Management](#step-53-session-management)
	- [Step 5.4: Profile Display](#step-54-profile-display)
- [Phase 6: History Analytics](#phase-6-history-analytics)
	- [Step 6.1: Data Loading](#step-61-data-loading)
	- [Step 6.2: Statistics Calculations](#step-62-statistics-calculations)
	- [Step 6.3: Chart Visualization](#step-63-chart-visualization)
	- [Step 6.4: Timeline View](#step-64-timeline-view)
	- [Step 6.5: Export Functionality](#step-65-export-functionality)
- [Phase 7: Product Recommendations](#phase-7-product-recommendations)
	- [Step 7.1: Recommendation Prompt](#step-71-recommendation-prompt)
	- [Step 7.2: LLM Generation](#step-72-llm-generation)
	- [Step 7.3: Display Components](#step-73-display-components)
- [Phase 8: Integration & Testing](#phase-8-integration--testing)
	- [Step 8.1: Module Integration](#step-81-module-integration)
	- [Step 8.2: Navigation Flow](#step-82-navigation-flow)
	- [Step 8.3: Error Handling](#step-83-error-handling)
	- [Step 8.4: End-to-End Testing](#step-84-end-to-end-testing)
- [Phase 9: UI/UX Polish](#phase-9-uiux-polish)
	- [Step 9.1: Styling Consistency](#step-91-styling-consistency)
	- [Step 9.2: Loading States](#step-92-loading-states)
	- [Step 9.3: Responsive Design](#step-93-responsive-design)
	- [Step 9.4: User Feedback](#step-94-user-feedback)
- [Phase 10: Deployment](#phase-10-deployment)
	- [Step 10.1: Pre-Deployment Checklist](#step-101-pre-deployment-checklist)
	- [Step 10.2: Streamlit Cloud Setup](#step-102-streamlit-cloud-setup)
	- [Step 10.3: Secrets Configuration](#step-103-secrets-configuration)
	- [Step 10.4: Final Testing](#step-104-final-testing)
- [Phase 11: Documentation](#phase-11-documentation)
	- [Step 11.1: Code Documentation](#step-111-code-documentation)
	- [Step 11.2: Project Updates](#step-112-project-updates)
	- [Step 11.3: Submission Preparation](#step-113-submission-preparation)
- [Timeline Estimate](#timeline-estimate)
- [Team Task Distribution](#team-task-distribution)
- [Testing Checklist](#testing-checklist)
- [Common Issues & Solutions](#common-issues--solutions)

## Overview

This implementation plan provides a step-by-step guide to building the SkinInsight platform. Each phase is broken down into specific, actionable steps with clear deliverables. Follow this plan sequentially to ensure smooth development and integration.

**Development Approach:**
- Work in feature branches, merge to main when complete
- Test each module independently before integration
- Commit frequently with descriptive messages
- Use pair programming for complex features
- Review each other's code before merging

**Key Principles:**
1. **LLM-First**: Let the LLM handle logic through prompts
2. **Modular**: Each feature in its own module
3. **Testable**: Test components independently
4. **User-Friendly**: Focus on clear UI/UX

## Development Phases

### Phase 1: Project Setup
**Duration:** 1 day  
**Responsible:** Both team members  
**Goal:** Establish project foundation with proper structure and dependencies

#### Step 1.1: Repository Initialization

**Actions:**
1. Create GitHub repository named `COMP-4145-PD2` or `skininsight-app`
2. Initialize with README (basic placeholder)
3. Set repository to private or public as per course requirements
4. Add both team members as collaborators

**Commands:**
```bash
# On local machine
cd ~/Downloads/COMP-4145-PD2

# Initialize git (if not already done)
git init

# Create .gitignore first (see Step 1.5)
touch .gitignore

# Initial commit
git add .gitignore
git commit -m "Initial commit: Add .gitignore"

# Connect to remote
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

**Deliverables:**
- ✅ GitHub repository created
- ✅ Both team members have access
- ✅ Local repository initialized

#### Step 1.2: Directory Structure Creation

**Actions:**
1. Create all required directories
2. Add `__init__.py` files to make Python packages
3. Create placeholder files to preserve directory structure in git

**Commands:**
```bash
# Navigate to project root
cd ~/Downloads/COMP-4145-PD2

# Create directory structure
mkdir -p modules
mkdir -p prompts
mkdir -p config
mkdir -p data/users
mkdir -p data/analyses
mkdir -p assets/images
mkdir -p assets/styles
mkdir -p docs
mkdir -p .streamlit

# Create __init__.py files
touch modules/__init__.py
touch config/__init__.py

# Create .gitkeep files to preserve empty directories
touch data/users/.gitkeep
touch data/analyses/.gitkeep
touch assets/images/.gitkeep
touch assets/styles/.gitkeep

# Verify structure
tree -L 2
```

**Expected Structure:**
```
COMP-4145-PD2/
├── modules/
│   └── __init__.py
├── prompts/
├── config/
│   └── __init__.py
├── data/
│   ├── users/
│   │   └── .gitkeep
│   └── analyses/
│       └── .gitkeep
├── assets/
│   ├── images/
│   │   └── .gitkeep
│   └── styles/
│       └── .gitkeep
├── docs/
├── .streamlit/
└── .gitignore
```

**Deliverables:**
- ✅ All directories created
- ✅ Python packages properly initialized
- ✅ Structure verified

#### Step 1.3: Dependencies Installation

**Actions:**
1. Create `requirements.txt` with all necessary packages
2. Create virtual environment
3. Install dependencies
4. Verify installations

**Create `requirements.txt`:**
```txt
# Core Framework
streamlit==1.31.0

# API & HTTP
requests==2.31.0

# Data Processing
pandas==2.2.0
numpy==1.26.3

# Visualization
plotly==5.18.0
matplotlib==3.8.2

# Image Processing
Pillow==10.2.0

# Utilities
python-dotenv==1.0.0
uuid==1.30

# Date/Time
python-dateutil==2.8.2
```

**Commands:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list

# Test Streamlit installation
streamlit hello
# This should open a demo app in your browser
# Close it after verification (Ctrl+C in terminal)
```

**Verification:**
```bash
# Check Python version
python --version
# Should be 3.9 or higher

# Check Streamlit version
streamlit version
# Should show 1.31.0 or similar

# Test imports in Python
python -c "import streamlit, requests, pandas, plotly; print('All imports successful')"
```

**Deliverables:**
- ✅ `requirements.txt` created
- ✅ Virtual environment created
- ✅ All dependencies installed
- ✅ Installations verified

#### Step 1.4: Configuration Setup

**Actions:**
1. Create configuration module
2. Create Streamlit config file
3. Create environment template

**Create `config/config.py`:**
```python
# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEY = os.getenv("API_KEY", "")
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-6-luna")

# Application Configuration
APP_TITLE = "SkinInsight"
APP_ICON = "🔬"

# File Paths
DATA_DIR = "data"
USERS_DIR = os.path.join(DATA_DIR, "users")
ANALYSES_DIR = os.path.join(DATA_DIR, "analyses")

# API Settings
API_TIMEOUT = 30  # seconds
API_MAX_RETRIES = 3
API_MAX_TOKENS = 1500

# Image Settings
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]

# Session Settings
SESSION_TIMEOUT = 3600  # 1 hour in seconds
```

**Create `.streamlit/config.toml`:**
```toml
[theme]
primaryColor = "#FF6B9D"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 5
enableXsrfProtection = true
enableCORS = false

[browser]
gatherUsageStats = false
```

**Create `.env.example` (template for users):**
```bash
# API Configuration
API_KEY=your_api_key_here
API_ENDPOINT=https://genai.hkbu.edu.hk/api/v1/chat/completions
MODEL_NAME=gpt-6-luna
```

**Create actual `.env` file:**
```bash
# Copy template
cp .env.example .env

# Edit .env and add real API key
# (This file should NOT be committed to git)
```

**Deliverables:**
- ✅ `config/config.py` created
- ✅ `.streamlit/config.toml` created
- ✅ `.env.example` created
- ✅ `.env` created (with actual API key)

#### Step 1.5: Git Configuration

**Actions:**
1. Create comprehensive `.gitignore`
2. Commit initial structure
3. Create development branch

**Create `.gitignore`:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Environment Variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Data (exclude user data but keep structure)
data/users/*.json
data/analyses/**/*.json
!data/users/.gitkeep
!data/analyses/.gitkeep

# Logs
*.log

# Jupyter Notebooks (if used)
.ipynb_checkpoints/

# Test Coverage
htmlcov/
.coverage
.pytest_cache/

# Temporary files
*.tmp
temp/
```

**Commands:**
```bash
# Add all files
git add .

# Commit
git commit -m "feat: Initial project structure and configuration"

# Push to main
git push origin main

# Create development branch
git checkout -b develop
git push -u origin develop

# Go back to main
git checkout main
```

**Deliverables:**
- ✅ `.gitignore` created and committed
- ✅ Initial structure committed
- ✅ Development branch created

---

### Phase 2: Core API Integration
**Duration:** 1-2 days  
**Responsible:** Team Member 1 (You)  
**Goal:** Build and test the LLM API client wrapper

#### Step 2.1: API Client Module

**Actions:**
1. Create API client module with retry logic
2. Implement text-only and image+text methods
3. Add error handling

**Create `modules/api_client.py`:**

See ARCHITECTURE.md for complete implementation. Key points:

**Implementation Checklist:**
- [ ] Create `LLMClient` class
- [ ] Implement `__init__()` with configuration
- [ ] Implement `call_llm()` for text-only requests
- [ ] Implement `encode_image()` for base64 encoding
- [ ] Implement `call_with_image()` for image+text requests
- [ ] Add retry logic with exponential backoff
- [ ] Handle all HTTP status codes (200, 401, 429, 500)
- [ ] Add timeout handling
- [ ] Return standardized response format
- [ ] Create global `llm_client` instance

**Testing Commands:**
```python
# Test in Python interpreter
python

>>> from modules.api_client import llm_client
>>> 
>>> # Test text-only call
>>> result = llm_client.call_llm(
...     messages=[
...         {"role": "system", "content": "You are a helpful assistant."},
...         {"role": "user", "content": "Say hello!"}
...     ],
...     temperature=0.7,
...     max_tokens=50
... )
>>> 
>>> print(result)
>>> # Should see: {"success": True, "response": "Hello! ...", ...}
>>>
>>> # Test with image (use a sample image)
>>> with open("test_face.jpg", "rb") as f:
...     image_bytes = f.read()
>>> 
>>> result = llm_client.call_with_image(
...     system_prompt="You are an image analyzer.",
...     user_prompt="Describe this image.",
...     image_bytes=image_bytes
... )
>>> 
>>> print(result)
>>> # Should see: {"success": True, "response": "This image shows...", ...}
```

**Deliverables:**
- ✅ `modules/api_client.py` created
- ✅ All methods implemented
- ✅ Manual testing passed
- ✅ Committed to git

**Git Commands:**
```bash
git checkout -b feature/api-client
git add modules/api_client.py
git commit -m "feat: Add LLM API client with retry logic"
git push origin feature/api-client
# Create pull request on GitHub
# After review, merge to main
```

#### Step 2.2: Prompt Templates

**Actions:**
1. Create prompt utilities module
2. Create all prompt template files
3. Test prompt loading

**Create `prompts/prompt_utils.py`:**
```python
# prompts/prompt_utils.py

import os

PROMPTS_DIR = os.path.dirname(__file__)

def load_prompt(prompt_name: str) -> str:
    """
    Load prompt template from file.
    
    Args:
        prompt_name: Name of prompt file (without .txt extension)
    
    Returns:
        Prompt text content
    
    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    
    prompt_file = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")
    
    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


def save_prompt(prompt_name: str, content: str):
    """
    Save prompt template to file.
    
    Args:
        prompt_name: Name of prompt file (without .txt extension)
        content: Prompt text content
    """
    
    prompt_file = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")
    
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(content)


def list_prompts() -> list:
    """
    List all available prompt templates.
    
    Returns:
        List of prompt names (without .txt extension)
    """
    
    prompts = []
    
    for filename in os.listdir(PROMPTS_DIR):
        if filename.endswith('.txt'):
            prompts.append(filename[:-4])  # Remove .txt
    
    return sorted(prompts)
```

**Create prompt template files:**

See ARCHITECTURE.md for full prompt content. Create these files:

1. `prompts/skin_analysis_system.txt`
2. `prompts/skin_analysis_user.txt`
3. `prompts/chatbot_system.txt`
4. `prompts/recommendation_system.txt`

**Key Requirements for Prompts:**
- Clear role definition
- Explicit output format (JSON with exact structure)
- Use "CRITICAL: You MUST respond in valid JSON format"
- Provide example JSON template
- Include guidelines and constraints
- Specify what NOT to do

**Testing:**
```python
# Test prompt loading
python

>>> from prompts.prompt_utils import load_prompt, list_prompts
>>> 
>>> # List all prompts
>>> print(list_prompts())
>>> # Should show: ['chatbot_system', 'recommendation_system', 'skin_analysis_system', 'skin_analysis_user']
>>>
>>> # Load a prompt
>>> prompt = load_prompt("skin_analysis_system")
>>> print(prompt[:100])
>>> # Should show first 100 characters
```

**Deliverables:**
- ✅ `prompts/prompt_utils.py` created
- ✅ All 4 prompt template files created
- ✅ Prompts tested and loading correctly
- ✅ Committed to git

**Git Commands:**
```bash
git checkout -b feature/prompts
git add prompts/
git commit -m "feat: Add prompt templates and utilities"
git push origin feature/prompts
# Merge to main after review
```

#### Step 2.3: API Testing

**Actions:**
1. Create test script for API functionality
2. Test all API methods
3. Document API behavior

**Create `test_api.py` (in project root):**
```python
# test_api.py
# Simple test script to verify API functionality

import sys
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt

def test_text_call():
    """Test basic text-only API call."""
    print("Testing text-only API call...")
    
    result = llm_client.call_llm(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'API test successful!' and nothing else."}
        ],
        temperature=0.3,
        max_tokens=20
    )
    
    if result["success"]:
        print(f"✅ SUCCESS: {result['response']}")
        print(f"   Tokens used: {result['tokens_used']}")
        return True
    else:
        print(f"❌ FAILED: {result['error']}")
        return False


def test_image_call():
    """Test image+text API call."""
    print("\nTesting image+text API call...")
    print("Note: This requires a test image file named 'test_face.jpg'")
    
    try:
        with open("test_face.jpg", "rb") as f:
            image_bytes = f.read()
        
        result = llm_client.call_with_image(
            system_prompt="You are an image analyzer.",
            user_prompt="Briefly describe what you see in this image in one sentence.",
            image_bytes=image_bytes,
            temperature=0.3,
            max_tokens=100
        )
        
        if result["success"]:
            print(f"✅ SUCCESS: {result['response']}")
            print(f"   Tokens used: {result['tokens_used']}")
            return True
        else:
            print(f"❌ FAILED: {result['error']}")
            return False
    
    except FileNotFoundError:
        print("⚠️  SKIPPED: test_face.jpg not found")
        return None


def test_prompt_loading():
    """Test prompt template loading."""
    print("\nTesting prompt loading...")
    
    try:
        prompt = load_prompt("skin_analysis_system")
        print(f"✅ SUCCESS: Loaded prompt ({len(prompt)} characters)")
        print(f"   First 100 chars: {prompt[:100]}...")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_error_handling():
    """Test API error handling with invalid key."""
    print("\nTesting error handling (invalid API key)...")
    
    from modules.api_client import LLMClient
    
    # Create client with invalid key
    bad_client = LLMClient(api_key="invalid_key_12345")
    
    result = bad_client.call_llm(
        messages=[{"role": "user", "content": "test"}],
        max_tokens=10
    )
    
    if not result["success"] and "401" in str(result["error"]) or "Invalid API key" in str(result["error"]):
        print(f"✅ SUCCESS: Error handled correctly")
        print(f"   Error message: {result['error']}")
        return True
    else:
        print(f"❌ FAILED: Error not handled properly")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("API Integration Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Text Call", test_text_call()))
    results.append(("Image Call", test_image_call()))
    results.append(("Prompt Loading", test_prompt_loading()))
    results.append(("Error Handling", test_error_handling()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⚠️  SKIPPED"
        
        print(f"{test_name:20s} {status}")
    
    # Exit with appropriate code
    if all(r in [True, None] for r in [r[1] for r in results]):
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)
```

**Run Tests:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run test script
python test_api.py

# Expected output:
# ============================================================
# API Integration Tests
# ============================================================
# Testing text-only API call...
# ✅ SUCCESS: API test successful!
#    Tokens used: 25
# 
# Testing image+text API call...
# ⚠️  SKIPPED: test_face.jpg not found
# 
# Testing prompt loading...
# ✅ SUCCESS: Loaded prompt (1234 characters)
#    First 100 chars: You are an expert dermatologist and skincare analyst...
# 
# Testing error handling (invalid API key)...
# ✅ SUCCESS: Error handled correctly
#    Error message: Invalid API key. Please check your API key in settings.
# 
# ============================================================
# Test Summary
# ============================================================
# Text Call            ✅ PASSED
# Image Call           ⚠️  SKIPPED
# Prompt Loading       ✅ PASSED
# Error Handling       ✅ PASSED
# 
# 🎉 All tests passed!
```

**Deliverables:**
- ✅ Test script created
- ✅ All tests passing (except image test if no test image)
- ✅ API functionality verified
- ✅ Documented test results

---

### Phase 3: Skin Analysis Feature
**Duration:** 2-3 days  
**Responsible:** Team Member 1 (You)  
**Goal:** Build the core skin analysis feature with image upload and results display

#### Step 3.1: Basic UI Layout

**Actions:**
1. Create main app.py with navigation
2. Create skin_analysis module skeleton
3. Test basic rendering

**Create `app.py`:**
```python
# app.py

import streamlit as st
from config import config

# Import modules (will create these)
from modules import skin_analysis

# MUST be first Streamlit command
st.set_page_config(
    page_title=f"{config.APP_ICON} {config.APP_TITLE}",
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.analyses = []
        st.session_state.chat_history = []
        st.session_state.current_analysis = None
        st.session_state.recommendations = None

init_session_state()

# Sidebar navigation
with st.sidebar:
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.markdown("---")
    
    # Navigation menu
    page = st.radio(
        "Navigate to:",
        [
            "🏠 Skin Analysis",
            "💬 Chatbot",
            "👤 My Profile",
            "📊 History",
            "💄 Recommendations"
        ],
        index=0,
        label_visibility="visible"
    )
    
    st.markdown("---")
    
    # API Configuration
    with st.expander("⚙️ API Settings", expanded=False):
        api_key_input = st.text_input(
            "API Key",
            value=config.API_KEY if config.API_KEY else "",
            type="password",
            help="Enter your GPT-6-Luna API key"
        )
        
        if st.button("Save API Key"):
            config.API_KEY = api_key_input
            st.success("✅ API Key saved for this session!")
            st.info("Note: Key is only saved for current session")
    
    st.markdown("---")
    st.caption(f"Version 1.0 | COMP4145 PD2")

# Main content routing
if page == "🏠 Skin Analysis":
    skin_analysis.render()
elif page == "💬 Chatbot":
    st.title("💬 Chatbot")
    st.info("Coming soon...")
elif page == "👤 My Profile":
    st.title("👤 My Profile")
    st.info("Coming soon...")
elif page == "📊 History":
    st.title("📊 History")
    st.info("Coming soon...")
elif page == "💄 Recommendations":
    st.title("💄 Recommendations")
    st.info("Coming soon...")
```

**Create `modules/skin_analysis.py` (skeleton):**
```python
# modules/skin_analysis.py

import streamlit as st

def render():
    """
    Render the Skin Analysis page.
    """
    
    st.title("🔬 AI-Powered Skin Analysis")
    st.markdown("Upload a clear face photo for comprehensive skin quality assessment.")
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📸 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose a face image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear, well-lit photo of your face",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🔍 Analyze Skin", type="primary", use_container_width=True):
                st.info("Analysis functionality coming next...")
        else:
            st.info("👆 Please upload an image to begin analysis")
    
    with col2:
        st.subheader("📊 Analysis Results")
        st.info("Results will appear here after analysis")
```

**Test Basic UI:**
```bash
streamlit run app.py
```

**Verify:**
- Application launches without errors
- Sidebar navigation appears
- Skin Analysis page renders
- File uploader works
- Image displays after upload
- Other pages show "Coming soon"

**Deliverables:**
- ✅ `app.py` created with navigation
- ✅ `modules/skin_analysis.py` skeleton created
- ✅ Basic UI renders correctly
- ✅ Committed to git

**Git Commands:**
```bash
git checkout -b feature/skin-analysis-ui
git add app.py modules/skin_analysis.py
git commit -m "feat: Add basic UI layout for skin analysis"
git push origin feature/skin-analysis-ui
```

#### Step 3.2: Image Upload Handler

**Actions:**
1. Add image validation
2. Handle file size limits
3. Display image preview

**Update `modules/skin_analysis.py`:**

Add these functions before the `render()` function:

```python
def validate_image(uploaded_file) -> tuple:
    """
    Validate uploaded image file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    
    from config import config
    
    # Check file size
    if uploaded_file.size > config.MAX_IMAGE_SIZE:
        size_mb = uploaded_file.size / (1024 * 1024)
        max_mb = config.MAX_IMAGE_SIZE / (1024 * 1024)
        return False, f"File too large ({size_mb:.1f}MB). Maximum size: {max_mb:.1f}MB"
    
    # Check file type
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext not in config.ALLOWED_IMAGE_TYPES:
        return False, f"Invalid file type: {file_ext}. Allowed types: {', '.join(config.ALLOWED_IMAGE_TYPES)}"
    
    return True, None
```

**Update the `render()` function:**

Replace the file uploader section with:

```python
        uploaded_file = st.file_uploader(
            "Choose a face image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear, well-lit photo of your face",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Validate image
            is_valid, error_msg = validate_image(uploaded_file)
            
            if not is_valid:
                st.error(f"❌ {error_msg}")
            else:
                # Display image
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                
                # Show file info
                st.caption(f"📄 {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
                
                # Analyze button
                if st.button("🔍 Analyze Skin", type="primary", use_container_width=True):
                    analyze_skin(uploaded_file)
        else:
            # Show placeholder
            st.info("👆 Please upload an image to begin analysis")
            
            # Sample instructions
            with st.expander("📋 Photo Guidelines"):
                st.markdown("""
                For best results, ensure your photo:
                - Shows your full face clearly
                - Is well-lit (natural lighting preferred)
                - Is front-facing (not angled)
                - Has a clean face (no makeup for accurate analysis)
                - Is in focus (not blurry)
                """)
```

**Deliverables:**
- ✅ Image validation implemented
- ✅ File size and type checking working
- ✅ Error messages display correctly
- ✅ Photo guidelines added

#### Step 3.3: LLM Integration

**Actions:**
1. Create analyze_skin() function
2. Integrate API client
3. Add loading states

**Add to `modules/skin_analysis.py`:**

```python
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt
from datetime import datetime
import uuid
import json

def analyze_skin(uploaded_file):
    """
    Perform skin analysis using LLM.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    """
    
    # Check API key
    from config import config
    if not config.API_KEY:
        st.error("❌ API key not configured. Please add your API key in the sidebar settings.")
        return
    
    # Show loading state
    with st.spinner("🔬 Analyzing your skin... This may take 10-20 seconds."):
        
        # Read image bytes
        image_bytes = uploaded_file.read()
        
        # Load prompts
        try:
            system_prompt = load_prompt("skin_analysis_system")
            user_prompt = load_prompt("skin_analysis_user")
        except FileNotFoundError as e:
            st.error(f"❌ Prompt template error: {e}")
            return
        
        # Call LLM API
        result = llm_client.call_with_image(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image_bytes=image_bytes,
            temperature=0.3,  # Lower for consistent analysis
            max_tokens=1500
        )
        
        if result["success"]:
            # Parse response
            try:
                analysis_data = parse_analysis_response(result["response"])
                
                # Add metadata
                analysis_data["timestamp"] = datetime.now().isoformat()
                analysis_data["analysis_id"] = str(uuid.uuid4())
                analysis_data["image_name"] = uploaded_file.name
                
                # Store in session state
                st.session_state.current_analysis = analysis_data
                st.session_state.analyses.append(analysis_data)
                
                # Save to file
                save_analysis(analysis_data)
                
                st.success("✅ Analysis complete!")
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Failed to parse analysis results: {str(e)}")
                
                # Show raw response for debugging
                with st.expander("🐛 Debug Info - Raw Response"):
                    st.code(result["response"])
        
        else:
            st.error(f"❌ Analysis failed: {result['error']}")
```

**Deliverables:**
- ✅ analyze_skin() function implemented
- ✅ API integration working
- ✅ Loading spinner displays
- ✅ Error handling in place

#### Step 3.4: Response Parsing

**Actions:**
1. Create parse_analysis_response() function
2. Handle JSON extraction from markdown
3. Validate response format

**Add to `modules/skin_analysis.py`:**

```python
def parse_analysis_response(response_text: str) -> dict:
    """
    Parse LLM response into structured format.
    
    Expected LLM response:
    {
        "skin_cleanliness_score": 8,
        "skin_quality_score": 7,
        "age_estimate": 28,
        "skin_condition_description": "...",
        "concerns": ["..."],
        "recommendations": ["..."]
    }
    
    Args:
        response_text: Raw LLM response
    
    Returns:
        Parsed dict with structured data
    
    Raises:
        json.JSONDecodeError: If response is not valid JSON
        ValueError: If required fields are missing
    """
    
    # Clean response
    response_text = response_text.strip()
    
    # Remove markdown code blocks
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "", 1)
    if response_text.startswith("```"):
        response_text = response_text.replace("```", "", 1)
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]
    
    # Parse JSON
    data = json.loads(response_text.strip())
    
    # Validate required fields
    required_fields = [
        "skin_cleanliness_score",
        "skin_quality_score",
        "age_estimate",
        "skin_condition_description"
    ]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure scores are integers in range [0, 10]
    data["skin_cleanliness_score"] = int(max(0, min(10, data["skin_cleanliness_score"])))
    data["skin_quality_score"] = int(max(0, min(10, data["skin_quality_score"])))
    
    # Ensure age is reasonable
    data["age_estimate"] = int(max(0, min(120, data["age_estimate"])))
    
    # Ensure lists exist (even if empty)
    if "concerns" not in data:
        data["concerns"] = []
    if "recommendations" not in data:
        data["recommendations"] = []
    
    return data
```

**Deliverables:**
- ✅ parse_analysis_response() implemented
- ✅ Markdown stripping working
- ✅ Field validation in place
- ✅ Score clamping implemented

#### Step 3.5: Results Display

**Actions:**
1. Create display_results() function
2. Add KPI metrics and progress bars
3. Add action buttons

**Add to `modules/skin_analysis.py`:**

```python
def display_results(analysis: dict):
    """
    Display analysis results in structured UI.
    
    Args:
        analysis: Parsed analysis dict
    """
    
    # KPI Cards
    st.markdown("### 📈 Key Metrics")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        score = analysis['skin_cleanliness_score']
        st.metric(
            label="Skin Cleanliness",
            value=f"{score}/10",
            help="Overall cleanliness and clarity of skin"
        )
        # Color-coded emoji
        if score >= 8:
            st.success("Excellent! ✨")
        elif score >= 6:
            st.info("Good! 👍")
        else:
            st.warning("Needs improvement 💪")
    
    with metric_col2:
        score = analysis['skin_quality_score']
        st.metric(
            label="Skin Quality",
            value=f"{score}/10",
            help="Overall health and condition of skin"
        )
        if score >= 8:
            st.success("Excellent! ✨")
        elif score >= 6:
            st.info("Good! 👍")
        else:
            st.warning("Needs improvement 💪")
    
    with metric_col3:
        st.metric(
            label="Estimated Age",
            value=f"{analysis['age_estimate']} years",
            help="AI-estimated age based on skin condition"
        )
    
    # Progress bars
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Cleanliness Score**")
        st.progress(analysis['skin_cleanliness_score'] / 10)
    
    with col_b:
        st.markdown("**Quality Score**")
        st.progress(analysis['skin_quality_score'] / 10)
    
    # Detailed Description
    st.markdown("---")
    st.markdown("### 📝 Skin Condition Analysis")
    st.write(analysis['skin_condition_description'])
    
    # Concerns (if any)
    if analysis.get('concerns'):
        st.markdown("---")
        st.markdown("### ⚠️ Identified Concerns")
        for concern in analysis['concerns']:
            st.markdown(f"- {concern}")
    
    # Quick Recommendations (if any)
    if analysis.get('recommendations'):
        st.markdown("---")
        st.markdown("### 💡 Quick Recommendations")
        for rec in analysis['recommendations']:
            st.markdown(f"- {rec}")
    
    # Action Buttons
    st.markdown("---")
    st.markdown("### 🎯 Next Steps")
    
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("💬 Discuss with AI Assistant", use_container_width=True):
            st.info("Switch to 'Chatbot' page in the sidebar to discuss your results!")
    
    with btn_col2:
        if st.button("💄 Get Product Recommendations", use_container_width=True):
            st.info("Switch to 'Recommendations' page in the sidebar!")
    
    # Analysis metadata
    st.markdown("---")
    st.caption(f"Analysis ID: {analysis['analysis_id']}")
    st.caption(f"Performed: {datetime.fromisoformat(analysis['timestamp']).strftime('%B %d, %Y at %H:%M:%S')}")
```

**Update `render()` function to display results:**

In the second column (col2), replace the placeholder with:

```python
    with col2:
        st.subheader("📊 Analysis Results")
        
        # Display results if available
        if st.session_state.current_analysis:
            display_results(st.session_state.current_analysis)
        else:
            st.info("Results will appear here after analysis")
```

**Deliverables:**
- ✅ display_results() implemented
- ✅ KPI metrics display correctly
- ✅ Progress bars working
- ✅ All sections render properly

#### Step 3.6: Data Persistence

**Actions:**
1. Create save_analysis() function
2. Set up file storage
3. Test data saving

**Add to `modules/skin_analysis.py`:**

```python
import os

def save_analysis(analysis: dict):
    """
    Save analysis to JSON file for history tracking.
    
    Args:
        analysis: Analysis dict to save
    """
    
    from config import config
    
    # Get user ID (or use 'guest' if not logged in)
    user_id = st.session_state.get("user_id", "guest")
    
    # Create user directory
    user_dir = os.path.join(config.ANALYSES_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    
    # Save as JSON file
    filename = os.path.join(user_dir, f"{analysis['analysis_id']}.json")
    
    try:
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
    except Exception as e:
        st.warning(f"⚠️ Could not save analysis to file: {e}")
```

**Test Data Persistence:**

1. Run app: `streamlit run app.py`
2. Upload an image and analyze
3. Check that file was created: `ls data/analyses/guest/`
4. Verify JSON content: `cat data/analyses/guest/<analysis_id>.json`

**Deliverables:**
- ✅ save_analysis() implemented
- ✅ Directory creation working
- ✅ JSON files saving correctly
- ✅ Error handling in place

**Final Git Commit for Phase 3:**
```bash
git add modules/skin_analysis.py
git commit -m "feat: Complete skin analysis feature with LLM integration and results display"
git push origin feature/skin-analysis-ui
# Merge to main
```

---

### Phase 4: Chatbot Feature
**Duration:** 1-2 days  
**Responsible:** Team Member 1 (You)  
**Goal:** Build interactive chatbot with context from skin analysis

#### Step 4.1: Chat UI Components

**Actions:**
1. Create chatbot module
2. Implement chat message display
3. Add chat input

**Create `modules/chatbot.py`:**

```python
# modules/chatbot.py

import streamlit as st
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt
from datetime import datetime

def render():
    """
    Render the Chatbot page.
    """
    
    st.title("💬 SkinCare AI Assistant")
    st.markdown("Ask me anything about skincare, your analysis results, or get personalized advice!")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        # Show welcome message if no history
        if not st.session_state.chat_history:
            with st.chat_message("assistant"):
                st.markdown("👋 Hello! I'm your AI skincare assistant. How can I help you today?")
                
                # Show analysis summary if available
                if st.session_state.current_analysis:
                    st.info(f"I see you recently completed a skin analysis (Quality Score: {st.session_state.current_analysis['skin_quality_score']}/10). Feel free to ask me about your results!")
        
        # Display message history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(message["timestamp"])
    
    # Chat input
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        handle_user_message(user_input)
```

**Update `app.py` to import chatbot:**

```python
from modules import skin_analysis, chatbot

# ... in routing section:
elif page == "💬 Chatbot":
    chatbot.render()
```

**Deliverables:**
- ✅ chatbot.py created
- ✅ Chat UI renders
- ✅ Welcome message displays
- ✅ Chat input ready

#### Step 4.2: Conversation History

**Actions:**
1. Implement handle_user_message()
2. Store messages in session state
3. Display messages in real-time

**Add to `modules/chatbot.py`:**

```python
def handle_user_message(user_input: str):
    """
    Handle user's chat message.
    
    Args:
        user_input: User's message text
    """
    
    # Add user message to history
    user_message = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.chat_history.append(user_message)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
        st.caption(user_message["timestamp"])
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            bot_response = get_chatbot_response(user_input)
            st.markdown(bot_response)
            
            # Add bot message to history
            bot_message = {
                "role": "assistant",
                "content": bot_response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.chat_history.append(bot_message)
            st.caption(bot_message["timestamp"])
```

**Deliverables:**
- ✅ Message handling implemented
- ✅ History stored in session_state
- ✅ Messages display with timestamps

#### Step 4.3: Context Integration

**Actions:**
1. Implement get_chatbot_response()
2. Build context from analysis
3. Include chat history in LLM call

**Add to `modules/chatbot.py`:**

```python
def get_chatbot_response(user_input: str) -> str:
    """
    Get chatbot response from LLM.
    
    Args:
        user_input: User's question/message
    
    Returns:
        Bot's response text
    """
    
    from config import config
    
    # Check API key
    if not config.API_KEY:
        return "❌ API key not configured. Please add your API key in the sidebar settings."
    
    # Build context
    context = build_conversation_context()
    
    # Load system prompt
    try:
        system_prompt = load_prompt("chatbot_system")
    except FileNotFoundError:
        return "❌ Chatbot system prompt not found. Please ensure all prompt files are present."
    
    # Add context to system prompt
    if context:
        system_prompt += f"\n\n{context}"
    
    # Build messages array
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add recent chat history (last 10 messages to stay within token limits)
    recent_history = st.session_state.chat_history[-10:] if len(st.session_state.chat_history) > 10 else st.session_state.chat_history
    
    for msg in recent_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add current user input
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Call LLM
    result = llm_client.call_llm(
        messages=messages,
        temperature=0.7,
        max_tokens=800
    )
    
    if result["success"]:
        return result["response"]
    else:
        return f"❌ Sorry, I encountered an error: {result['error']}\n\nPlease try again or check your API settings."


def build_conversation_context() -> str:
    """
    Build context string from user's latest analysis.
    
    Returns:
        Formatted context string for LLM
    """
    
    if not st.session_state.current_analysis:
        return ""
    
    analysis = st.session_state.current_analysis
    
    context = f"""
=== USER'S LATEST SKIN ANALYSIS ===
(Use this information to provide personalized advice)

Analysis Date: {analysis.get('timestamp', 'N/A')}
Skin Cleanliness Score: {analysis.get('skin_cleanliness_score', 'N/A')}/10
Skin Quality Score: {analysis.get('skin_quality_score', 'N/A')}/10
Estimated Age: {analysis.get('age_estimate', 'N/A')} years
Condition: {analysis.get('skin_condition_description', 'N/A')}
"""
    
    if analysis.get('concerns'):
        context += f"\nIdentified Concerns: {', '.join(analysis['concerns'])}"
    
    context += "\n" + "=" * 40
    
    return context.strip()
```

**Deliverables:**
- ✅ get_chatbot_response() implemented
- ✅ Context building working
- ✅ Chat history included in API calls
- ✅ Responses contextually aware

#### Step 4.4: Quick Questions

**Actions:**
1. Add sidebar with quick questions
2. Add clear history button
3. Test full chatbot flow

**Add to `modules/chatbot.py` in `render()` function, after chat_input:**

```python
    # Sidebar quick actions
    with st.sidebar:
        st.markdown("### 💬 Chat Options")
        
        # Clear history button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        # Message count
        msg_count = len(st.session_state.chat_history)
        st.caption(f"Messages in history: {msg_count}")
        
        st.markdown("---")
        
        # Quick questions
        st.markdown("### 💡 Quick Questions")
        st.caption("Click to ask:")
        
        quick_questions = [
            "What products should I use for my skin type?",
            "How can I improve my skin quality score?",
            "Explain my latest analysis results",
            "What causes premature skin aging?",
            "Best skincare routine for beginners?"
        ]
        
        for i, question in enumerate(quick_questions):
            if st.button(question, key=f"quick_q_{i}", use_container_width=True):
                # Add question to chat
                handle_user_message(question)
                st.rerun()
```

**Test Chatbot:**

1. Run app
2. Complete a skin analysis first
3. Go to Chatbot page
4. Test conversation:
   - Ask about analysis results
   - Ask general skincare questions
   - Try quick questions
   - Test clear history
5. Verify context is used in responses

**Deliverables:**
- ✅ Quick questions sidebar added
- ✅ Clear history working
- ✅ Full chatbot flow tested
- ✅ Committed to git

**Git Commands:**
```bash
git checkout -b feature/chatbot
git add modules/chatbot.py app.py
git commit -m "feat: Add interactive chatbot with context-aware responses"
git push origin feature/chatbot
# Merge to main
```

---

### Phase 5: User Authentication
**Duration:** 1-2 days  
**Responsible:** Team Member 2  
**Goal:** Build simulated user authentication and profile management

*(Implementation details similar to ARCHITECTURE.md - create auth.py module with login/register forms, profile display, and JSON-based user storage)*

**Key Files to Create:**
- `modules/auth.py`
- Update `app.py` to import and route to auth module

**Testing Checklist:**
- [ ] Registration creates new user
- [ ] Login loads existing user
- [ ] Profile displays correctly
- [ ] Profile editing saves changes
- [ ] Logout clears session
- [ ] User data persists in JSON files

---

### Phase 6: History Analytics
**Duration:** 2 days  
**Responsible:** Team Member 2  
**Goal:** Build analytics dashboard with charts and timeline

*(Implementation details in ARCHITECTURE.md - create history.py with pandas DataFrame manipulation and Plotly charts)*

**Key Files to Create:**
- `modules/history.py`

**Testing Checklist:**
- [ ] Loads all analyses from session_state
- [ ] Displays summary metrics
- [ ] Charts render correctly
- [ ] Timeline shows all analyses
- [ ] Export to CSV works

---

### Phase 7: Product Recommendations
**Duration:** 1-2 days  
**Responsible:** Team Member 2  
**Goal:** Build LLM-powered product recommendation system

*(Implementation details in ARCHITECTURE.md - create recommendations.py)*

**Key Files to Create:**
- `modules/recommendations.py`
- `prompts/recommendation_system.txt`

**Testing Checklist:**
- [ ] Generates recommendations based on analysis
- [ ] Displays products by category
- [ ] Shows ingredients and usage
- [ ] Regenerate button works

---

### Phase 8: Integration & Testing
**Duration:** 2 days  
**Responsible:** Both team members  
**Goal:** Integrate all modules and test end-to-end flows

#### Step 8.1: Module Integration

**Actions:**
1. Ensure all modules imported in app.py
2. Test navigation between all pages
3. Verify session state persists across pages

**Update `app.py` with all imports:**

```python
from modules import skin_analysis, chatbot, auth, history, recommendations
```

**Update routing:**

```python
if page == "🏠 Skin Analysis":
    skin_analysis.render()
elif page == "💬 Chatbot":
    chatbot.render()
elif page == "👤 My Profile":
    auth.render()
elif page == "📊 History":
    history.render()
elif page == "💄 Recommendations":
    recommendations.render()
```

**Deliverables:**
- ✅ All modules integrated
- ✅ Navigation working smoothly
- ✅ No import errors

#### Step 8.2: Navigation Flow

**Actions:**
1. Test user journeys
2. Add navigation helpers between related pages
3. Verify data flows correctly

**Test These Flows:**

1. **New User Flow:**
   - Register on Profile page
   - Upload image on Skin Analysis
   - View results
   - Discuss in Chatbot
   - Get Recommendations
   - View History

2. **Returning User Flow:**
   - Login on Profile page
   - View History
   - Select past analysis
   - Get new recommendations

3. **Error Flow:**
   - Try analysis without API key
   - Try with invalid image
   - Handle API errors gracefully

**Deliverables:**
- ✅ All user flows tested
- ✅ Navigation intuitive
- ✅ Data persists correctly

#### Step 8.3: Error Handling

**Actions:**
1. Test all error scenarios
2. Ensure user-friendly error messages
3. Add fallback behaviors

**Error Scenarios to Test:**

1. **API Errors:**
   - Invalid API key → Show clear message in sidebar
   - Rate limit → Show retry message
   - Timeout → Show connection error
   - Server error → Show generic error

2. **Data Errors:**
   - Missing prompt files → Show file error
   - Corrupted JSON → Handle gracefully
   - Missing analysis → Show placeholder

3. **Input Errors:**
   - Image too large → Show size limit
   - Wrong file type → Show allowed types
   - Empty inputs → Show validation messages

**Deliverables:**
- ✅ All error scenarios tested
- ✅ Error messages user-friendly
- ✅ No unhandled exceptions

#### Step 8.4: End-to-End Testing

**Actions:**
1. Complete full user journey
2. Test on different browsers
3. Document any issues

**Full Test Script:**

```
1. Open app in Chrome
2. Register new account (username: test_user_1)
3. Upload test image (face photo)
4. Verify analysis completes
5. Check all KPIs display
6. Go to Chatbot
7. Ask 3 questions
8. Verify context is used
9. Go to Recommendations
10. Generate recommendations
11. Verify products display
12. Go to History
13. Verify analysis appears
14. Check charts render
15. Export CSV
16. Go to Profile
17. Edit profile
18. Logout
19. Login again
20. Verify data persisted

Repeat in Firefox and Safari
```

**Deliverables:**
- ✅ Full E2E test passed
- ✅ Tested in multiple browsers
- ✅ Issues documented and fixed

---

### Phase 9: UI/UX Polish
**Duration:** 1-2 days  
**Responsible:** Both team members  
**Goal:** Improve visual design and user experience

#### Step 9.1: Styling Consistency

**Actions:**
1. Ensure consistent spacing and layout
2. Standardize button styles
3. Add visual hierarchy

**Create `assets/styles/custom.css` (optional):**

```css
/* Custom CSS for SkinInsight */

/* Ensure consistent spacing */
.stButton > button {
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Progress bars */
.stProgress > div > div {
    border-radius: 10px;
}

/* Metrics */
.stMetric {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
}
```

**Load CSS in app.py:**

```python
# Load custom CSS (optional)
def load_css():
    try:
        with open("assets/styles/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()
```

**Deliverables:**
- ✅ Consistent styling across pages
- ✅ Visual hierarchy clear
- ✅ Professional appearance

#### Step 9.2: Loading States

**Actions:**
1. Ensure all API calls show spinners
2. Disable buttons during processing
3. Add progress indicators

**Verify Loading States:**

- [ ] Skin analysis shows spinner
- [ ] Chatbot shows "Thinking..."
- [ ] Recommendations show generation progress
- [ ] Buttons disabled during API calls

#### Step 9.3: Responsive Design

**Actions:**
1. Test on different screen sizes
2. Ensure mobile-friendly
3. Adjust layouts as needed

**Test Resolutions:**
- Desktop: 1920x1080
- Laptop: 1366x768
- Tablet: 768x1024
- Mobile: 375x667

#### Step 9.4: User Feedback

**Actions:**
1. Add success/error messages
2. Add tooltips and help text
3. Improve instructions

**Feedback Elements:**
- ✅ Success messages after actions
- ✅ Error messages when things fail
- ✅ Loading indicators during waits
- ✅ Help text for complex features
- ✅ Instructions for first-time users

---

### Phase 10: Deployment
**Duration:** 1 day  
**Responsible:** Both team members  
**Goal:** Deploy application to Streamlit Cloud

#### Step 10.1: Pre-Deployment Checklist

**Actions:**
1. Test locally one final time
2. Ensure all files committed
3. Update documentation

**Checklist:**
- [ ] All features working
- [ ] No hardcoded API keys
- [ ] requirements.txt up to date
- [ ] README updated
- [ ] .gitignore correct
- [ ] No sensitive data in repo

#### Step 10.2: Streamlit Cloud Setup

**Actions:**
1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Configure app settings

**Steps:**

1. **Push to GitHub:**
```bash
git checkout main
git pull origin main
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `COMP-4145-PD2`
   - Branch: `main`
   - Main file: `app.py`
   - Click "Deploy"

3. **App Settings:**
   - App URL: Choose custom URL (e.g., `skininsight-comp4145`)
   - Python version: 3.9
   - Advanced: None needed

#### Step 10.3: Secrets Configuration

**Actions:**
1. Add API key to Streamlit secrets
2. Update config.py to read from secrets
3. Test deployed app

**In Streamlit Cloud Dashboard:**

1. Click on your app
2. Go to "Settings" → "Secrets"
3. Add:
```toml
API_KEY = "your_actual_api_key_here"
API_ENDPOINT = "https://genai.hkbu.edu.hk/api/v1/chat/completions"
MODEL_NAME = "gpt-6-luna"
```

**Update `config/config.py` to handle Streamlit secrets:**

```python
# Try to load from Streamlit secrets first
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        API_KEY = st.secrets.get("API_KEY", os.getenv("API_KEY", ""))
        API_ENDPOINT = st.secrets.get("API_ENDPOINT", os.getenv("API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions"))
        MODEL_NAME = st.secrets.get("MODEL_NAME", os.getenv("MODEL_NAME", "gpt-6-luna"))
    else:
        # Fall back to environment variables
        API_KEY = os.getenv("API_KEY", "")
        API_ENDPOINT = os.getenv("API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions")
        MODEL_NAME = os.getenv("MODEL_NAME", "gpt-6-luna")
except:
    # Fall back to environment variables
    API_KEY = os.getenv("API_KEY", "")
    API_ENDPOINT = os.getenv("API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-6-luna")
```

#### Step 10.4: Final Testing

**Actions:**
1. Test deployed app
2. Verify all features work in cloud
3. Note deployment URL

**Test on Deployed App:**
- [ ] App loads correctly
- [ ] API calls work
- [ ] File uploads work
- [ ] Data persists within session
- [ ] All pages accessible
- [ ] No errors in logs

**Copy Deployment URL:**
- Format: `https://<app-name>.streamlit.app/`
- Save this for documentation

**Deliverables:**
- ✅ App deployed successfully
- ✅ All features working in production
- ✅ URL documented

---

### Phase 11: Documentation
**Duration:** 1-2 days  
**Responsible:** Both team members  
**Goal:** Complete all project documentation for submission

#### Step 11.1: Code Documentation

**Actions:**
1. Add docstrings to all functions
2. Add inline comments where needed
3. Update README with deployment URL

**Verify:**
- [ ] All functions have docstrings
- [ ] Complex logic has comments
- [ ] README includes deployment URL

#### Step 11.2: Project Updates

**Actions:**
1. Complete PROJECT_UPDATE_INITIAL.md
2. Complete PROJECT_UPDATE_FINAL.md
3. Complete VIBE_CODING_REFLECTION.md

*(Will create these documents next)*

#### Step 11.3: Submission Preparation

**Actions:**
1. Combine documentation into Word file
2. Add diagrams/screenshots
3. Ensure under 4 pages
4. Submit

**Word Document Structure:**

```
Title: SkinInsight - AI-Powered Skin Analysis Platform
Team: [Your Names]
Course: COMP4145 PD2

1. Initial Project Update (0.5 page)
2. Final Project Update (1.5 pages)
3. Vibe Coding Reflection (1 page)
4. Deployment Link & Architecture Diagram (0.5 page)
5. References (0.5 page)

Total: 4 pages
```

---

## Timeline Estimate

| Phase | Duration | Team Member | Week |
|-------|----------|-------------|------|
| Phase 1: Setup | 1 day | Both | Week 1 |
| Phase 2: API Integration | 1-2 days | TM1 | Week 1-2 |
| Phase 3: Skin Analysis | 2-3 days | TM1 | Week 2 |
| Phase 4: Chatbot | 1-2 days | TM1 | Week 2-3 |
| Phase 5: Authentication | 1-2 days | TM2 | Week 2-3 |
| Phase 6: History | 2 days | TM2 | Week 3 |
| Phase 7: Recommendations | 1-2 days | TM2 | Week 3-4 |
| Phase 8: Integration | 2 days | Both | Week 4 |
| Phase 9: UI Polish | 1-2 days | Both | Week 4 |
| Phase 10: Deployment | 1 day | Both | Week 5 |
| Phase 11: Documentation | 1-2 days | Both | Week 5 |

**Total: ~4-5 weeks**

## Team Task Distribution

### Team Member 1 (You)
**Core Responsibilities:**
- ✅ Phase 1: Project setup (shared)
- ✅ Phase 2: API client module
- ✅ Phase 3: Skin analysis feature
- ✅ Phase 4: Chatbot feature
- ✅ Phase 8: Integration testing (shared)
- ✅ Phase 10: Deployment (shared)

**Estimated Effort:** ~50% of development

### Team Member 2 (Groupmate)
**Core Responsibilities:**
- ✅ Phase 1: Project setup (shared)
- ✅ Phase 5: User authentication
- ✅ Phase 6: History analytics
- ✅ Phase 7: Product recommendations
- ✅ Phase 9: UI/UX polish (shared)
- ✅ Phase 11: Documentation (shared)

**Estimated Effort:** ~50% of development

## Testing Checklist

### Functional Testing
- [ ] Image upload and validation
- [ ] Skin analysis with LLM
- [ ] Results display correctly
- [ ] Chatbot conversation
- [ ] Context awareness in chat
- [ ] User registration
- [ ] User login
- [ ] Profile editing
- [ ] History display
- [ ] Charts rendering
- [ ] Recommendations generation
- [ ] Data persistence
- [ ] Navigation between pages
- [ ] Session state management

### Error Handling
- [ ] Invalid API key
- [ ] Network timeout
- [ ] Invalid image format
- [ ] Image too large
- [ ] Missing prompt files
- [ ] Corrupted JSON
- [ ] API rate limiting
- [ ] Empty inputs

### Performance
- [ ] API response time < 30s
- [ ] UI responsive
- [ ] No memory leaks
- [ ] Charts load quickly
- [ ] Image upload fast

### Browser Compatibility
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Deployment
- [ ] Runs on Streamlit Cloud
- [ ] Secrets configured
- [ ] No errors in logs
- [ ] Public URL accessible

## Common Issues & Solutions

### Issue 1: API Key Not Working
**Symptom:** 401 Unauthorized error

**Solutions:**
1. Check API key in sidebar settings
2. Verify key in .env file
3. Check Streamlit secrets configuration
4. Ensure no extra spaces in key

### Issue 2: Image Upload Fails
**Symptom:** Error when uploading image

**Solutions:**
1. Check file size (max 5MB)
2. Verify file format (jpg, png only)
3. Check image is not corrupted
4. Try different image

### Issue 3: LLM Returns Non-JSON
**Symptom:** JSON parsing error

**Solutions:**
1. Check prompt template formatting
2. Add more explicit JSON instructions in prompt
3. Increase max_tokens if response cut off
4. Show raw response for debugging

### Issue 4: Session State Not Persisting
**Symptom:** Data lost when switching pages

**Solutions:**
1. Ensure using st.session_state correctly
2. Don't use st.rerun() unnecessarily
3. Check initialization in app.py
4. Verify no conflicts in session keys

### Issue 5: Deployment Fails
**Symptom:** App doesn't load on Streamlit Cloud

**Solutions:**
1. Check requirements.txt is complete
2. Verify Python version compatibility
3. Check logs in Streamlit dashboard
4. Ensure all imports are available
5. Test locally first with exact requirements.txt

### Issue 6: Charts Not Rendering
**Symptom:** Plotly charts don't display

**Solutions:**
1. Check plotly version in requirements.txt
2. Verify DataFrame has data
3. Check column names match
4. Test chart code in isolation

### Issue 7: Slow Performance
**Symptom:** App is sluggish

**Solutions:**
1. Reduce chat history context (last 10 messages)
2. Optimize image size before encoding
3. Use st.cache_data for expensive operations
4. Minimize st.rerun() calls

---

**Last Updated:** 2026-11-03  
**Version:** 1.0  
**Status:** Ready for Implementation
