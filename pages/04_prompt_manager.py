"""
Prompt Manager Page
Manage research prompts with CRUD operations
"""

import streamlit as st
import json
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.session_manager import SessionStateManager

# Page configuration
st.set_page_config(page_title="Prompt Manager", page_icon="📝", layout="wide")

st.title("📝 Research Prompt Manager")
st.markdown("Create, manage, and organize research prompts for various analysis tasks")

# Initialize
SessionStateManager.initialize()

# Comprehensive prompts library from research.py
DEFAULT_PROMPTS = {
    "Summary": {
        "category": "Analysis",
        "prompt": "Provide a comprehensive summary of this research paper including: 1) Main research question/objective, 2) Key methodology, 3) Major findings, 4) Conclusions and implications. Keep it concise but informative.",
        "variables": [],
    },
    "Key Findings": {
        "category": "Analysis",
        "prompt": "Extract and list the key findings from this research paper. For each finding: 1) State the finding clearly, 2) Mention the evidence or data supporting it, 3) Explain its significance.",
        "variables": [],
    },
    "Methodology Review": {
        "category": "Analysis",
        "prompt": "Analyze the research methodology used in this paper: 1) What methods were used?, 2) Were they appropriate for the research question?, 3) What are the strengths and limitations?, 4) Could alternative methods have been better?",
        "variables": [],
    },
    "Critical Analysis": {
        "category": "Analysis",
        "prompt": "Provide a critical analysis of this research paper covering: 1) Strengths (novelty, rigor, contribution), 2) Weaknesses (limitations, gaps, assumptions), 3) Validity of conclusions, 4) Suggestions for improvement.",
        "variables": [],
    },
    "Literature Review": {
        "category": "Analysis",
        "prompt": "Analyze how this paper reviews and positions itself within existing literature: 1) Key papers cited, 2) Research gaps identified, 3) How this work fills those gaps, 4) Missing relevant literature.",
        "variables": [],
    },
    "Research Gap Identification": {
        "category": "Research Planning",
        "prompt": "Based on this paper, identify potential research gaps and future research directions: 1) What questions remain unanswered?, 2) What are the stated limitations?, 3) What extensions could be explored?, 4) What new questions arise?",
        "variables": [],
    },
    "Proposal Generation": {
        "category": "Research Planning",
        "prompt": "Generate a research proposal based on this paper's findings. Include: 1) Research question, 2) Significance and motivation, 3) Proposed methodology, 4) Expected contributions, 5) Timeline and resources needed.",
        "variables": ["research_area"],
    },
    "Dataset Analysis": {
        "category": "Technical",
        "prompt": "Analyze the datasets used in this research: 1) What datasets were used?, 2) Are they appropriate for the task?, 3) Dataset characteristics (size, quality, bias), 4) Data preprocessing steps, 5) Availability and reproducibility.",
        "variables": [],
    },
    "Experimental Design": {
        "category": "Technical",
        "prompt": "Evaluate the experimental design: 1) What experiments were conducted?, 2) Control variables and baselines, 3) Evaluation metrics used, 4) Statistical significance, 5) Reproducibility considerations.",
        "variables": [],
    },
    "Results Interpretation": {
        "category": "Technical",
        "prompt": "Interpret the results presented in this paper: 1) What do the results show?, 2) Are there unexpected findings?, 3) How do results compare to prior work?, 4) What are alternative interpretations?, 5) Confidence in conclusions.",
        "variables": [],
    },
    "Comparison Study": {
        "category": "Comparative",
        "prompt": "Compare this paper with the following reference: {reference}. Include: 1) Similarities in approach, 2) Key differences, 3) Relative strengths and weaknesses, 4) Which is more suitable for {use_case}?",
        "variables": ["reference", "use_case"],
    },
    "Technical Depth": {
        "category": "Technical",
        "prompt": "Provide an in-depth technical analysis: 1) Theoretical foundations, 2) Mathematical formulations, 3) Algorithm details, 4) Computational complexity, 5) Implementation considerations.",
        "variables": [],
    },
    "Practical Applications": {
        "category": "Application",
        "prompt": "Identify practical applications of this research: 1) Real-world use cases, 2) Industry relevance, 3) Deployment challenges, 4) Scalability considerations, 5) Commercialization potential.",
        "variables": [],
    },
    "Ethical Considerations": {
        "category": "Ethics",
        "prompt": "Analyze ethical considerations in this research: 1) Potential ethical concerns, 2) Societal impact, 3) Bias and fairness issues, 4) Privacy considerations, 5) Responsible AI principles.",
        "variables": [],
    },
    "Grant Proposal": {
        "category": "Research Planning",
        "prompt": "Draft a grant proposal section based on this paper for {funding_agency}. Include: 1) Project title, 2) Abstract, 3) Significance, 4) Innovation, 5) Approach, 6) Expected outcomes.",
        "variables": ["funding_agency"],
    },
}


