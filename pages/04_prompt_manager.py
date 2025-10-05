"""
Prompt Manager Page
Manage research prompts with CRUD operations
"""

import streamlit as st
import json
from typing import Dict, List, Optional
from src.utils.session_manager import SessionStateManager
from src.utils.prompt_manager import PromptManager as MongoPromptManager

st.markdown("Create, manage, and organize research prompts for various analysis tasks")
SessionStateManager.initialize()


class PromptManager:
    """Manage research prompts with CRUD operations using MongoDB"""

    _mongo_manager = None

    @staticmethod
    def _manager():
        """Get or initialize MongoDB manager"""
        if PromptManager._mongo_manager is None:
            try:
                PromptManager._mongo_manager = MongoPromptManager()
            except Exception as e:
                st.error(f"⚠️ Failed to connect to MongoDB: {e}")
                st.info("Ensure MongoDB is running and MONGODB_URI is set.")
                return None
        return PromptManager._mongo_manager

    # ---------------------------
    # CRUD + UTILITY OPERATIONS
    # ---------------------------
    @staticmethod
    def get_all_prompts() -> Dict:
        mgr = PromptManager._manager()
        if not mgr:
            return {}
        prompts = mgr.get_all_prompts()
        return {
            str(p["_id"]): {
                "title": p["title"],
                "category": p.get("category", "general"),
                "description": p.get("description", ""),
                "prompt": p.get("value", ""),
                "variables": p.get("variables", []),
                "tags": p.get("tags", []),
            }
            for p in prompts
        }

    @staticmethod
    def get_prompt(name: str) -> Optional[Dict]:
        mgr = PromptManager._manager()
        if not mgr:
            return None
        p = mgr.get_prompt_by_title(name)
        if not p:
            return None
        return {
            "category": p.get("category", "general"),
            "description": p.get("description", ""),
            "prompt": p.get("value", ""),
            "variables": p.get("variables", []),
            "tags": p.get("tags", []),
        }

    @staticmethod
    def get_categories() -> List[str]:
        mgr = PromptManager._manager()
        if not mgr:
            return []
        return mgr.get_all_categories() or []

    @staticmethod
    def search_prompts(term: str) -> Dict:
        mgr = PromptManager._manager()
        if not mgr:
            return {}
        prompts = mgr.search_prompts(term)
        return {
            str(p["_id"]): {
                "title": p["title"],
                "category": p.get("category", "general"),
                "description": p.get("description", ""),
                "prompt": p.get("value", ""),
                "variables": p.get("variables", []),
                "tags": p.get("tags", []),
            }
            for p in prompts
        }

    @staticmethod
    def add_prompt(name, category, prompt, variables, description="", tags=None):
        mgr = PromptManager._manager()
        if not mgr:
            return {"success": False, "message": "MongoDB not connected"}
        return mgr.add_prompt(
            title=name,
            value=prompt,
            category=category,
            description=description,
            variables=variables,
            tags=tags or [],
        )

    @staticmethod
    def update_prompt(name, category, prompt, variables, description="", tags=None):
        mgr = PromptManager._manager()
        if not mgr:
            return {"success": False, "message": "MongoDB not connected"}
        updates = {
            "value": prompt,
            "category": category,
            "description": description,
            "variables": variables,
            "tags": tags or [],
        }
        return mgr.update_prompt(name, updates)

    @staticmethod
    def delete_prompt(name):
        mgr = PromptManager._manager()
        if not mgr:
            return {"success": False, "message": "MongoDB not connected"}
        return mgr.delete_prompt(name)

    @staticmethod
    def export_prompts() -> str:
        # Export without MongoDB _id, use title as key for compatibility
        prompts = PromptManager.get_all_prompts()
        export_dict = {
            data["title"]: {
                "category": data["category"],
                "description": data["description"],
                "prompt": data["prompt"],
                "variables": data["variables"],
                "tags": data["tags"],
            }
            for data in prompts.values()
        }
        return json.dumps(export_dict, indent=2)

    @staticmethod
    def import_prompts(prompts_json: str):
        mgr = PromptManager._manager()
        if not mgr:
            return False, "MongoDB not connected"
        try:
            prompts = json.loads(prompts_json)
            count = 0
            for title, data in prompts.items():
                res = mgr.add_prompt(
                    title=title,
                    value=data.get("prompt", ""),
                    category=data.get("category", "general"),
                    description=data.get("description", ""),
                    variables=data.get("variables", []),
                    tags=data.get("tags", []),
                )
                if res.get("success"):
                    count += 1
            return True, f"Imported {count} prompts successfully."
        except Exception as e:
            return False, f"Error importing prompts: {e}"

    @staticmethod
    def delete_all_prompts():
        mgr = PromptManager._manager()
        if not mgr:
            return False, "MongoDB not connected"
        try:
            all_prompts = mgr.get_all_prompts()
            for p in all_prompts:
                mgr.delete_prompt(p["title"])
            return True, f"Deleted {len(all_prompts)} prompts."
        except Exception as e:
            return False, f"Error deleting prompts: {e}"


with st.sidebar:
    st.header("🔍 Filters")

    categories = ["All"] + PromptManager.get_categories()
    selected_category = st.selectbox("Category", categories)

    search_query = st.text_input("🔎 Search prompts", placeholder="Enter keywords...")


tab1, tab2, tab3 = st.tabs(["📚 Browse Prompts", "➕ Add New", "📊 Statistics"])

