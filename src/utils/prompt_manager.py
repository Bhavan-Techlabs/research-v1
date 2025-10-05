"""
MongoDB Utility for Prompt Management
Handles storage and retrieval of prompts from MongoDB
"""

from typing import List, Dict, Optional

from pymongo.errors import DuplicateKeyError
from .mongo_manager import MongoDBManager


class PromptManager(MongoDBManager):
    """
    MongoDB-based prompt management system for research prompts.
    Inherits from generic MongoDBManager.
    """

    def __init__(
        self, mongodb_uri: str = None, database_name: str = "research_assistant"
    ):
        super().__init__(
            collection_name="prompts",
            mongodb_uri=mongodb_uri,
            database_name=database_name,
        )

    def add_prompt(
        self,
        title: str,
        value: str,
        category: str = "general",
        description: str = "",
        variables: list = None,
        tags: list = None,
    ) -> dict:
        """
        Add a new prompt to the database

        Args:
            title: Prompt title
            value: Prompt text/template
            category: Category of the prompt
            description: Description of what the prompt does
            variables: List of variable names used in the prompt (for replacement)
            tags: List of tags for the prompt (for filtering)

        Returns:
            Dictionary with insertion result
        """
        if variables is None:
            variables = []
        if tags is None:
            tags = []

        prompt_doc = {
            "title": title,
            "value": value,
            "category": category,
            "description": description,
            "variables": variables,
            "tags": tags,
        }
        try:
            result = self.insert_one(prompt_doc)
            return {
                "success": True,
                "id": str(result.inserted_id),
                "message": f"Prompt '{title}' added successfully",
            }
        except DuplicateKeyError:
            return {
                "success": False,
                "message": f"Prompt with title '{title}' already exists",
            }
        except Exception as e:
            return {"success": False, "message": f"Error adding prompt: {str(e)}"}

    def get_prompt_by_title(self, title: str) -> dict:
        """
        Retrieve a prompt by its title

        Args:
            title: Title of the prompt

        Returns:
            Prompt document or None if not found
        """
        return self.find_one({"title": title})

    def get_prompts_by_category(self, category: str) -> list:
        """
        Retrieve all prompts in a category

        Args:
            category: Category name

        Returns:
            List of prompt documents
        """
        return self.find({"category": category})

    def get_all_prompts(self) -> list:
        """
        Retrieve all prompts

        Returns:
            List of all prompt documents
        """
        return self.find()

    def get_all_categories(self) -> list:
        """
        Get list of all unique categories

        Returns:
            List of category names
        """
        return self.distinct("category")

    def update_prompt(self, title: str, updates: dict) -> dict:
        """
        Update an existing prompt

        Args:
            title: Title of the prompt to update
            updates: Dictionary of fields to update

        Returns:
            Dictionary with update result
        """
        result = self.update_one({"title": title}, updates)
        if result.modified_count > 0:
            return {
                "success": True,
                "message": f"Prompt '{title}' updated successfully",
            }
        elif result.matched_count > 0:
            return {
                "success": True,
                "message": f"Prompt '{title}' exists but no changes were made",
            }
        else:
            return {"success": False, "message": f"Prompt '{title}' not found"}

    def delete_prompt(self, title: str) -> dict:
        """
        Delete a prompt

        Args:
            title: Title of the prompt to delete

        Returns:
            Dictionary with deletion result
        """
        result = self.delete_one({"title": title})
        if result.deleted_count > 0:
            return {
                "success": True,
                "message": f"Prompt '{title}' deleted successfully",
            }
        else:
            return {"success": False, "message": f"Prompt '{title}' not found"}

    def search_prompts(self, search_term: str) -> list:
        """
        Search prompts by text in title, description, or tags

        Args:
            search_term: Term to search for

        Returns:
            List of matching prompt documents
        """
        query = {
            "$or": [
                {"title": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}},
                {"tags": {"$regex": search_term, "$options": "i"}},
            ]
        }
        return self.find(query)

    def bulk_add_prompts(self, prompts: list) -> dict:
        """
        Add multiple prompts at once

        Args:
            prompts: List of prompt dictionaries

        Returns:
            Dictionary with insertion results
        """
        try:
            result = self.insert_many(prompts)
            return {
                "success": True,
                "inserted_count": len(result.inserted_ids),
                "message": f"Successfully added {len(result.inserted_ids)} prompts",
            }
        except Exception as e:
            return {"success": False, "message": f"Error during bulk insert: {str(e)}"}

    # close() is inherited from MongoDBManager
