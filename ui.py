import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import message

def create_sidebar():
    """Create professional sidebar with API key input"""
    st.sidebar.title("🔑 API Configuration")
    api_key = st.sidebar.text_input("Mistral API Key", type="password", 
                                   help="Get your key from mistral.ai")
    st.sidebar.markdown("---")
    st.sidebar.title("📊 Quick Stats")
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric("Fit Score", "85%", "↑2%")
    with col2:
        st.metric("Skills Match", "12/15")
    with col3:
        st.metric("Status", "✅ PASS")
    return api_key

def create_wheel_chart(score):
    """Create beautiful wheel chart for resume fit"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Resume Fit Score"},
        delta = {'reference': 75},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))
    fig.update_layout(height=300, font=dict(size=12))
    return fig

def resume_analysis_tab(agent):
    """Tab 1: Resume Analysis with Job Matching"""
    st.header("📋 Resume Analysis & Job Matching")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Job Selection")
        job_positions = [
            "AI/ML Engineer", "Data Scientist", "NLP Engineer", 
            "Computer Vision Engineer", "MLOps Engineer"
        ]
        selected_job = st.selectbox("Select Position", job_positions)
        
        skills = {
            "AI/ML Engineer": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "NLP", "Computer Vision"],
            "Data Scientist": ["Statistics", "SQL", "Pandas", "Machine Learning", "A/B Testing"],
            "NLP Engineer": ["Transformers", "BERT", "spaCy", "HuggingFace", "LLM Fine-tuning"]
        }
    
    with col2:
        if st.button("🚀 Analyze Resume Fit", use_container_width=True):
            with st.spinner("Analyzing your resume..."):
                result = agent.analyze_resume_fit(selected_job, skills=skills.get(selected_job))
                st.session_state.analysis_result = result
    
    if 'analysis_result' in st.session_state:
        result = st.session_state.analysis_result
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.metric("🎯 Fit Score", f"{result['fit_score']:.1f}%")
            status = "✅ PASS" if result['fit_score'] > 75 else "❌ FAIL"
            st.error(f"Status: {status}")
        
        with col2:
            st.subheader("✅ Matching Skills")
            for skill in result.get('matching_skills', [])[:5]:
                st.success(f"• {skill}")
        
        with col3:
            st.subheader("⚠️ Weak Areas")
            for area in result.get('weak_areas', [])[:3]:
                st.warning(f"• {area}")
        
        # Wheel Chart
        st.plotly_chart(create_wheel_chart(result['fit_score']), use_container_width=True)
        
        # Improvement Suggestions
        st.subheader("💡 Improvement Suggestions")
        for suggestion in result.get('suggestions', [])[:5]:
            st.info(suggestion)

def interview_prep_tab(agent):
    """Tab 2: Interview Preparation"""
    st.header("🎤 Interview Preparation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("❓ Generate Questions")
        job_title = st.selectbox("Job Title", ["AI/ML Engineer", "Data Scientist"])
        if st.button("Generate Questions", use_container_width=True):
            questions = agent.generate_interview_questions(job_title)
            st.session_state.questions = questions
    
    with col2:
        if 'questions' in st.session_state:
            st.subheader("📝 Your Questions")
            st.markdown(st.session_state.questions)
    
    st.subheader("💬 Chat with Your Resume")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.chat_input("Ask about your skills, projects, experience...")
    if user_input:
        response = agent.chat_with_resume(user_input)
        st.session_state.chat_history.append({"user": user_input, "agent": response})
    
    for chat in st.session_state.chat_history:
        message(chat["user"], is_user=True)
        message(chat["agent"])

def resume_improver_tab(agent):
    """Tab 3: Resume Improver"""
    st.header("✨ Resume Improver")
    
    job_title = st.selectbox("Target Job Title", ["AI/ML Engineer", "Data Scientist"])
    
    if st.button("🎯 Generate Improved Resume", use_container_width=True):
        with st.spinner("Improving your resume..."):
            improved_resume = agent.improve_resume(job_title)
            st.session_state.improved_resume = improved_resume
    
    if 'improved_resume' in st.session_state:
        st.subheader("✅ Your Improved Resume")
        st.markdown(st.session_state.improved_resume)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "💾 Download Improved Resume",
                data=st.session_state.improved_resume,
                file_name="improved_resume.md",
                mime="text/markdown"
            )
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(st.session_state.improved_resume)

def create_tabs(agent):
    """Create all 4 tabs with excellent UI"""
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Resume Analysis", "🎤 Interview Prep", "✨ Resume Improver", "💾 Download"])
    
    with tab1:
        resume_analysis_tab(agent)
    
    with tab2:
        interview_prep_tab(agent)
    
    with tab3:
        resume_improver_tab(agent)
    
    with tab4:
        st.header("💾 Download Center")
        if 'improved_resume' in st.session_state:
            st.download_button(
                "🎯 Download Final Resume",
                data=st.session_state.improved_resume,
                file_name="final_improved_resume.md",
                mime="text/markdown",
                use_container_width=True
            )