class PromptManager:
    """Manage research prompts with CRUD operations"""

    @staticmethod
    def initialize_prompts():
        """Initialize prompts in session state"""
        if "prompts" not in st.session_state:
            st.session_state["prompts"] = DEFAULT_PROMPTS.copy()

    @staticmethod
    def get_all_prompts() -> Dict:
        """Get all prompts"""
        PromptManager.initialize_prompts()
        return st.session_state["prompts"]

    @staticmethod
    def get_prompt(name: str) -> Optional[Dict]:
        """Get a specific prompt"""
        prompts = PromptManager.get_all_prompts()
        return prompts.get(name)

    @staticmethod
    def add_prompt(name: str, category: str, prompt: str, variables: List[str]):
        """Add a new prompt"""
        prompts = PromptManager.get_all_prompts()
        prompts[name] = {"category": category, "prompt": prompt, "variables": variables}
        st.session_state["prompts"] = prompts

    @staticmethod
    def update_prompt(name: str, category: str, prompt: str, variables: List[str]):
        """Update an existing prompt"""
        prompts = PromptManager.get_all_prompts()
        if name in prompts:
            prompts[name] = {
                "category": category,
                "prompt": prompt,
                "variables": variables,
            }
            st.session_state["prompts"] = prompts

    @staticmethod
    def delete_prompt(name: str):
        """Delete a prompt"""
        prompts = PromptManager.get_all_prompts()
        if name in prompts:
            del prompts[name]
            st.session_state["prompts"] = prompts

    @staticmethod
    def get_categories() -> List[str]:
        """Get all unique categories"""
        prompts = PromptManager.get_all_prompts()
        categories = set(p["category"] for p in prompts.values())
        return sorted(list(categories))

    @staticmethod
    def export_prompts() -> str:
        """Export prompts as JSON"""
        prompts = PromptManager.get_all_prompts()
        return json.dumps(prompts, indent=2)

    @staticmethod
    def import_prompts(prompts_json: str):
        """Import prompts from JSON"""
        try:
            prompts = json.loads(prompts_json)
            st.session_state["prompts"] = prompts
            return True, "Prompts imported successfully!"
        except Exception as e:
            return False, f"Error importing prompts: {str(e)}"


# Initialize prompts
PromptManager.initialize_prompts()

# Sidebar - Filters and Actions
with st.sidebar:
    st.header("🔍 Filters")

    # Category filter
    categories = ["All"] + PromptManager.get_categories()
    selected_category = st.selectbox("Category", categories)

    # Search
    search_query = st.text_input("🔎 Search prompts", placeholder="Enter keywords...")

    st.divider()

    # Import/Export
    st.header("📤 Import/Export")

    # Export
    if st.button("📥 Export Prompts", use_container_width=True):
        export_data = PromptManager.export_prompts()
        st.download_button(
            label="Download JSON",
            data=export_data,
            file_name="research_prompts.json",
            mime="application/json",
            use_container_width=True,
        )

    # Import
    uploaded_file = st.file_uploader("📤 Import Prompts", type=["json"])
    if uploaded_file:
        try:
            prompts_json = uploaded_file.read().decode()
            success, message = PromptManager.import_prompts(prompts_json)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    st.divider()

    # Reset
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        if st.session_state.get("confirm_reset"):
            st.session_state["prompts"] = DEFAULT_PROMPTS.copy()
            st.session_state["confirm_reset"] = False
            st.success("Prompts reset to defaults!")
            st.rerun()
        else:
            st.session_state["confirm_reset"] = True
            st.warning("Click again to confirm reset")

# Main content
tab1, tab2, tab3 = st.tabs(["📚 Browse Prompts", "➕ Add New", "📊 Statistics"])

with tab1:
    st.subheader("📚 Prompt Library")

    # Get and filter prompts
    all_prompts = PromptManager.get_all_prompts()

    # Apply filters
    filtered_prompts = {}
    for name, data in all_prompts.items():
        # Category filter
        if selected_category != "All" and data["category"] != selected_category:
            continue

        # Search filter
        if search_query:
            search_lower = search_query.lower()
            if (
                search_lower not in name.lower()
                and search_lower not in data["prompt"].lower()
                and search_lower not in data["category"].lower()
            ):
                continue

        filtered_prompts[name] = data

    if not filtered_prompts:
        st.info("No prompts found matching your filters.")
    else:
        st.info(f"📝 Showing {len(filtered_prompts)} prompt(s)")

        # Display prompts
        for name, data in filtered_prompts.items():
            with st.expander(f"**{name}** - {data['category']}", expanded=False):
                # Display prompt
                st.markdown("**Prompt:**")
                st.code(data["prompt"], language=None)

                # Variables
                if data["variables"]:
                    st.markdown("**Variables:**")
                    st.write(", ".join([f"`{{{v}}}`" for v in data["variables"]]))

                # Actions
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("📋 Copy", key=f"copy_{name}"):
                        st.code(data["prompt"], language=None)
                        st.success("Prompt displayed above!")

                with col2:
                    if st.button("✏️ Edit", key=f"edit_{name}"):
                        st.session_state["edit_prompt"] = name
                        st.rerun()

                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{name}"):
                        PromptManager.delete_prompt(name)
                        st.success(f"Deleted '{name}'")
                        st.rerun()

