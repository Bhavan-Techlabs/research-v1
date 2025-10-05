# 🚀 Quick Start Guide - Research Assistant v2.0

Get up and running in 5 minutes!

## Step 1: Install (2 minutes)

```bash
# Clone or navigate to project
cd /path/to/research-v1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-v2-multi-llm.txt
```

## Step 2: Configure (1 minute)

```bash
# Copy environment template
cp .env.example.v2 .env

# Edit .env and add at least ONE API key:
nano .env  # or use your preferred editor
```

**Minimum Configuration** (choose ONE):
```bash
# Option 1: OpenAI (recommended)
OPENAI_API_KEY=sk-your_key_here

# Option 2: Anthropic
ANTHROPIC_API_KEY=sk-ant-your_key_here

# Option 3: Google Gemini (free tier available)
GOOGLE_API_KEY=your_google_key_here

# Option 4: Groq (generous free tier)
GROQ_API_KEY=gsk_your_key_here
```

## Step 3: Run (30 seconds)

```bash
# Start the application
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

## Step 4: Configure Provider (1 minute)

1. Click **Settings** in the sidebar
2. Go to **LLM Providers** tab
3. Find your provider (e.g., OpenAI)
4. Enter your API key
5. Click **Save**
6. Click **Test Connection**
7. You should see ✅ "Connection successful!"

## Step 5: Start Using! (30 seconds)

### Try Research Assistant
1. Click **Research Assistant** in sidebar
2. Enter: "large language models transformers"
3. Select **ArXiv**
4. Click **Search**
5. View results!

### Try Paper Analyzer
1. Click **Paper Analyzer**
2. Upload a PDF (or download one from ArXiv first)
3. Select **Summary** analysis type
4. Click **Analyze Paper**
5. Get instant analysis!

### Try RAG Chat
1. Click **RAG Chat**
2. Upload a PDF or text file
3. Click **Process Documents**
4. Ask: "What is the main contribution of this paper?"
5. Get intelligent answers!

## Common Issues

### ❌ "Import error: No module named 'streamlit'"
```bash
# Make sure you activated the virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-v2-multi-llm.txt
```

### ❌ "Provider not configured"
```bash
# Go to Settings → LLM Providers
# Add your API key
# Click Save
```

### ❌ "Connection failed: Invalid API key"
```bash
# Double-check your API key in .env
# Make sure there are no extra spaces
# Try regenerating the key from provider's dashboard
```

### ❌ "Rate limit exceeded"
```bash
# Wait a few minutes
# Or switch to a different provider
# Or upgrade your API plan
```

## Provider-Specific Setup

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into .env: `OPENAI_API_KEY=sk-...`
4. Start with `gpt-4o-mini` (cheaper) or `gpt-4o` (better)

### Anthropic
1. Go to https://console.anthropic.com/
2. Get API key
3. Copy to .env: `ANTHROPIC_API_KEY=sk-ant-...`
4. Use `claude-3-5-sonnet-20241022` (recommended)

### Google Gemini
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Copy to .env: `GOOGLE_API_KEY=...`
4. Use `gemini-1.5-flash` (fast & free tier)

### Groq (Free & Fast!)
1. Go to https://console.groq.com/keys
2. Create API key
3. Copy to .env: `GROQ_API_KEY=gsk_...`
4. Use `llama3-70b-8192` (very fast!)

## What to Try First

### 1. Literature Search (3 minutes)
```bash
Research Assistant → Search "your research topic"
→ Select all sources → Export results
```

### 2. Paper Analysis (5 minutes)
```bash
Paper Analyzer → Upload PDF → Try different analysis types:
- Summary
- Key Findings
- Critical Analysis
```

### 3. Ask Questions (5 minutes)
```bash
RAG Chat → Upload paper(s) → Ask:
- "What are the limitations?"
- "How does this compare to [other work]?"
- "Explain the methodology"
```

### 4. Custom Prompts (5 minutes)
```bash
Prompt Manager → Add New → Create your own analysis prompt
→ Use it in Paper Analyzer
```

### 5. Multi-LLM Comparison (10 minutes)
```bash
Configure 2+ providers → Analyze same paper with each
→ Compare results → Find your favorite!
```

## Cost-Saving Tips

1. **Start with free tiers**: Google Gemini, Groq
2. **Use smaller models**: gpt-4o-mini, claude-3-haiku, gemini-flash
3. **Set token limits**: Reduce max_tokens in Settings
4. **Batch process**: Analyze multiple papers at once
5. **Reuse sessions**: Don't re-upload same documents

## Example Workflow

### Conducting a Literature Review

```bash
1. Research Assistant
   → Search your topic across all sources
   → Export to CSV
   
2. Paper Analyzer (Batch)
   → Upload top 10 papers
   → Run "Summary" analysis
   → Review all summaries
   
3. Paper Analyzer (Individual)
   → Deep dive on 3 most relevant
   → Run "Critical Analysis"
   → Save detailed notes
   
4. RAG Chat
   → Upload all papers
   → Ask comparative questions:
     * "What methodologies are most common?"
     * "What are the main research gaps?"
     * "Which papers are most cited?"
   
5. Prompt Manager
   → Create custom "Literature Review" prompt
   → Export for future use
```

## Next Steps

- 📖 Read [README-v2.md](README-v2.md) for full features
- 🏗️ Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- 🔧 See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) to extend
- 🔄 Review [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) if upgrading from v1

## Getting Help

- 📝 Check documentation files in project root
- 🐛 Common issues in MIGRATION_GUIDE.md troubleshooting section
- 💬 Settings → About tab for system information
- 📧 Contact support@research-assistant.io

## Advanced Configuration

### Multiple Providers
```bash
# Configure all providers you have access to
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
GROQ_API_KEY=gsk_...

# Then switch between them in the UI for comparison!
```

### Custom Models
```bash
# In Settings → LLM Providers
# For providers with "custom" models
# Enter your deployment name or model name
# Example for Azure: your-deployment-name
```

### Google Custom Search (Optional)
```bash
# For enhanced web search in Research Assistant
GOOGLE_API_KEY=your_key  # (same as Gemini)
GOOGLE_CSE_ID=your_custom_search_engine_id
```

### MongoDB (Optional)
```bash
# For persistent prompt storage
MONGODB_URI=mongodb://localhost:27017/research_assistant
# Or MongoDB Atlas
```

## Performance Tuning

### For Faster Responses
```bash
# In Settings → Preferences
- Use smaller models (gpt-4o-mini, gemini-flash)
- Lower max_tokens (500-1000 for summaries)
- Reduce chunk_size for RAG (500-750)
- Use Groq (very fast inference)
```

### For Better Quality
```bash
# In Settings → Preferences
- Use larger models (gpt-4o, claude-3-5-sonnet)
- Higher max_tokens (2000-4000)
- Increase chunk_overlap (250-400)
- Temperature: 0.0 for factual, 0.7 for creative
```

## You're Ready! 🎉

Your research assistant is now configured and ready to use!

Start with a simple search or upload a paper to analyze.

**Happy researching! 🔬📚✨**

---

*For detailed documentation, see README-v2.md*
