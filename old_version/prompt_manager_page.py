import streamlit as st
from src.utils.mongo_utils import PromptManager

# Example prompt structure display

# MongoDB connection (uses env var or default)
prompt_manager = PromptManager()

# Sidebar: Add/Edit/Delete
st.sidebar.header("Manage Prompts")

# List all prompts
prompts = prompt_manager.get_all_prompts()

# Search
search_term = st.text_input("Search Prompts", "")
if search_term:
    prompts = prompt_manager.search_prompts(search_term)

# Display prompts in a table
st.subheader("Prompt List")
if prompts:
    for prompt in prompts:
        with st.expander(f"{prompt.get('title', '')} [{prompt.get('category', '')}]"):
            st.write(f"**Description:** {prompt.get('description', '')}")
            st.write(f"**Value:**\n{prompt.get('value', '')}")
            st.write(f"**Tags:** {', '.join(prompt.get('tags', []))}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Edit", key=f"edit_{prompt['_id']}"):
                    st.session_state['edit_prompt'] = prompt
            with col2:
                if st.button(f"Delete", key=f"delete_{prompt['_id']}"):
                    result = prompt_manager.delete_prompt(prompt['title'])
                    st.success(result['message'])
                    st.experimental_rerun()
else:
    st.info("No prompts found.")

# Add/Edit prompt form
edit_prompt = st.session_state.get('edit_prompt')
if edit_prompt:
    st.subheader("Edit Prompt")
    with st.form("edit_prompt_form"):
        title = st.text_input("Title", value=edit_prompt['title'])
        value = st.text_area("Value", value=edit_prompt['value'])
        category = st.text_input("Category", value=edit_prompt.get('category', 'general'))
        description = st.text_area("Description", value=edit_prompt.get('description', ''))
        tags = st.text_input("Tags (comma separated)", value=','.join(edit_prompt.get('tags', [])))
        submitted = st.form_submit_button("Update Prompt")
        if submitted:
            updates = {
                "title": title,
                "value": value,
                "category": category,
                "description": description,
                "tags": [t.strip() for t in tags.split(',') if t.strip()],
            }
            result = prompt_manager.update_prompt(edit_prompt['title'], updates)
            st.success(result['message'])
            st.session_state['edit_prompt'] = None
            st.experimental_rerun()
    if st.button("Cancel Edit"):
        st.session_state['edit_prompt'] = None
        st.experimental_rerun()
else:
    st.subheader("Add New Prompt")
    with st.form("add_prompt_form"):
        title = st.text_input("Title")
        value = st.text_area("Value")
        category = st.text_input("Category", value="general")
        description = st.text_area("Description")
        tags = st.text_input("Tags (comma separated)")
        submitted = st.form_submit_button("Add Prompt")
        if submitted:
            result = prompt_manager.add_prompt(
                title=title,
                value=value,
                category=category,
                description=description,
                tags=[t.strip() for t in tags.split(',') if t.strip()]
            )
            if result['success']:
                st.success(result['message'])
                st.experimental_rerun()
            else:
                st.error(result['message'])