# ---------- TAB 1: BROWSE ----------
with tab1:
    st.subheader("📚 Prompt Library")

    all_prompts = PromptManager.get_all_prompts()

    if search_query:
        filtered_prompts = PromptManager.search_prompts(search_query)
        if selected_category != "All":
            filtered_prompts = {
                n: d
                for n, d in filtered_prompts.items()
                if d["category"] == selected_category
            }
    else:
        filtered_prompts = {
            n: d
            for n, d in all_prompts.items()
            if selected_category == "All" or d["category"] == selected_category
        }

    if not filtered_prompts:
        st.info("No prompts found.")
    else:
        st.info(f"📝 Showing {len(filtered_prompts)} prompt(s)")
        for prompt_id, data in filtered_prompts.items():
            prompt_title = data["title"]
            with st.expander(
                f"**{prompt_title}** ({data['category']})", expanded=False
            ):
                if data.get("description"):
                    st.markdown(f"*{data['description']}*")
                if data.get("tags"):
                    st.markdown(
                        "**Tags:** " + ", ".join([f"`{t}`" for t in data["tags"]])
                    )
                st.divider()
                st.markdown("**Prompt:**")
                st.code(data["prompt"], language=None)
                if data["variables"]:
                    st.markdown(
                        "**Variables:** "
                        + ", ".join([f"`{{{v}}}`" for v in data["variables"]])
                    )

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(
                        "🚀 Try Prompt",
                        key=f"try_{prompt_id}",
                        use_container_width=True,
                    ):
                        st.session_state["try_prompt"] = prompt_title
                        st.session_state["try_prompt_data"] = data
                        st.rerun()
                with col2:
                    if st.button(
                        "✏️ Edit", key=f"edit_{prompt_id}", use_container_width=True
                    ):
                        st.session_state["edit_prompt"] = prompt_title
                        st.rerun()


# ---------- TAB 2: ADD/EDIT ----------
with tab2:
    st.subheader("➕ Add New Prompt")

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
        prompt_name = st.text_input(
            "Prompt Name *", value=default_name, disabled=bool(editing)
        )
        existing_categories = PromptManager.get_categories()
        category_options = existing_categories + ["+ New Category"]
        category_select = st.selectbox("Category *", options=category_options)
        category = (
            st.text_input("New Category Name")
            if category_select == "+ New Category"
            else category_select
        )
        description = st.text_area("Description", value=default_description, height=100)
        prompt_text = st.text_area(
            "Prompt Text *",
            value=default_prompt,
            height=200,
            placeholder="Use {variable_name} for variables.",
        )
        variables_input = st.text_input(
            "Variables (comma-separated) *", value=default_variables
        )
        tags_input = st.text_input("Tags (comma-separated)", value=default_tags)

        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button(
                "💾 Save Prompt" if editing else "➕ Add Prompt", type="primary"
            )
        with col2:
            if editing and st.form_submit_button("❌ Cancel"):
                st.session_state["edit_prompt"] = None
                st.rerun()

        if submitted:
            if not prompt_name or not category or not prompt_text:
                st.error("Please fill in all required fields (*)")
            else:
                variables = [v.strip() for v in variables_input.split(",") if v.strip()]
                tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                if editing:
                    result = PromptManager.update_prompt(
                        prompt_name, category, prompt_text, variables, description, tags
                    )
                else:
                    result = PromptManager.add_prompt(
                        prompt_name, category, prompt_text, variables, description, tags
                    )
                if result.get("success"):
                    st.success(
                        f"✅ {'Updated' if editing else 'Added'} '{prompt_name}'"
                    )
                    st.session_state["edit_prompt"] = None
                    st.rerun()
                else:
                    st.error(result.get("message", "Operation failed"))


# ---------- TAB 3: STATISTICS ----------
with tab3:
    st.subheader("📊 Prompt Statistics")
    all_prompts = PromptManager.get_all_prompts()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Prompts", len(all_prompts))
    with col2:
        st.metric("Categories", len(PromptManager.get_categories()))
    with col3:
        st.metric(
            "With Variables", sum(1 for p in all_prompts.values() if p["variables"])
        )

    st.divider()
    st.subheader("📈 Prompts by Category")

    category_counts = {}
    for d in all_prompts.values():
        category_counts[d["category"]] = category_counts.get(d["category"], 0) + 1
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        st.markdown(f"**{cat}**: {count} prompt(s)")

    st.divider()
    st.subheader("🔤 Most Common Variables")
    variable_counts = {}
    for d in all_prompts.values():
        for var in d["variables"]:
            variable_counts[var] = variable_counts.get(var, 0) + 1
    if variable_counts:
        for var, count in sorted(
            variable_counts.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            st.markdown(f"**{{{var}}}**: Used in {count} prompt(s)")
    else:
        st.info("No variables defined.")


# ------------------------------------------------------
# 💡 FOOTER
# ------------------------------------------------------
st.divider()
st.markdown(
    """
### 💡 Tips
- **Try Prompt**: Click 🚀 Try Prompt to test prompts with your configured LLM  
- **Variables**: Use `{variable_name}` syntax for runtime replacements  
- **Tags**: Use tags for quick filtering  
- **Categories**: Organize prompts logically (Analysis, Ethics, etc.)  
- **Export/Import**: Backup or share your prompt collections  
- **MongoDB**: Prompts are stored persistently in MongoDB  
"""
)
