"""
Prompt Manager Page
Manage research prompts with CRUD operations
"""

import streamlit as st
import json
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.session_manager import SessionStateManager
from src.utils.prompt_manager import PromptManager as MongoPromptManager

# Page configuration
st.markdown("Create, manage, and organize research prompts for various analysis tasks")

# Initialize
SessionStateManager.initialize()


class PromptManager:
    """Manage research prompts with CRUD operations using MongoDB"""

    _mongo_manager = None

    @staticmethod
    def get_mongo_manager():
        """Get or create MongoDB manager instance"""
        if PromptManager._mongo_manager is None:
            try:
                PromptManager._mongo_manager = MongoPromptManager()
            except Exception as e:
                st.error(f"Failed to connect to MongoDB: {str(e)}")
                st.info(
                    "Please ensure MongoDB is running and MONGODB_URI is set in your environment."
                )
                return None
        return PromptManager._mongo_manager

    @staticmethod
    def initialize_prompts():
        """Initialize prompts - check database connection"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return

        # Just verify connection is working
        try:
            manager.get_all_prompts()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")


# Try Prompt Modal Dialog
if st.session_state.get("try_prompt"):
    prompt_name = st.session_state["try_prompt"]
    prompt_data = st.session_state.get("try_prompt_data")

    @st.dialog(f"🚀 Try Prompt: {prompt_name}", width="large")
    def show_try_prompt_dialog():
        from src.services.llm_manager import get_llm_manager
        from src.utils.credentials_manager import CredentialsManager

        st.markdown(f"**Category:** {prompt_data['category']}")
        if prompt_data.get("description"):
            st.markdown(f"*{prompt_data['description']}*")

        st.divider()

        # Show original prompt template
        with st.expander("View Prompt Template"):
            st.code(prompt_data["prompt"], language=None)

        # Variable inputs
        variable_values = {}
        if prompt_data["variables"]:
            st.subheader("📝 Fill in Variables")
            for var in prompt_data["variables"]:
                variable_values[var] = st.text_input(
                    f"{var}:",
                    key=f"var_{var}",
                    placeholder=f"Enter value for {var}",
                    help=f"This value will replace {{{var}}} in the prompt",
                )

        st.divider()

        # LLM Configuration
        st.subheader("🤖 LLM Configuration")

        llm_manager = get_llm_manager()
        configured_providers = CredentialsManager.get_configured_providers()

        if not configured_providers:
            st.warning(
                "⚠️ No LLM providers configured. Please configure at least one provider in Settings."
            )
            if st.button("Go to Settings"):
                st.session_state["try_prompt"] = None
                st.switch_page("pages/05_settings.py")
            return

        col1, col2 = st.columns(2)

        with col1:
            # Provider selection
            provider_names = {
                p: llm_manager.get_provider_info(p).get("name", p)
                for p in configured_providers
            }
            selected_provider = st.selectbox(
                "Provider",
                options=configured_providers,
                format_func=lambda x: provider_names.get(x, x),
            )

        with col2:
            # Model selection
            if selected_provider:
                available_models = llm_manager.get_available_models(selected_provider)
                if available_models and available_models != ["custom"]:
                    selected_model = st.selectbox("Model", options=available_models)
                else:
                    selected_model = st.text_input(
                        "Model Name",
                        placeholder="Enter model name",
                    )

        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)

        st.divider()

        # Generate button
        if st.button("✨ Generate Response", type="primary", use_container_width=True):
            # Validate variables
            if prompt_data["variables"]:
                missing_vars = [
                    v for v in prompt_data["variables"] if not variable_values.get(v)
                ]
                if missing_vars:
                    st.error(f"Please fill in all variables: {', '.join(missing_vars)}")
                    return

            # Replace variables in prompt
            final_prompt = prompt_data["prompt"]
            for var, value in variable_values.items():
                final_prompt = final_prompt.replace(f"{{{var}}}", value)

            # Show final prompt
            with st.expander("📄 Final Prompt Sent to LLM"):
                st.code(final_prompt, language=None)

            # Initialize LLM and generate
            try:
                with st.spinner(
                    f"Generating response using {provider_names.get(selected_provider)}..."
                ):
                    llm = llm_manager.initialize_model(
                        provider=selected_provider,
                        model=selected_model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )

                    response = llm.invoke(final_prompt)

                    st.success("✅ Response generated!")
                    st.markdown("### 🤖 LLM Response")
                    st.markdown(response.content)

            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

        # Close button
        if st.button("Close", use_container_width=True):
            st.session_state["try_prompt"] = None
            st.session_state["try_prompt_data"] = None
            st.rerun()

    show_try_prompt_dialog()

    # Main content

    @staticmethod
    def get_all_prompts() -> Dict:
        """Get all prompts from MongoDB"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return {}

        prompts = manager.get_all_prompts()
        # Transform to match expected format
        result = {}
        for prompt in prompts:
            result[prompt["title"]] = {
                "category": prompt.get("category", "general"),
                "description": prompt.get("description", ""),
                "prompt": prompt.get("value", ""),
                "variables": prompt.get("variables", []),
                "tags": prompt.get("tags", []),
            }
        return result

    @staticmethod
    def get_prompt(name: str) -> Optional[Dict]:
        """Get a specific prompt"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return None

        prompt = manager.get_prompt_by_title(name)
        if prompt:
            return {
                "category": prompt.get("category", "general"),
                "description": prompt.get("description", ""),
                "prompt": prompt.get("value", ""),
                "variables": prompt.get("variables", []),
                "tags": prompt.get("tags", []),
            }
        return None

    @staticmethod
    def add_prompt(
        name: str,
        category: str,
        prompt: str,
        variables: List[str],
        description: str = "",
        tags: List[str] = None,
    ):
        """Add a new prompt"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return {"success": False, "message": "MongoDB connection failed"}

        return manager.add_prompt(
            title=name,
            value=prompt,
            category=category,
            description=description,
            variables=variables,
            tags=tags or [],
        )

    @staticmethod
    def update_prompt(
        name: str,
        category: str,
        prompt: str,
        variables: List[str],
        description: str = "",
        tags: List[str] = None,
    ):
        """Update an existing prompt"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return {"success": False, "message": "MongoDB connection failed"}

        updates = {
            "value": prompt,
            "category": category,
            "description": description,
            "variables": variables,
            "tags": tags or [],
        }
        return manager.update_prompt(name, updates)

    @staticmethod
    def delete_prompt(name: str):
        """Delete a prompt"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return {"success": False, "message": "MongoDB connection failed"}

        return manager.delete_prompt(name)

    @staticmethod
    def get_categories() -> List[str]:
        """Get all unique categories"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return []

        return manager.get_all_categories()

    @staticmethod
    def search_prompts(search_term: str) -> Dict:
        """Search prompts by term"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return {}

        prompts = manager.search_prompts(search_term)
        # Transform to match expected format
        result = {}
        for prompt in prompts:
            result[prompt["title"]] = {
                "category": prompt.get("category", "general"),
                "description": prompt.get("description", ""),
                "prompt": prompt.get("value", ""),
                "variables": prompt.get("variables", []),
                "tags": prompt.get("tags", []),
            }
        return result

    @staticmethod
    def export_prompts() -> str:
        """Export prompts as JSON"""
        prompts = PromptManager.get_all_prompts()
        return json.dumps(prompts, indent=2)

    @staticmethod
    def import_prompts(prompts_json: str):
        """Import prompts from JSON"""
        try:
            manager = PromptManager.get_mongo_manager()
            if manager is None:
                return False, "MongoDB connection failed"

            prompts = json.loads(prompts_json)

            # Import each prompt
            success_count = 0
            for name, data in prompts.items():
                result = manager.add_prompt(
                    title=name,
                    value=data.get("prompt", data.get("value", "")),
                    category=data.get("category", "general"),
                    description=data.get("description", ""),
                    variables=data.get("variables", []),
                    tags=data.get("tags", []),
                )
                if result.get("success"):
                    success_count += 1

            return True, f"Successfully imported {success_count} prompts!"
        except Exception as e:
            return False, f"Error importing prompts: {str(e)}"

    @staticmethod
    def delete_all_prompts():
        """Delete all prompts from database"""
        manager = PromptManager.get_mongo_manager()
        if manager is None:
            return False, "MongoDB connection failed"

        try:
            # Delete all existing prompts
            all_prompts = manager.get_all_prompts()
            for prompt in all_prompts:
                manager.delete_prompt(prompt["title"])

            return True, f"Deleted all {len(all_prompts)} prompts!"
        except Exception as e:
            return False, f"Error deleting prompts: {str(e)}"


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

    # Delete All
    if st.button("�️ Delete All Prompts", use_container_width=True):
        if st.session_state.get("confirm_delete_all"):
            success, message = PromptManager.delete_all_prompts()
            st.session_state["confirm_delete_all"] = False
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        else:
            st.session_state["confirm_delete_all"] = True
            st.warning("⚠️ Click again to confirm deletion of ALL prompts")

