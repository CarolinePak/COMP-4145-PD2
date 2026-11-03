# SkinInsight - Vibe Coding Reflection

## Table of Contents
- [What is Vibe Coding?](#what-is-vibe-coding)
- [Our Experience with AI-Assisted Development](#our-experience-with-ai-assisted-development)
- [Tools and Techniques Used](#tools-and-techniques-used)
- [Benefits Realized](#benefits-realized)
- [Challenges Encountered](#challenges-encountered)
- [Human-AI Collaboration Dynamics](#human-ai-collaboration-dynamics)
- [Code Quality Considerations](#code-quality-considerations)
- [Learning Outcomes](#learning-outcomes)
- [Best Practices Discovered](#best-practices-discovered)
- [Future of AI-Assisted Development](#future-of-ai-assisted-development)

## What is Vibe Coding?

**Vibe Coding** (also known as AI-assisted coding or prompt-driven development) refers to the practice of using Large Language Models and AI assistants to accelerate software development. Rather than writing every line of code manually, developers describe what they want to build, and AI tools generate code, documentation, and even architectural designs.

**Key Characteristics:**
- Natural language descriptions → Working code
- Rapid prototyping and iteration
- AI as a pair programming partner
- Focus on high-level logic, not syntax
- Documentation generation alongside code

**Common AI Tools:**
- Claude (Anthropic) - Conversational coding assistant
- GitHub Copilot - Inline code suggestions
- ChatGPT (OpenAI) - General purpose assistance
- Cursor - AI-powered IDE
- Tabnine - Code completion

## Our Experience with AI-Assisted Development

### How We Used AI in This Project

Throughout the SkinInsight project, we extensively leveraged AI assistance, particularly Claude, for various development tasks:

**1. Architecture Design (80% AI-assisted)**
- Described project requirements to AI
- AI suggested modular architecture
- AI generated system architecture diagrams (in text/ASCII)
- AI proposed technology stack with justifications
- **Human role:** Validated choices, made final decisions, adjusted for course requirements

**2. Code Generation (60% AI-assisted)**
- AI wrote initial boilerplate code
- AI generated module skeletons
- AI implemented standard patterns (API clients, error handling)
- AI wrote utility functions
- **Human role:** Reviewed code, customized logic, integrated modules, fixed bugs

**3. Documentation (70% AI-assisted)**
- AI generated README structure
- AI wrote technical documentation (ARCHITECTURE.md)
- AI created step-by-step implementation plans
- AI drafted project updates
- **Human role:** Added project-specific details, verified accuracy, refined language

**4. Prompt Engineering (90% AI-assisted)**
- AI helped craft effective LLM prompts
- AI suggested prompt structures and formats
- AI iteratively refined prompts based on feedback
- **Human role:** Tested prompts, evaluated outputs, fine-tuned for our use case

**5. Debugging (40% AI-assisted)**
- AI suggested solutions to error messages
- AI explained complex errors
- AI proposed debugging strategies
- **Human role:** Implemented fixes, tested thoroughly, handled edge cases

**6. Testing (30% AI-assisted)**
- AI suggested test scenarios
- AI wrote test script templates
- **Human role:** Executed tests, identified real-world issues, wrote additional tests

### Example: AI-Generated Code

**Prompt to AI:**
> "Create a Python function for a Streamlit app that validates an uploaded image file. Check if the file size is under 5MB and if the format is jpg, png, or jpeg. Return a tuple with (is_valid: bool, error_message: str or None)."

**AI-Generated Code:**
```python
def validate_image(uploaded_file) -> tuple:
    """
    Validate uploaded image file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_TYPES = ["jpg", "jpeg", "png"]
    
    # Check file size
    if uploaded_file.size > MAX_SIZE:
        size_mb = uploaded_file.size / (1024 * 1024)
        max_mb = MAX_SIZE / (1024 * 1024)
        return False, f"File too large ({size_mb:.1f}MB). Maximum size: {max_mb:.1f}MB"
    
    # Check file type
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext not in ALLOWED_TYPES:
        return False, f"Invalid file type: {file_ext}. Allowed types: {', '.join(ALLOWED_TYPES)}"
    
    return True, None
```

**Human Refinement:**
- Moved constants to `config.py` for consistency
- Added unit tests for edge cases
- Integrated with UI error display
- Added logging for debugging

**Result:** Production-ready function in 5 minutes vs. 20-30 minutes manual coding.

## Tools and Techniques Used

### Primary AI Tool: Claude (Anthropic)

**Why Claude?**
- Strong at understanding complex requirements
- Excellent at generating structured outputs (JSON, markdown)
- Good at explaining technical concepts
- Maintains context across long conversations
- Produces high-quality, well-commented code

**How We Used Claude:**

1. **Conversational Development:**
   ```
   Human: "I need an API client wrapper for GPT-6-Luna with retry logic"
   Claude: [Generates complete api_client.py with exponential backoff]
   Human: "Add timeout handling"
   Claude: [Updates code with timeout parameter]
   ```

2. **Iterative Refinement:**
   - Start with general requirements
   - AI generates initial version
   - Human tests and provides feedback
   - AI refines based on feedback
   - Repeat until satisfactory

3. **Documentation Generation:**
   - Ask AI to explain code it generated
   - Generate README sections
   - Create inline comments
   - Write docstrings

### Prompting Techniques

**1. Specific Requirements:**
❌ Bad: "Write a function for image analysis"
✅ Good: "Write a Python function that takes image bytes, calls GPT-6-Luna API, and returns parsed JSON with skin scores"

**2. Context Provision:**
```
"I'm building a Streamlit app for skin analysis. I need a chatbot module that:
- Uses st.chat_message() for display
- Stores history in session_state
- Includes latest analysis in context
- Has a clear history button"
```

**3. Format Specification:**
```
"Generate Python code with:
- Type hints
- Docstrings
- Error handling
- No external dependencies beyond requirements.txt"
```

**4. Example-Driven:**
```
"Create a prompt template similar to this example, but for product recommendations:
[paste example prompt]"
```

**5. Incremental Building:**
- Start with skeleton/interface
- Add one feature at a time
- Test between additions
- Refine based on results

### Collaboration Workflow

```
┌─────────────┐
│   Human:    │
│  Describe   │
│   Need      │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    AI:      │
│  Generate   │
│   Code      │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Human:    │
│   Review    │
│    Test     │
└──────┬──────┘
       │
       ↓
  ┌────┴────┐
  │ Works?  │
  └────┬────┘
       │
   No  │  Yes
   ────┤────→ [Integrate]
       │
       ↓
┌─────────────┐
│   Human:    │
│  Provide    │
│  Feedback   │
└──────┬──────┘
       │
       ↓
   [Loop back to AI]
```

## Benefits Realized

### 1. Development Speed

**Time Savings Estimate:**

| Task | Manual Time | With AI | Time Saved | AI Impact |
|------|-------------|---------|------------|-----------|
| API Client Module | 4 hours | 1 hour | 75% | High |
| Prompt Templates | 3 hours | 1 hour | 67% | High |
| Documentation | 8 hours | 3 hours | 63% | High |
| Module Boilerplate | 6 hours | 2 hours | 67% | High |
| Error Handling | 3 hours | 1 hour | 67% | Medium |
| Testing Scripts | 2 hours | 1 hour | 50% | Medium |
| UI Components | 4 hours | 2 hours | 50% | Medium |
| Debugging | 6 hours | 4 hours | 33% | Low |
| **Total** | **36 hours** | **15 hours** | **58%** | **High** |

**Overall Development Time Reduced by ~60%**

### 2. Code Quality Improvements

**AI-Generated Code Quality:**
- ✅ Consistent style and formatting
- ✅ Comprehensive error handling
- ✅ Clear variable naming
- ✅ Proper type hints
- ✅ Detailed docstrings
- ✅ Standard design patterns

**Human Additions:**
- Project-specific logic
- Edge case handling
- Integration code
- Optimization for our use case

### 3. Learning Acceleration

**Knowledge Gained:**
- Learned Streamlit best practices from AI-generated examples
- Understood prompt engineering through AI guidance
- Discovered Python patterns we hadn't used before
- Learned error handling strategies

**Example:**
We didn't know about Streamlit's `st.session_state` persistence patterns. AI showed us:
```python
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    # Initialize variables
```

This pattern became central to our architecture.

### 4. Documentation Excellence

**AI Advantages:**
- Never forgets to document
- Consistent documentation style
- Explains complex concepts clearly
- Generates multiple formats (README, API docs, guides)

**Human Additions:**
- Project-specific context
- Screenshots and diagrams
- Real deployment URLs
- Team reflections

### 5. Reduced Boilerplate Pain

**Repetitive tasks AI handled:**
- Import statements
- File/directory creation commands
- Configuration files (.gitignore, requirements.txt)
- Standard function signatures
- Common utility functions

**Time saved on "boring" tasks:** ~40%

## Challenges Encountered

### 1. AI Doesn't Know Everything

**Limitations:**
- Doesn't know our specific API endpoint behavior
- Can't test code in our environment
- Doesn't understand project-specific constraints
- Training data cutoff means outdated library versions

**Example Issue:**
AI suggested using `st.experimental_rerun()` which was deprecated. We had to update to `st.rerun()`.

**Solution:** Always verify AI suggestions against official documentation.

### 2. Context Window Limitations

**Problem:**
Long conversations caused AI to "forget" earlier context.

**Example:**
After 50+ exchanges, AI suggested a structure inconsistent with our earlier architecture decisions.

**Solution:**
- Start new conversations for new modules
- Summarize key decisions in each prompt
- Keep architectural decisions in shared documents

### 3. Over-Reliance Risk

**Observation:**
Sometimes accepted AI code without fully understanding it.

**Consequence:**
Difficulty debugging later when issues arose.

**Solution:**
- Always read and understand AI-generated code
- Ask AI to explain complex sections
- Refactor for clarity if needed
- Add our own comments

### 4. Integration Challenges

**Problem:**
AI generates modules independently, but integration requires human judgment.

**Example:**
Each module had slightly different error handling patterns.

**Solution:**
- Created style guide early
- Refactored for consistency
- Centralized common patterns (API client)

### 5. Testing Gaps

**Problem:**
AI-generated code rarely includes comprehensive tests.

**Example:**
Generated code worked for happy path but failed on edge cases.

**Solution:**
- Human-written integration tests
- Manual testing of all features
- Real-world usage scenarios

### 6. Prompt Engineering Learning Curve

**Challenge:**
Initially, vague prompts produced generic code.

**Learning Process:**
- Week 1: Generic prompts → Generic code
- Week 2: Specific prompts → Better code
- Week 3: Context-rich prompts → Great code

**Key Insight:** Prompt quality directly affects output quality.

## Human-AI Collaboration Dynamics

### What Humans Did Better

**1. High-Level Design Decisions**
- Choosing features to implement
- Balancing scope vs. time
- Understanding user needs
- Making trade-offs

**2. Integration & Architecture**
- Connecting modules cohesively
- Ensuring consistent patterns
- Managing dependencies
- Overall system design

**3. Testing & Quality Assurance**
- Identifying edge cases
- Real-world usage testing
- User experience evaluation
- Performance optimization

**4. Context & Judgment**
- Understanding project constraints
- Prioritizing features
- Deciding when "good enough" is enough
- Managing risks

**5. Creative Problem Solving**
- Novel solutions to unique problems
- Adapting to unexpected challenges
- Inventing new approaches

### What AI Did Better

**1. Code Generation**
- Writing boilerplate quickly
- Implementing standard patterns
- Generating consistent code style
- Creating comprehensive examples

**2. Documentation**
- Writing detailed explanations
- Generating multiple formats
- Maintaining consistency
- Never forgetting to document

**3. Knowledge Recall**
- Remembering syntax details
- Recalling library functions
- Providing code examples
- Explaining concepts

**4. Repetitive Tasks**
- Creating similar components
- Generating configuration files
- Writing utility functions

**5. Initial Drafts**
- Starting point for refinement
- Multiple options to choose from
- Quick prototyping

### Ideal Division of Labor

**AI Role: The Efficient Junior Developer**
- Generate initial code
- Handle boilerplate
- Create documentation templates
- Suggest solutions

**Human Role: The Senior Architect**
- Make design decisions
- Review and refine AI output
- Handle integration
- Ensure quality
- Make final calls

**Collaboration Model:**
```
Human: Strategy & Design
   ↓
AI: Implementation
   ↓
Human: Review & Refinement
   ↓
AI: Adjustments
   ↓
Human: Integration & Testing
```

## Code Quality Considerations

### Quality Comparison

**AI-Generated Code Quality:** 7/10
- Clean and readable
- Follows conventions
- Good error handling
- Sometimes over-engineered
- May miss project-specific nuances

**Human-Written Code Quality:** 8/10
- Context-aware
- Optimized for use case
- Sometimes inconsistent style
- Occasionally incomplete documentation

**AI + Human Collaboration Quality:** 9/10
- Best of both worlds
- Consistent and contextual
- Well-documented
- Thoroughly tested

### Code Ownership

**Important Principle:**
> Even if AI wrote the code, the developer is responsible for understanding, maintaining, and debugging it.

**Our Approach:**
1. AI generates code
2. Human reads and understands it
3. Human customizes for project
4. Human tests thoroughly
5. Human commits with confidence

**Never blindly commit AI code without understanding it.**

## Learning Outcomes

### Technical Skills Gained

**1. Prompt Engineering**
- How to write effective prompts
- Iterative refinement techniques
- Context provision strategies

**2. Code Review Skills**
- Evaluating AI-generated code
- Identifying potential issues
- Refactoring for clarity

**3. Streamlit Development**
- Best practices learned from AI examples
- Common patterns and anti-patterns
- Performance optimization techniques

**4. LLM Integration**
- API communication patterns
- Error handling strategies
- Response parsing techniques

### Soft Skills Developed

**1. Critical Thinking**
- Evaluating AI suggestions
- Questioning assumptions
- Validating outputs

**2. Communication**
- Articulating requirements clearly
- Providing effective feedback
- Explaining technical concepts

**3. Judgment**
- Knowing when to use AI
- Recognizing AI limitations
- Making final decisions

**4. Adaptability**
- Working with new tools
- Adjusting to AI capabilities
- Iterating based on results

### Meta-Learning

**Learning How to Learn with AI:**
- Use AI to explain concepts
- Ask for examples and analogies
- Request step-by-step breakdowns
- Generate practice problems

**Example:**
"Explain how Streamlit session state works with an analogy and code example."

## Best Practices Discovered

### 1. Start with AI, End with Human

```
AI generates → Human reviews → Human tests → Human refines → Human approves
```

### 2. Be Specific in Prompts

❌ "Write a chatbot"
✅ "Write a Streamlit chatbot module that stores history in session_state, includes latest analysis context, and uses st.chat_message() for display"

### 3. Iterate Incrementally

- Get basic version working first
- Add features one at a time
- Test after each addition
- Refine based on results

### 4. Validate Everything

- Don't trust AI blindly
- Check against documentation
- Test in real environment
- Verify assumptions

### 5. Maintain Human Oversight

- Review all AI-generated code
- Understand before integrating
- Test thoroughly
- Take ownership

### 6. Use AI for Learning

- Ask "why" questions
- Request explanations
- Seek alternatives
- Learn patterns

### 7. Document AI Contributions

- Note which code was AI-generated
- Record prompts used (for future reference)
- Document refinements made
- Share learnings with team

### 8. Set Quality Standards

- Define coding standards upfront
- Share with AI in prompts
- Enforce through code review
- Refactor for consistency

## Future of AI-Assisted Development

### Trends We Observed

**1. AI Capabilities Improving**
- Better code quality over time
- More context awareness
- Fewer errors

**2. Integration Deepening**
- IDEs with built-in AI
- Version control with AI review
- Testing with AI generation

**3. Prompt Engineering as a Skill**
- Increasingly important
- Specialized techniques emerging
- Best practices forming

### Implications for Developers

**What Changes:**
- Less time on syntax, more on architecture
- Higher-level thinking required
- Faster prototyping
- More focus on integration

**What Doesn't Change:**
- Need for deep understanding
- Importance of testing
- Value of code review
- Critical thinking essential

**Skills Becoming More Important:**
- System design
- Prompt engineering
- Code review
- Testing strategies
- User experience

**Skills Becoming Less Critical:**
- Memorizing syntax
- Writing boilerplate
- Documentation formatting

### Our Prediction

**10 Years from Now:**
- AI will generate ~80% of code
- Humans will focus on:
  - Requirements and design
  - Architecture decisions
  - Integration and testing
  - User experience
  - Strategic direction

**But humans will still be essential for:**
- Understanding business needs
- Making trade-off decisions
- Ensuring quality and security
- Providing creativity and innovation
- Exercising judgment

## Conclusion

### Summary of Our Vibe Coding Experience

**What Worked Well:**
✅ Rapid development (60% time savings)
✅ Consistent code quality
✅ Excellent documentation
✅ Accelerated learning
✅ Reduced boilerplate work

**What Was Challenging:**
⚠️ Learning to prompt effectively
⚠️ Avoiding over-reliance
⚠️ Handling integration complexity
⚠️ Testing AI-generated code
⚠️ Maintaining context across long sessions

**Overall Assessment:**
Vibe coding with AI assistance was a **highly positive experience** that significantly accelerated our development while maintaining high quality. The key was finding the right balance between AI generation and human oversight.

### Recommendations for Others

**For Students:**
1. **Learn the fundamentals first** - Understand coding before relying on AI
2. **Use AI as a teacher** - Ask for explanations, not just code
3. **Always review and understand** - Don't blindly copy-paste
4. **Start simple** - Build skills incrementally
5. **Focus on architecture** - AI helps with implementation, you design the system

**For Teams:**
1. **Establish guidelines** - When and how to use AI
2. **Share learnings** - What prompts work well
3. **Maintain standards** - Code quality expectations
4. **Review AI code** - Same standards as human code
5. **Document usage** - Track what AI generates

**For Projects:**
1. **Use for prototyping** - Fast initial versions
2. **Refine iteratively** - AI + human collaboration
3. **Test thoroughly** - Don't assume AI code is bug-free
4. **Keep humans in control** - Final decisions by humans
5. **Learn continuously** - Improve prompts over time

### Final Thoughts

**The Future is Collaborative:**
The best results come from **human-AI collaboration**, not AI replacement of humans. AI amplifies human capabilities, allowing developers to work at a higher level of abstraction and deliver more value faster.

**Vibe coding isn't about replacing developers** - it's about empowering them to focus on what matters: solving real problems, designing great systems, and creating value for users.

We're excited about the future of AI-assisted development and believe the skills we've learned in this project will be increasingly valuable in the software industry.

---

**Reflection Authors:** SkinInsight Team  
**Date:** November 2026  
**Project:** COMP4145 PD2  
**AI Tool Used:** Claude (Anthropic) + GPT-6-Luna  
**Overall Experience:** ⭐⭐⭐⭐⭐ (5/5)
