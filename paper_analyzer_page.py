"""Paper Analyzer Page - AI-powered research paper analysis"""

import streamlit as st
import sys
import os
import json
from pathlib import Path
from io import BytesIO

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from core.research_app import ResearchApp
    from utils.mongo_utils import PromptManager
except ImportError:
    st.error("⚠️ Research app dependencies not installed. Please run: pip install -r requirements.txt")
    st.stop()

# Initialize session state
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# Sidebar configuration
with st.sidebar:
    st.header("Analysis Configuration")

    # Model selection
    model = st.selectbox(
        "AI Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0
    )

    # Analysis type
    st.subheader("Analysis Type")
    analysis_type = st.selectbox(
        "Choose Analysis",
        [
            "Full Analysis",
            "Research Questions & Objectives",
            "Methodology Analysis",
            "Key Findings",
            "Limitations & Gaps",
            "Citation Analysis",
        ],
    )

    # Output format
    st.subheader("Output Format")
    output_format = st.selectbox(
        "Format", ["Structured JSON", "Narrative Text", "Both"]
    )

    # Advanced options
    with st.expander("Advanced Options"):
        include_citations = st.checkbox("Extract Citations", value=True)
        custom_prompt = st.text_area(
            "Custom Analysis Prompt",
            placeholder="Enter custom instructions for analysis...",
        )

# Main upload interface
st.subheader("📁 Upload Papers")

# File uploader
uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload one or more research papers in PDF format",
)

# Alternative: URL input
with st.expander("Or provide paper URLs/IDs"):
    col1, col2 = st.columns(2)
    with col1:
        paper_url = st.text_input("Paper URL", placeholder="https://arxiv.org/pdf/...")
    with col2:
        arxiv_id = st.text_input("ArXiv ID", placeholder="2301.12345")

    if st.button("Fetch from URL/ID"):
        if paper_url or arxiv_id:
            st.info("URL/ArXiv fetching functionality coming soon!")

# Analyze button
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

    if st.button("🔍 Analyze Papers", type="primary", use_container_width=True):
        try:
            # Initialize research app
            research_app = ResearchApp(model_name=model)

            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            all_analyses = []

            # Process each uploaded file
            for idx, uploaded_file in enumerate(uploaded_files, 1):
                status_text.text(f"Analyzing {uploaded_file.name}...")

                try:
                    # Extract text from PDF
                    pdf_bytes = BytesIO(uploaded_file.getbuffer())
                    paper_text = research_app.extract_text_from_pdf(pdf_bytes)

                    if not paper_text:
                        st.warning(f"Could not extract text from {uploaded_file.name}")
                        continue

                    # Create analysis prompt based on type
                    if analysis_type == "Full Analysis":
                        analysis_prompt = f"""
                        Analyze this research paper comprehensively and provide a structured JSON response with the following sections:
                        - title: Paper title
                        - research_questions: Main research questions
                        - methodology: Research methodology used
                        - key_findings: Main findings and results
                        - limitations: Study limitations
                        - contributions: Key contributions to the field
                        - future_work: Suggested future research directions
                        
                        Paper content (first 8000 chars):
                        {paper_text[:8000]}
                        """
                    else:
                        analysis_prompt = f"""
                        Analyze the following research paper focusing specifically on: {analysis_type}
                        
                        {'Additional instructions: ' + custom_prompt if custom_prompt else ''}
                        
                        Provide a detailed analysis in JSON format.
                        
                        Paper content (first 8000 chars):
                        {paper_text[:8000]}
                        """

                    # Get analysis
                    analysis_result = research_app.extract_research_paper_info(analysis_prompt)

                    # Store result
                    all_analyses.append({
                        "filename": uploaded_file.name,
                        "analysis_type": analysis_type,
                        "result": analysis_result,
                        "word_count": len(paper_text.split()),
                    })

                except Exception as e:
                    st.error(f"Error analyzing {uploaded_file.name}: {str(e)}")

                # Update progress
                progress_bar.progress(idx / len(uploaded_files))

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Store results
            st.session_state.analysis_results = all_analyses
            st.success(f"✅ Analysis completed for {len(all_analyses)} papers!")

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

# Display results
if st.session_state.analysis_results:
    st.markdown("---")
    st.header("📊 Analysis Results")

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Papers Analyzed", len(st.session_state.analysis_results))
    with col2:
        total_words = sum([r["word_count"] for r in st.session_state.analysis_results])
        st.metric("Total Words", f"{total_words:,}")
    with col3:
        st.metric("Analysis Type", st.session_state.analysis_results[0]["analysis_type"])

    # Display each paper's analysis
    for idx, analysis in enumerate(st.session_state.analysis_results, 1):
        with st.expander(f"📄 {analysis['filename']}", expanded=True):
            st.markdown(f"**File:** {analysis['filename']}")
            st.markdown(f"**Word Count:** {analysis['word_count']:,}")
            st.markdown("---")

            result = analysis["result"]

            # Display based on format
            if output_format in ["Structured JSON", "Both"]:
                st.subheader("Structured Output")
                try:
                    if isinstance(result, str):
                        result_json = json.loads(result)
                    else:
                        result_json = result
                    st.json(result_json)
                except:
                    st.code(result)

            if output_format in ["Narrative Text", "Both"]:
                if output_format == "Both":
                    st.markdown("---")
                st.subheader("Analysis Text")
                st.markdown(result if isinstance(result, str) else json.dumps(result, indent=2))

            # Action buttons
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📥 Download Analysis", key=f"download_{idx}"):
                    st.info("Download functionality coming soon!")
            with col2:
                if st.button(f"📋 Copy Analysis", key=f"copy_{idx}"):
                    st.info("Copy functionality coming soon!")

    # Clear results button
    if st.button("🗑️ Clear All Results", use_container_width=True):
        st.session_state.analysis_results = None
        st.rerun()

# Help section
with st.expander("ℹ️ How to Use Paper Analyzer"):
    st.markdown(
        """
    ### Paper Analyzer Guide
    
    1. **Upload Papers**: Upload PDF files using the file uploader
    2. **Choose Analysis Type**: Select what aspect to focus on
    3. **Configure Options**: Adjust model and output format
    4. **Run Analysis**: Click "Analyze Papers" to start
    5. **Review Results**: Explore the structured analysis results
    
    ### Analysis Types
    
    - **Full Analysis**: Comprehensive analysis of all aspects
    - **Research Questions & Objectives**: Focus on research goals
    - **Methodology Analysis**: Examine research methods used
    - **Key Findings**: Extract main results and discoveries
    - **Limitations & Gaps**: Identify study weaknesses
    - **Citation Analysis**: Analyze references and citations
    
    ### Tips
    
    - Use GPT-4o for more detailed analysis
    - Try different analysis types on the same paper
    - Use custom prompts for specific requirements
    """
    )