# Main content
tab1, tab2, tab3 = st.tabs(["📚 Browse Prompts", "➕ Add New", "📊 Statistics"])

with tab1:
    st.subheader("📚 Prompt Library")

    # Get and filter prompts
    all_prompts = PromptManager.get_all_prompts()

    # Apply filters
    filtered_prompts = {}

    # If search is active, use search_prompts method
    if search_query:
        filtered_prompts = PromptManager.search_prompts(search_query)
        # Apply category filter to search results
        if selected_category != "All":
            filtered_prompts = {
                name: data
                for name, data in filtered_prompts.items()
                if data["category"] == selected_category
            }
    else:
        # Apply category filter only
        for name, data in all_prompts.items():
            if selected_category != "All" and data["category"] != selected_category:
                continue
            filtered_prompts[name] = data

    if not filtered_prompts:
        st.info("No prompts found matching your filters.")
    else:
        st.info(f"📝 Showing {len(filtered_prompts)} prompt(s)")

        # Display prompts
        for name, data in filtered_prompts.items():
            with st.expander(f"**{name}** - {data['category']}", expanded=False):
                # Description
                if data.get("description"):
                    st.markdown(f"*{data['description']}*")
                    st.divider()

                # Display prompt
                st.markdown("**Prompt:**")
                st.code(data["prompt"], language=None)

                # Variables
                if data["variables"]:
                    st.markdown("**Variables:**")
                    st.write(", ".join([f"`{{{v}}}`" for v in data["variables"]]))

                # Tags (for filtering)
                if data.get("tags"):
                    st.markdown("**Tags:**")
                    st.write(", ".join([f"`{t}`" for t in data["tags"]]))

                # Actions - aligned to left
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button(
                        "🚀 Try Prompt", key=f"try_{name}", use_container_width=True
                    ):
                        st.session_state["try_prompt"] = name
                        st.session_state["try_prompt_data"] = data
                        st.rerun()

                with col2:
                    if st.button(
                        "✏️ Edit", key=f"edit_{name}", use_container_width=True
                    ):
                        st.session_state["edit_prompt"] = name
                        st.rerun()

