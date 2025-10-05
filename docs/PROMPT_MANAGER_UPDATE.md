# Prompt Manager - MongoDB Integration Update

## Summary of Changes

The Prompt Manager page has been completely refactored to use MongoDB for persistent storage instead of session state. This provides better data persistence, scalability, and multi-user support.

## What Changed

### 1. Storage Backend
- **Before**: Prompts stored in Streamlit session state (temporary)
- **After**: Prompts stored in MongoDB (persistent)

### 2. New Features
- ✅ Persistent storage across sessions
- ✅ Description field for better prompt documentation
- ✅ Enhanced search using MongoDB regex
- ✅ Automatic database seeding with default prompts
- ✅ Better error handling and user feedback
- ✅ Success/failure status for all operations

### 3. Data Structure
Prompts now include a `description` field:
```python
{
    "title": "Summary",
    "value": "Provide a comprehensive summary...",
    "category": "Analysis",
    "description": "Provide a comprehensive summary of research papers",
    "tags": []  # Used for variables
}
```

## Setup Instructions

### 1. MongoDB Setup

#### Option A: Local MongoDB
```bash
# Install MongoDB (macOS)
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Set environment variable
export MONGODB_URI="mongodb://localhost:27017/"
```

#### Option B: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get connection string
4. Set environment variable:
```bash
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
```

### 2. Environment Configuration

Add to your `.env` file or export in terminal:
```bash
export MONGODB_URI="mongodb://localhost:27017/"
```

Or add to your `.bashrc` / `.zshrc`:
```bash
echo 'export MONGODB_URI="mongodb://localhost:27017/"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Verify Setup

Run the test script:
```bash
cd /Users/bhavanloganathan/Downloads/code/research-v1
python tests/test_prompt_manager.py
```

Expected output:
```
==================================================
Prompt Manager MongoDB Integration Test
==================================================

Testing MongoDB connection...
✅ Successfully connected to MongoDB

==================================================
Testing CRUD Operations
==================================================
...
✅ All tests completed!
```

## Usage

### Starting the Application

```bash
cd /Users/bhavanloganathan/Downloads/code/research-v1
streamlit run streamlit_app.py
```

Navigate to **Prompt Manager** page.

### First Run
- System automatically detects empty database
- Seeds with 15 default prompts
- Shows info message: "Seeding database with default prompts..."

### Managing Prompts

#### Add New Prompt
1. Go to "Add New" tab
2. Fill in:
   - **Name**: Unique prompt name
   - **Category**: Existing or new category
   - **Description**: What the prompt does (optional)
   - **Prompt Text**: The actual prompt template
   - **Variables**: Comma-separated list (e.g., `topic, use_case`)
3. Click "Add Prompt"

#### Edit Prompt
1. Browse prompts in "Browse Prompts" tab
2. Click "Edit" button
3. Modify fields (name cannot be changed)
4. Click "Save Prompt"

#### Delete Prompt
1. Browse prompts in "Browse Prompts" tab
2. Click "Delete" button
3. Prompt removed immediately

#### Search Prompts
- Use search box in sidebar
- Searches title, description, and tags
- Case-insensitive
- Combine with category filter

#### Export/Import
- **Export**: Download all prompts as JSON
- **Import**: Upload JSON file to add prompts

#### Reset to Defaults
- Click "Reset to Defaults" in sidebar
- Confirm by clicking again
- Deletes all custom prompts
- Restores 15 default prompts

## Default Prompts Included

The system includes 15 carefully crafted prompts:

### Analysis Category
1. **Summary** - Comprehensive paper summaries
2. **Key Findings** - Extract main findings
3. **Methodology Review** - Analyze research methods
4. **Critical Analysis** - Strengths and weaknesses
5. **Literature Review** - Literature positioning

### Research Planning
6. **Research Gap Identification** - Find research gaps
7. **Proposal Generation** - Generate research proposals
8. **Grant Proposal** - Draft grant sections

### Technical Category
9. **Dataset Analysis** - Analyze datasets used
10. **Experimental Design** - Evaluate experiments
11. **Results Interpretation** - Interpret findings
12. **Technical Depth** - In-depth technical analysis

### Other Categories
13. **Comparison Study** (Comparative) - Compare papers
14. **Practical Applications** (Application) - Real-world use cases
15. **Ethical Considerations** (Ethics) - Ethical implications

## Troubleshooting

### Issue: "Failed to connect to MongoDB"

**Check MongoDB is running:**
```bash
# macOS
brew services list | grep mongodb

