# Prompt Manager Migration to MongoDB

## Overview
The Prompt Manager has been updated to use MongoDB for persistent storage instead of hardcoded session state. This ensures prompts are saved across sessions and can be managed centrally.

## Key Changes

### 1. **MongoDB Integration**
- **Before**: Prompts were stored in `st.session_state["prompts"]` dictionary
- **After**: Prompts are stored in MongoDB using `MongoPromptManager` from `src/utils/mongo_utils.py`

### 2. **Data Structure Transformation**
The data structure has been adapted to match MongoDB schema:

**Old Structure (Session State)**:
```python
{
    "Summary": {
        "category": "Analysis",
        "prompt": "Provide a comprehensive summary...",
        "variables": []
    }
}
```

**New Structure (MongoDB)**:
```python
{
    "title": "Summary",
    "value": "Provide a comprehensive summary...",
    "category": "Analysis",
    "description": "Provide a comprehensive summary of research papers",
    "tags": []  # Used for variables
}
```

### 3. **PromptManager Class Updates**

#### New Methods:
- `get_mongo_manager()`: Singleton pattern for MongoDB connection
- `initialize_prompts()`: Seeds database with default prompts if empty
- `search_prompts(search_term)`: Uses MongoDB's text search capabilities
- `reset_to_defaults()`: Resets all prompts to default values

#### Updated Methods:
All CRUD methods now return success/failure status:
```python
{
    "success": True/False,
    "message": "Success/error message"
}
```

### 4. **Default Prompts Enhanced**
- Added `description` field to each default prompt
- Descriptions help users understand prompt purposes
- All 15 default prompts are preserved with improved metadata

### 5. **UI Improvements**
- Added description field in the "Add New Prompt" form
- Description displays in prompt cards for better context
- Error handling for MongoDB connection failures
- Success/error messages for all operations
- MongoDB status info in the footer tips

### 6. **Search Functionality**
- Now uses MongoDB's `search_prompts()` method
- Searches across title, description, and tags
- Case-insensitive regex matching
- Combined with category filtering

## Setup Requirements

### Environment Variables
Set the MongoDB connection string:
```bash
export MONGODB_URI="mongodb://localhost:27017/"
# or
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
```

### MongoDB Setup
1. **Local MongoDB**: Ensure MongoDB is running on your machine
2. **MongoDB Atlas**: Use a cloud-hosted MongoDB cluster
3. **Database Name**: `research_assistant` (default)
4. **Collection Name**: `prompts`

## Migration Path

### For Existing Users
1. **First Run**: The system will automatically seed the database with 15 default prompts
2. **Import Old Prompts**: Use the Import feature to load previously exported prompts
3. **Manual Migration**: If you have custom prompts in session state, export them before the migration

### Seeding Process
On first run with an empty database:
1. System checks if `prompts` collection is empty
2. Automatically inserts all 15 default prompts
3. Displays info message: "Seeding database with default prompts..."

## Feature Comparison

| Feature | Old (Session State) | New (MongoDB) |
|---------|-------------------|---------------|
| Persistence | Session only | Permanent |
| Search | Client-side filtering | MongoDB regex search |
| Concurrent Access | No | Yes |
| Backup | Manual export | Database backups |
| Scalability | Limited | High |
| Description Field | No | Yes |
| Error Handling | Basic | Comprehensive |

## API Changes

### Adding a Prompt
**Before**:
```python
PromptManager.add_prompt(name, category, prompt, variables)
# No return value
```

**After**:
```python
result = PromptManager.add_prompt(name, category, prompt, variables, description)
# Returns: {"success": True, "message": "Prompt 'X' added successfully"}
```

### Deleting a Prompt
**Before**:
```python
PromptManager.delete_prompt(name)
# No return value
```

**After**:
```python
result = PromptManager.delete_prompt(name)
# Returns: {"success": True, "message": "Prompt 'X' deleted successfully"}
```

## Error Handling

### Connection Failures
- Graceful degradation if MongoDB is unavailable
- User-friendly error messages
- Instructions to set up MONGODB_URI

### Operation Failures
- All operations return success/failure status
- Detailed error messages for debugging
- UI displays appropriate success/error notifications

## Testing

### Manual Testing Checklist
- [ ] MongoDB connection successful
- [ ] Default prompts seeded on first run
- [ ] Add new prompt works
- [ ] Edit existing prompt works
- [ ] Delete prompt works
- [ ] Search functionality works
- [ ] Category filtering works
- [ ] Export prompts works
- [ ] Import prompts works
- [ ] Reset to defaults works

### Connection Test
```python
from src.utils.mongo_utils import PromptManager
manager = PromptManager()
prompts = manager.get_all_prompts()
print(f"Found {len(prompts)} prompts")
```

## Troubleshooting

### Issue: "Failed to connect to MongoDB"
**Solution**: 
1. Check if MongoDB is running: `mongod --version`
2. Verify MONGODB_URI environment variable is set
3. Test connection: `mongosh $MONGODB_URI`

### Issue: No prompts showing
**Solution**:
1. Check MongoDB connection
2. Verify collection name: `prompts`
3. Try "Reset to Defaults" to re-seed

### Issue: Duplicate prompts on import
**Solution**:
- MongoDB prevents duplicates by title
- Delete existing prompts before importing
- Or use update operations for existing prompts

## Future Enhancements

1. **Version Control**: Track prompt versions and changes
2. **Sharing**: Share prompts between users/teams
3. **Categories Management**: CRUD operations for categories
4. **Prompt Templates**: Reusable prompt templates
5. **Analytics**: Track prompt usage and effectiveness
6. **Permissions**: Role-based access control for prompts

## Related Files

- `/pages/04_prompt_manager.py` - Main UI implementation
- `/src/utils/mongo_utils.py` - MongoDB operations
- `/src/utils/mongo_manager.py` - Base MongoDB manager
- `/old_version/prompt_manager_page.py` - Original MongoDB implementation

## Rollback Plan

If issues arise, you can temporarily revert:
1. Copy `old_version/prompt_manager_page.py` to `pages/04_prompt_manager.py`
2. Adjust imports and paths as needed
3. Note: This version has less polish but works with MongoDB

## Support

For issues or questions:
1. Check MongoDB connection first
2. Review error messages in Streamlit UI
3. Check terminal logs for detailed errors
4. Refer to MongoDB documentation for connection issues