with tab2:
    st.subheader("➕ Add New Prompt")

    # Check if editing
    editing = st.session_state.get("edit_prompt")

    if editing:
        st.info(f"✏️ Editing: **{editing}**")
        prompt_data = PromptManager.get_prompt(editing)
        default_name = editing
        default_category = prompt_data["category"]
        default_prompt = prompt_data["prompt"]
        default_variables = ", ".join(prompt_data["variables"])
    else:
        default_name = ""
        default_category = "Analysis"
        default_prompt = ""
        default_variables = ""

    with st.form("prompt_form"):
        # Prompt name
        prompt_name = st.text_input(
            "Prompt Name *",
            value=default_name,
            placeholder="e.g., Summary Analysis",
            disabled=bool(editing),
        )

        # Category
        existing_categories = PromptManager.get_categories()
        category_options = existing_categories + ["+ New Category"]

        category_index = (
            existing_categories.index(default_category)
            if default_category in existing_categories
            else 0
        )
        category_select = st.selectbox(
            "Category *", options=category_options, index=category_index
        )

        if category_select == "+ New Category":
            category = st.text_input("New Category Name", placeholder="e.g., Ethics")
        else:
            category = category_select

        # Prompt text
        prompt_text = st.text_area(
            "Prompt Text *",
            value=default_prompt,
            height=200,
            placeholder="Enter your prompt here. Use {variable_name} for variables.",
            help="Use {variable_name} syntax to define variables that can be filled in later",
        )

        # Variables
        variables_input = st.text_input(
            "Variables (comma-separated)",
            value=default_variables,
            placeholder="e.g., research_area, use_case",
            help="List variable names that appear in {curly braces} in the prompt",
        )

        # Submit
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button(
                "💾 Save Prompt" if editing else "➕ Add Prompt",
                type="primary",
                use_container_width=True,
            )
        with col2:
            if editing and st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state["edit_prompt"] = None
                st.rerun()

        if submitted:
            # Validation
            if not prompt_name or not category or not prompt_text:
                st.error("Please fill in all required fields (*)")
            else:
                # Parse variables
                variables = [v.strip() for v in variables_input.split(",") if v.strip()]

                # Add or update
                if editing:
                    PromptManager.update_prompt(
                        prompt_name, category, prompt_text, variables
                    )
                    st.success(f"✅ Updated '{prompt_name}'")
                    st.session_state["edit_prompt"] = None
                else:
                    if prompt_name in PromptManager.get_all_prompts():
                        st.error(
                            f"Prompt '{prompt_name}' already exists. Use a different name or edit the existing one."
                        )
                    else:
                        PromptManager.add_prompt(
                            prompt_name, category, prompt_text, variables
                        )
                        st.success(f"✅ Added '{prompt_name}'")

                st.rerun()

with tab3:
    st.subheader("📊 Prompt Statistics")

    all_prompts = PromptManager.get_all_prompts()

    # Overall stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Prompts", len(all_prompts))

    with col2:
        st.metric("Categories", len(PromptManager.get_categories()))

    with col3:
        prompts_with_vars = sum(1 for p in all_prompts.values() if p["variables"])
        st.metric("With Variables", prompts_with_vars)

    st.divider()

    # Category breakdown
    st.subheader("📈 Prompts by Category")

    category_counts = {}
    for data in all_prompts.values():
        cat = data["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    for category, count in sorted(
        category_counts.items(), key=lambda x: x[1], reverse=True
    ):
        st.markdown(f"**{category}**: {count} prompt(s)")

    st.divider()

    # Variable usage
    st.subheader("🔤 Most Common Variables")

    variable_counts = {}
    for data in all_prompts.values():
        for var in data["variables"]:
            variable_counts[var] = variable_counts.get(var, 0) + 1

    if variable_counts:
        for var, count in sorted(
            variable_counts.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            st.markdown(f"**{{{var}}}**: Used in {count} prompt(s)")
    else:
        st.info("No variables defined in prompts")

# Footer
st.divider()
st.markdown(
    """
### 💡 Tips
- **Variables**: Use `{variable_name}` syntax in prompts for customizable fields
- **Categories**: Organize prompts by purpose (Analysis, Technical, Ethics, etc.)
- **Export**: Backup your prompts regularly or share with colleagues
- **Search**: Use keywords to quickly find relevant prompts
"""
)
