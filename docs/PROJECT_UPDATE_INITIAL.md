# SkinInsight - Initial Project Update

## Table of Contents
- [Project Overview](#project-overview)
- [Team Information](#team-information)
- [Project Objectives](#project-objectives)
- [Proposed Features](#proposed-features)
- [Technical Approach](#technical-approach)
- [Architecture Design](#architecture-design)
- [Development Plan](#development-plan)
- [Risk Assessment](#risk-assessment)
- [Expected Outcomes](#expected-outcomes)

## Project Overview

**Project Name:** SkinInsight  
**Course:** COMP4145 - Professional Development 2  
**Date:** November 2026  
**Status:** Planning & Initial Development Phase

SkinInsight is an AI-powered skincare analysis platform designed to help users understand their skin condition and receive personalized skincare recommendations. The platform leverages Large Language Models (specifically GPT-6-Luna) to provide comprehensive skin quality assessments without requiring traditional machine learning model training or fine-tuning.

## Team Information

**Team Size:** 2 members

**Team Member Roles:**

| Member | Primary Responsibilities |
|--------|-------------------------|
| Member 1 | Core skin analysis module, chatbot functionality, API integration, main application structure |
| Member 2 | User authentication, history analytics dashboard, product recommendations, UI/UX design |

**Collaboration Approach:**
- Version control via GitHub with feature branch workflow
- Regular sync meetings (2-3 times per week)
- Code reviews before merging to main branch
- Shared documentation in Google Docs for real-time collaboration

## Project Objectives

### Primary Objective
Develop an enhanced skincare analysis application that goes beyond basic image analysis to provide a comprehensive user experience including personalized recommendations, historical tracking, and interactive consultation.

### Learning Objectives
1. Apply AI/LLM integration in a practical web application
2. Practice collaborative software development with version control
3. Implement user-centric design principles
4. Gain experience with cloud deployment (Streamlit Cloud)
5. Document and communicate technical decisions effectively

### Business Value
- Help users make informed skincare decisions
- Provide accessible skincare consultation without requiring in-person dermatologist visits
- Track skin health progress over time
- Recommend appropriate products based on individual needs

## Proposed Features

### Core Feature (Requirement)
**1. Skin Analysis**
- Image upload functionality
- AI-powered skin assessment using GPT-6-Luna
- Key Performance Indicators (KPIs):
  - Skin Cleanliness Score (0-10)
  - Skin Quality Score (0-10)
  - Age Estimation
  - Detailed condition description

### Three Additional Features (Project Requirements)

**2. Interactive Chatbot** *(Additional Feature #1)*
- Conversational interface for skincare advice and follow-up questions
- Context-aware responses based on user's latest skin analysis
- Chat history management
- Quick question suggestions
- Natural language understanding for complex skincare queries
- **Implementation Approach:** Use LLM with conversation context and analysis data to provide personalized skincare guidance through an interactive chat interface.

**3. History Analytics Dashboard** *(Additional Feature #2)*
- Visual timeline of all past skin analyses
- Progress tracking with trend charts
- Statistical summaries (average scores, improvement metrics)
- Comparison between analyses
- Export functionality (CSV download)
- **Implementation Approach:** Use Plotly for interactive visualizations and pandas for data manipulation.

**4. Personalized Product Recommendations** *(Additional Feature #3)*
- AI-generated product suggestions based on skin analysis
- Categorized recommendations (cleanser, moisturizer, serum, etc.)
- Key ingredient explanations
- Usage instructions for each product
- **Implementation Approach:** Use LLM with specialized prompts to generate contextual recommendations based on analysis results.

### Supporting Features
- **User Profile Management:** Simple profile system for tracking user information (skin type, age, concerns)
- **Responsive UI:** Clean, intuitive interface accessible on desktop and mobile
- **Data Persistence:** Save analyses and chat history for future reference

## Technical Approach

### LLM-Centric Architecture

Unlike traditional approaches that require training custom models, our project adopts an **LLM-centric architecture** where business logic is encoded in carefully crafted prompts rather than traditional code algorithms.

**Key Design Principle:**
> "Let the LLM handle complexity through prompts, not code."

**Benefits:**
1. **Rapid Development:** No need for model training, dataset collection, or ML infrastructure
2. **Flexibility:** Easy to adjust behavior by modifying prompts
3. **Sophistication:** Leverage advanced reasoning capabilities of GPT-6-Luna
4. **Maintainability:** Prompts are easier to update than trained models

**Trade-offs:**
- Dependent on external API availability and costs
- Less control over exact outputs compared to trained models
- Requires careful prompt engineering for consistent results

### Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Frontend/UI** | Streamlit | Rapid prototyping, no separate frontend needed, Python-native |
| **Backend** | Python 3.9+ | Rich ecosystem, Streamlit compatibility, team familiarity |
| **LLM API** | GPT-6-Luna (HKBU endpoint) | Provided by institution, multimodal (text + image), powerful reasoning |
| **Data Visualization** | Plotly | Interactive charts, professional appearance, Streamlit integration |
| **Data Processing** | Pandas | Efficient data manipulation, analysis-friendly |
| **Data Storage** | JSON files + Session State | Lightweight, no database setup required, suitable for prototype |
| **Deployment** | Streamlit Community Cloud | Free hosting, easy deployment, automatic updates from GitHub |
| **Version Control** | Git/GitHub | Industry standard, collaboration support, deployment integration |

### Prompt Engineering Strategy

Each feature uses specialized prompts with strict output formatting:

1. **Skin Analysis Prompt:**
   - Role: Expert dermatologist
   - Output: JSON with scores, description, concerns, recommendations
   - Temperature: 0.3 (consistent results)

2. **Chatbot Prompt:**
   - Role: Friendly skincare advisor
   - Context: Includes latest analysis results
   - Temperature: 0.7 (conversational)

3. **Recommendations Prompt:**
   - Role: Product specialist
   - Output: JSON with routine, products, ingredients, tips
   - Temperature: 0.7 (creative but relevant)

## Architecture Design

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Browser                          │
│                (Streamlit Frontend)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   app.py                                │
│           (Main Application Controller)                 │
│  • Page routing                                         │
│  • Session state management                             │
│  • Navigation                                           │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┼──────────────┬─────────────┐
         ↓             ↓              ↓             ↓
    ┌────────┐   ┌─────────┐   ┌──────────┐  ┌──────────┐
    │  Skin  │   │Chatbot  │   │  Auth    │  │ History  │
    │Analysis│   │ Module  │   │  Module  │  │  Module  │
    └───┬────┘   └────┬────┘   └────┬─────┘  └────┬─────┘
        │             │              │             │
        └─────────────┴──────────────┴─────────────┘
                       │
                       ↓
              ┌────────────────┐
              │  API Client    │
              │    Module      │
              └────────┬───────┘
                       │
                       ↓
              ┌────────────────────────┐
              │   GPT-6-Luna API       │
              │  (HKBU Endpoint)       │
              └────────────────────────┘
```

### Data Flow Example: Skin Analysis

```
User uploads image
       ↓
Image validated (size, format)
       ↓
Image encoded to base64
       ↓
Prompt templates loaded
       ↓
API call to GPT-6-Luna
  • System prompt (role definition)
  • User prompt (task description)
  • Image data (base64)
       ↓
LLM processes and returns JSON
       ↓
Response parsed and validated
       ↓
Data stored:
  • Session state (current session)
  • JSON file (persistent storage)
       ↓
UI displays results
  • KPI metrics
  • Progress bars
  • Detailed description
```

### Modular Design

Each feature is self-contained in its own module:

```
modules/
├── api_client.py       # Centralized LLM API wrapper
├── skin_analysis.py    # Core analysis feature
├── chatbot.py          # Conversational interface
├── auth.py             # User authentication
├── history.py          # Analytics dashboard
└── recommendations.py  # Product suggestions
```

**Benefits:**
- Easy to develop features in parallel
- Clear separation of concerns
- Testable in isolation
- Simple to add new features

## Development Plan

### Timeline: 5 Weeks

**Week 1: Foundation**
- Set up project structure and GitHub repository
- Install dependencies and configure environment
- Create API client wrapper with error handling
- Develop prompt templates
- Test API integration

**Week 2: Core Features**
- **Member 1:** Build skin analysis module (UI + LLM integration)
- **Member 1:** Implement chatbot functionality
- **Member 2:** Create authentication system
- **Member 2:** Design UI/UX components

**Week 3: Additional Features**
- **Member 2:** Build history analytics dashboard with charts
- **Member 2:** Implement product recommendations
- **Member 1:** Refine analysis accuracy through prompt tuning
- **Member 1:** Add data persistence layer

**Week 4: Integration & Testing**
- Integrate all modules into main application
- Test end-to-end user flows
- Fix bugs and edge cases
- Polish UI/UX
- Optimize performance

**Week 5: Deployment & Documentation**
- Deploy to Streamlit Community Cloud
- Configure secrets and environment variables
- Complete project documentation
- Prepare submission materials
- Final testing in production environment

### Development Methodology

**Agile Approach:**
- 1-week sprints
- Daily standups (async via messaging)
- Sprint reviews at week end
- Feature branch workflow

**Git Workflow:**
1. Create feature branch from main
2. Develop and test locally
3. Commit with descriptive messages
4. Push to GitHub
5. Create pull request
6. Code review by teammate
7. Merge to main after approval

## Risk Assessment

### Technical Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| API downtime or rate limiting | High | Medium | Implement retry logic with exponential backoff; cache responses when possible; have fallback error messages |
| Inconsistent LLM responses | Medium | Medium | Use low temperature (0.3) for analysis; strict JSON format enforcement; validation layer |
| Image upload failures | Medium | Low | Validate file size/format; clear error messages; upload guidelines for users |
| Deployment issues | High | Low | Test locally with exact production requirements.txt; use Streamlit secrets properly |
| Performance bottlenecks | Low | Medium | Optimize image encoding; limit chat history context; use caching |

### Project Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Team member unavailability | Medium | Low | Cross-train on each other's modules; maintain clear documentation; use async communication |
| Scope creep | Medium | Medium | Stick to 3 additional features; park nice-to-have ideas for future; regular scope reviews |
| Time constraints | High | Medium | Prioritize core functionality first; have MVP mindset; cut features if needed, not quality |
| API cost overruns | Low | Low | Monitor token usage; optimize prompts; use test API key with limits |

### Quality Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Poor analysis accuracy | High | Medium | Extensive prompt engineering; test with diverse images; gather feedback |
| Security vulnerabilities | Medium | Low | Use environment variables for secrets; validate all inputs; clear security disclaimers |
| Poor user experience | Medium | Medium | Iterative UI testing; gather feedback; follow UX best practices |

## Expected Outcomes

### Deliverables

1. **Functional Web Application**
   - Deployed on Streamlit Cloud
   - Accessible via public URL
   - All 4 features (1 core + 3 additional) working

2. **Source Code Repository**
   - Clean, documented code
   - Proper Git history
   - README with setup instructions

3. **Project Documentation** (max 4 pages)
   - Initial project update (this document)
   - Final project update
   - Vibe coding reflection
   - Deployment link

4. **Technical Documentation**
   - Architecture design
   - Implementation plan
   - API documentation

### Success Criteria

**Technical Success:**
- [ ] All features functional and tested
- [ ] Deployed successfully to cloud
- [ ] API integration working reliably
- [ ] Response time < 30 seconds for analysis
- [ ] No critical bugs in production

**Educational Success:**
- [ ] Demonstrated understanding of LLM integration
- [ ] Applied collaborative development practices
- [ ] Documented technical decisions clearly
- [ ] Reflected on AI-assisted development (vibe coding)

**User Experience Success:**
- [ ] Intuitive navigation
- [ ] Clear instructions and feedback
- [ ] Professional visual design
- [ ] Accessible on multiple devices

### Learning Outcomes

Through this project, we expect to gain:

1. **Technical Skills:**
   - LLM API integration and prompt engineering
   - Streamlit application development
   - Cloud deployment and configuration
   - Data visualization with Plotly

2. **Software Engineering Practices:**
   - Version control with Git/GitHub
   - Code review and collaboration
   - Modular architecture design
   - Error handling and validation

3. **AI Development Insights:**
   - Strengths and limitations of LLM-centric approaches
   - Prompt engineering techniques
   - Balancing AI capabilities with traditional code
   - Managing AI unpredictability

4. **Professional Skills:**
   - Technical documentation
   - Project planning and estimation
   - Risk management
   - Team communication

### Future Enhancements (Out of Scope)

Ideas for future iterations:
- Real database (PostgreSQL) instead of JSON files
- Proper authentication with password hashing
- Multi-user support with data isolation
- Advanced analytics (before/after comparisons, predictive trends)
- Mobile app version
- Integration with e-commerce platforms
- Appointment booking with dermatologists
- Social features (community tips, progress sharing)

---

## Conclusion

SkinInsight represents an innovative approach to skincare analysis by leveraging the power of Large Language Models. Our LLM-centric architecture allows rapid development without the complexity of traditional ML pipelines, while still delivering sophisticated functionality.

The project is well-scoped with clear features, realistic timeline, and identified risks. Our team is prepared to collaborate effectively using modern development practices. We are confident in delivering a functional, well-documented application that meets the course requirements and demonstrates the potential of AI-assisted development.

**Next Steps:**
1. Complete environment setup and API testing
2. Begin development of core skin analysis module
3. Regular progress updates with team and instructor
4. Iterative testing and refinement

---

**Document Version:** 1.0  
**Last Updated:** November 2026  
**Status:** Submitted for Initial Project Update
