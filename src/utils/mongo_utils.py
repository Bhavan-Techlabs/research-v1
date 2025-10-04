"""
MongoDB Utility for Prompt Management
Handles storage and retrieval of prompts from MongoDB
"""

from typing import List, Dict, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import os


class PromptManager:
    """
    MongoDB-based prompt management system
    Stores and retrieves research prompts categorized by type
    """

    def __init__(
        self, mongodb_uri: str = None, database_name: str = "research_assistant"
    ):
        """
        Initialize the Prompt Manager

        Args:
            mongodb_uri: MongoDB connection URI
            database_name: Name of the database
        """
        # Get MongoDB URI from parameter or environment variable
        self.mongodb_uri = mongodb_uri or os.getenv("MONGODB_URI")

        if not self.mongodb_uri:
            raise ValueError(
                "MongoDB URI not provided. Set MONGODB_URI environment variable or pass it as parameter."
            )

        self.database_name = database_name
        self.client = None
        self.db = None
        self.prompts_collection = None

        # Connect to MongoDB
        self._connect()

    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.mongodb_uri)
            # Test the connection
            self.client.admin.command("ping")
            self.db = self.client[self.database_name]
            self.prompts_collection = self.db["prompts"]
            print(f"✅ Connected to MongoDB database: {self.database_name}")
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise

    def add_prompt(
        self,
        title: str,
        value: str,
        category: str = "general",
        description: str = "",
        tags: List[str] = None,
    ) -> Dict:
        """
        Add a new prompt to the database

        Args:
            title: Prompt title
            value: Prompt text/template
            category: Category of the prompt
            description: Description of what the prompt does
            tags: List of tags for the prompt

        Returns:
            Dictionary with insertion result
        """
        if tags is None:
            tags = []

        prompt_doc = {
            "title": title,
            "value": value,
            "category": category,
            "description": description,
            "tags": tags,
        }

        try:
            result = self.prompts_collection.insert_one(prompt_doc)
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

    def get_prompt_by_title(self, title: str) -> Optional[Dict]:
        """
        Retrieve a prompt by its title

        Args:
            title: Title of the prompt

        Returns:
            Prompt document or None if not found
        """
        return self.prompts_collection.find_one({"title": title})

    def get_prompts_by_category(self, category: str) -> List[Dict]:
        """
        Retrieve all prompts in a category

        Args:
            category: Category name

        Returns:
            List of prompt documents
        """
        return list(self.prompts_collection.find({"category": category}))

    def get_all_prompts(self) -> List[Dict]:
        """
        Retrieve all prompts

        Returns:
            List of all prompt documents
        """
        return list(self.prompts_collection.find())

    def get_all_categories(self) -> List[str]:
        """
        Get list of all unique categories

        Returns:
            List of category names
        """
        return self.prompts_collection.distinct("category")

    def update_prompt(self, title: str, updates: Dict) -> Dict:
        """
        Update an existing prompt

        Args:
            title: Title of the prompt to update
            updates: Dictionary of fields to update

        Returns:
            Dictionary with update result
        """
        result = self.prompts_collection.update_one({"title": title}, {"$set": updates})

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

    def delete_prompt(self, title: str) -> Dict:
        """
        Delete a prompt

        Args:
            title: Title of the prompt to delete

        Returns:
            Dictionary with deletion result
        """
        result = self.prompts_collection.delete_one({"title": title})

        if result.deleted_count > 0:
            return {
                "success": True,
                "message": f"Prompt '{title}' deleted successfully",
            }
        else:
            return {"success": False, "message": f"Prompt '{title}' not found"}

    def search_prompts(self, search_term: str) -> List[Dict]:
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
        return list(self.prompts_collection.find(query))

    def bulk_add_prompts(self, prompts: List[Dict]) -> Dict:
        """
        Add multiple prompts at once

        Args:
            prompts: List of prompt dictionaries

        Returns:
            Dictionary with insertion results
        """
        try:
            result = self.prompts_collection.insert_many(prompts, ordered=False)
            return {
                "success": True,
                "inserted_count": len(result.inserted_ids),
                "message": f"Successfully added {len(result.inserted_ids)} prompts",
            }
        except Exception as e:
            return {"success": False, "message": f"Error during bulk insert: {str(e)}"}

    def close(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")


def migrate_prompts_from_list(prompts_list: List[Dict], mongodb_uri: str = None):
    """
    Helper function to migrate prompts from a Python list to MongoDB

    Args:
        prompts_list: List of prompt dictionaries from research.py
        mongodb_uri: MongoDB connection URI
    """
    manager = PromptManager(mongodb_uri=mongodb_uri)

    # Transform prompts to match MongoDB schema
    transformed_prompts = []
    for prompt in prompts_list:
        # Determine category from title
        category = "general"
        if "[LONG]" in prompt["title"]:
            category = "evaluation"
        elif "Research" in prompt["title"]:
            category = "research"
        elif "Paper" in prompt["title"]:
            category = "paper_analysis"
        elif any(
            word in prompt["title"]
            for word in ["Text", "Grammar", "Paraphrase", "Formal"]
        ):
            category = "writing"

        transformed_prompts.append(
            {
                "title": prompt["title"].replace("[LONG] ", ""),
                "value": prompt["value"],
                "category": category,
                "description": "",
                "tags": [],
            }
        )

    result = manager.bulk_add_prompts(transformed_prompts)
    print(f"Migration result: {result}")
    manager.close()