with tab2:
    st.subheader("➕ Add New Prompt")

    # Check if editing
    editing = st.session_state.get("edit_prompt")

    if editing:
        st.info(f"✏️ Editing: **{editing}**")
        prompt_data = PromptManager.get_prompt(editing)
        if prompt_data:
            default_name = editing
            default_category = prompt_data["category"]
            default_description = prompt_data.get("description", "")
            default_prompt = prompt_data["prompt"]
            default_variables = ", ".join(prompt_data["variables"])
            default_tags = ", ".join(prompt_data.get("tags", []))
        else:
            st.error(f"Prompt '{editing}' not found")
            st.session_state["edit_prompt"] = None
            st.rerun()
    else:
        default_name = ""
        default_category = "Analysis"
        default_description = ""
        default_prompt = ""
        default_variables = ""
        default_tags = ""

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

        # Description
        description = st.text_area(
            "Description",
            value=default_description,
            height=100,
            placeholder="Brief description of what this prompt does",
            help="Optional description to help understand the purpose of this prompt",
        )

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
            "Variables (comma-separated) *",
            value=default_variables,
            placeholder="e.g., research_area, use_case",
            help="List variable names that appear in {curly braces} in the prompt. These will be replaced at runtime.",
        )

        # Tags
        tags_input = st.text_input(
            "Tags (comma-separated)",
            value=default_tags,
            placeholder="e.g., research, analysis, paper",
            help="Optional tags for filtering and organizing prompts",
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
                # Parse variables and tags
                variables = [v.strip() for v in variables_input.split(",") if v.strip()]
                tags = [t.strip() for t in tags_input.split(",") if t.strip()]

                # Add or update
                if editing:
                    result = PromptManager.update_prompt(
                        prompt_name, category, prompt_text, variables, description, tags
                    )
                    if result.get("success"):
                        st.success(f"✅ Updated '{prompt_name}'")
                        st.session_state["edit_prompt"] = None
                        st.rerun()
                    else:
                        st.error(result.get("message", "Failed to update"))
                else:
                    result = PromptManager.add_prompt(
                        prompt_name, category, prompt_text, variables, description, tags
                    )
                    if result.get("success"):
                        st.success(f"✅ Added '{prompt_name}'")
                        st.rerun()
                    else:
                        st.error(result.get("message", "Failed to add prompt"))

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
- **Try Prompt**: Click 🚀 Try Prompt to test prompts with your configured LLM
- **Variables**: Use `{variable_name}` syntax in prompts for runtime replacement
- **Tags**: Use tags for filtering and organizing prompts (separate from variables)
- **Categories**: Organize prompts by purpose (Analysis, Technical, Ethics, etc.)
- **Export**: Backup your prompts regularly or share with colleagues
- **Search**: Use keywords to quickly find relevant prompts across title, description, and tags
- **MongoDB**: All prompts are stored in MongoDB for persistence across sessions
"""
)