# Start if not running
brew services start mongodb-community
```

**Verify connection string:**
```bash
echo $MONGODB_URI
# Should output: mongodb://localhost:27017/
```

**Test connection:**
```bash
mongosh $MONGODB_URI
# Should connect successfully
```

### Issue: No prompts showing up

**Solution 1: Check database**
```bash
mongosh mongodb://localhost:27017/
use research_assistant
db.prompts.find().count()
```

**Solution 2: Reset to defaults**
- Use "Reset to Defaults" button in UI
- Re-seeds all default prompts

### Issue: Duplicate key error

This happens when importing prompts that already exist.

**Solution:**
- MongoDB prevents duplicates by title
- Delete existing prompt first, or
- Update the existing prompt instead

### Issue: Connection timeout

**For local MongoDB:**
```bash
# Check if MongoDB is actually running
ps aux | grep mongod

# Check MongoDB logs
tail -f /usr/local/var/log/mongodb/mongo.log
```

**For MongoDB Atlas:**
- Check network access settings
- Verify IP whitelist
- Check username/password in connection string

## Files Modified

1. **`pages/04_prompt_manager.py`** - Main UI page (completely refactored)
2. **`docs/PROMPT_MANAGER_MIGRATION.md`** - Detailed migration guide
3. **`tests/test_prompt_manager.py`** - Test script for MongoDB operations

## Files Referenced (Not Modified)

- `src/utils/mongo_utils.py` - MongoDB operations layer
- `src/utils/mongo_manager.py` - Base MongoDB manager
- `old_version/prompt_manager_page.py` - Original implementation reference

## API Reference

### PromptManager Methods

```python
# Get MongoDB manager instance
manager = PromptManager.get_mongo_manager()

# Initialize/seed database
PromptManager.initialize_prompts()

# Get all prompts
prompts = PromptManager.get_all_prompts()
# Returns: Dict[str, Dict]

# Get specific prompt
prompt = PromptManager.get_prompt("Summary")
# Returns: Dict or None

# Add prompt
result = PromptManager.add_prompt(
    name="New Prompt",
    category="Analysis",
    prompt="Prompt text here",
    variables=["var1", "var2"],
    description="What it does"
)
# Returns: {"success": True, "message": "..."}

# Update prompt
result = PromptManager.update_prompt(
    name="Existing Prompt",
    category="New Category",
    prompt="Updated text",
    variables=["var1"],
    description="Updated description"
)
# Returns: {"success": True, "message": "..."}

# Delete prompt
result = PromptManager.delete_prompt("Prompt Name")
# Returns: {"success": True, "message": "..."}

# Search prompts
results = PromptManager.search_prompts("search term")
# Returns: Dict[str, Dict]

# Get categories
categories = PromptManager.get_categories()
# Returns: List[str]

# Export/Import
json_str = PromptManager.export_prompts()
success, message = PromptManager.import_prompts(json_str)

# Reset to defaults
success, message = PromptManager.reset_to_defaults()
```

## Benefits of MongoDB Integration

1. **Persistence** - Data survives app restarts
2. **Scalability** - Handle thousands of prompts efficiently
3. **Multi-user** - Multiple users can share prompts
4. **Search** - Fast full-text search capabilities
5. **Backup** - Easy database-level backups
6. **Migration** - Easy to move data between environments
7. **Audit Trail** - Can add timestamps, versioning (future)

## Next Steps

1. ✅ Test the MongoDB connection
2. ✅ Run the application and verify prompts load
3. ✅ Try adding/editing/deleting prompts
4. ✅ Test search and filter functionality
5. ✅ Export prompts as backup
6. ✅ Verify prompts persist after app restart

## Support

If you encounter issues:

1. **Check MongoDB connection first** - Run test script
2. **Review error messages** - UI shows detailed errors
3. **Check logs** - Terminal shows connection attempts
4. **Verify environment** - Ensure MONGODB_URI is set
5. **Test manually** - Use mongosh to query database

## Future Enhancements

Possible improvements:
- Version control for prompts
- Prompt templates and inheritance
- User-specific prompts
- Prompt sharing and collaboration
- Usage analytics
- Prompt effectiveness tracking
- Import from external sources
- Prompt marketplace

---

**Last Updated**: October 5, 2025
**Migration Status**: ✅ Complete
