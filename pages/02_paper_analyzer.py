"""
Paper Analyzer Page
Analyze research papers using AI with multi-LLM support
"""

import streamlit as st
from pathlib import Path
import tempfile
from typing import List
from src.core.paper_analyzer import PaperAnalyzer
from src.utils.credentials_manager import CredentialsManager, LLMConfigWidget
from src.utils.session_manager import SessionStateManager
from config.constants import ANALYSIS_TYPES, UI_MESSAGES

# Page configuration
st.set_page_config(page_title="Paper Analyzer", page_icon="📄", layout="wide")

st.title("📄 Research Paper Analyzer")
st.markdown("Analyze research papers with AI-powered insights using your choice of LLM")

# Initialize
CredentialsManager.initialize()
SessionStateManager.initialize()

# Check if any LLM is configured
configured_providers = CredentialsManager.get_configured_providers()
if not configured_providers:
    st.warning(
        "⚠️ No LLM providers configured. Please configure at least one provider in Settings."
    )
    if st.button("Go to Settings"):
        st.switch_page("pages/05_settings.py")
    st.stop()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # LLM Selection
    provider, model = LLMConfigWidget.render_model_selector(default_provider="openai")

    if not provider or not model:
        st.error("Please select a valid provider and model")
        st.stop()

    st.divider()

    # Analysis settings
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Higher values make output more creative but less consistent",
    )

    max_tokens = st.number_input(
        "Max Tokens",
        min_value=500,
        max_value=4000,
        value=2000,
        step=100,
        help="Maximum length of analysis",
    )

# Main content
tab1, tab2 = st.tabs(["📄 Single Paper", "📚 Batch Analysis"])

with tab1:
    st.subheader("Analyze a Single Paper")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload PDF", type=["pdf"], help="Upload a research paper in PDF format"
    )

    if uploaded_file:
        # Analysis type selection
        analysis_type = st.selectbox(
            "Analysis Type",
            options=list(ANALYSIS_TYPES.keys()),
            help="Select the type of analysis to perform",
        )

        # Custom prompt option
        use_custom_prompt = st.checkbox("Use Custom Prompt")
        custom_prompt = ""

        if use_custom_prompt:
            custom_prompt = st.text_area(
                "Custom Prompt",
                height=150,
                placeholder="Enter your custom analysis prompt here...",
                help="Provide specific instructions for the analysis",
            )

        # Analyze button
        if st.button("🔍 Analyze Paper", type="primary", use_container_width=True):
            if not custom_prompt and use_custom_prompt:
                st.error(
                    "Please provide a custom prompt or uncheck 'Use Custom Prompt'"
                )
            else:
                with st.spinner(f"Analyzing paper with {provider} - {model}..."):
                    try:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".pdf"
                        ) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name

                        # Get credentials
                        api_key = CredentialsManager.get_api_key(provider)
                        creds = CredentialsManager.get_credential(provider)

                        # Create analyzer with multi-LLM support
                        analyzer = PaperAnalyzer(
                            provider=provider,
                            model=model,
                            api_key=api_key,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            **{k: v for k, v in creds.items() if k != "api_key"},
                        )

                        # Perform analysis
                        result = analyzer.analyze_pdf(
                            tmp_path,
                            analysis_type=(
                                analysis_type if not use_custom_prompt else "custom"
                            ),
                            custom_prompt=custom_prompt if use_custom_prompt else None,
                        )

                        # Display results
                        st.success("✅ Analysis complete!")
                        st.markdown("---")
                        st.markdown("### Analysis Results")
                        st.markdown(result)

                        # Save to history
                        SessionStateManager.increment_counter("analysis_count")

                        # Download button
                        st.download_button(
                            label="📥 Download Analysis",
                            data=result,
                            file_name=f"analysis_{uploaded_file.name.replace('.pdf', '')}.txt",
                            mime="text/plain",
                        )

                    except Exception as e:
                        st.error(f"Error analyzing paper: {str(e)}")
                    finally:
                        # Clean up temp file
                        Path(tmp_path).unlink(missing_ok=True)

with tab2:
    st.subheader("Batch Analysis")
    st.markdown("Analyze multiple papers at once with the same settings")

    # Multiple file upload
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload multiple research papers",
    )

    if uploaded_files:
        st.info(f"📚 {len(uploaded_files)} papers uploaded")

        # Analysis type selection
        batch_analysis_type = st.selectbox(
            "Analysis Type",
            options=list(ANALYSIS_TYPES.keys()),
            key="batch_analysis_type",
        )

        # Analyze button
        if st.button("🔍 Analyze All Papers", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.container()

            with st.spinner("Analyzing papers..."):
                try:
                    # Save files temporarily
                    temp_paths = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".pdf"
                        ) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            temp_paths.append(tmp_file.name)

                    # Get credentials
                    api_key = CredentialsManager.get_api_key(provider)
                    creds = CredentialsManager.get_credential(provider)

                    # Create analyzer
                    analyzer = PaperAnalyzer(
                        provider=provider,
                        model=model,
                        api_key=api_key,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        **{k: v for k, v in creds.items() if k != "api_key"},
                    )

                    # Analyze each paper
                    results = []
                    for idx, (temp_path, uploaded_file) in enumerate(
                        zip(temp_paths, uploaded_files)
                    ):
                        progress = (idx + 1) / len(uploaded_files)
                        progress_bar.progress(progress)
                        status_text.text(
                            f"Analyzing {uploaded_file.name}... ({idx + 1}/{len(uploaded_files)})"
                        )

                        result = analyzer.analyze_pdf(
                            temp_path, analysis_type=batch_analysis_type
                        )

                        results.append(
                            {"filename": uploaded_file.name, "analysis": result}
                        )

                    # Display results
                    status_text.empty()
                    progress_bar.empty()
                    st.success(f"✅ Analyzed {len(results)} papers!")

                    with results_container:
                        for idx, result_data in enumerate(results):
                            with st.expander(
                                f"📄 {result_data['filename']}", expanded=idx == 0
                            ):
                                st.markdown(result_data["analysis"])

                        # Download all results
                        all_results_text = (
                            "\n\n"
                            + "=" * 80
                            + "\n\n".join(
                                [
                                    f"PAPER: {r['filename']}\n\n{r['analysis']}"
                                    for r in results
                                ]
                            )
                        )

                        st.download_button(
                            label="📥 Download All Analyses",
                            data=all_results_text,
                            file_name="batch_analysis_results.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )

                    # Update session
                    SessionStateManager.increment_counter(
                        "analysis_count", len(results)
                    )

                except Exception as e:
                    st.error(f"Error in batch analysis: {str(e)}")
                finally:
                    # Clean up temp files
                    for temp_path in temp_paths:
                        Path(temp_path).unlink(missing_ok=True)

# Footer
st.divider()
st.markdown(
    """
### 💡 Tips
- **Summary**: Get a quick overview of the paper's main points
- **Key Findings**: Extract the most important results and conclusions
- **Methodology**: Understand the research methods and experimental design
- **Critical Analysis**: Get a balanced evaluation of strengths and weaknesses
- **Custom Prompt**: Tailor the analysis to your specific needs
"""
)
