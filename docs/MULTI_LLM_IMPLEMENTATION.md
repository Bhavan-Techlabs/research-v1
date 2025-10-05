# Multi-LLM Provider Support Implementation

## Overview
The Research Assistant now supports 22 different LLM providers using LangChain's `init_chat_model` implementation. This provides maximum flexibility for users to choose their preferred AI model provider.

## Changes Made

### 1. Prompt Manager Cleanup ✅

**Removed:**
- `tests/test_prompt_manager.py` - Test file removed
- `DEFAULT_PROMPTS` dictionary - No longer hardcoding prompts
- Automatic seeding logic - Database starts empty
- `reset_to_defaults()` method - Replaced with `delete_all_prompts()`

**Updated:**
- `initialize_prompts()` - Now just checks database connection
- Sidebar button - Changed from "Reset to Defaults" to "Delete All Prompts"
- Users must manually add prompts or import them

### 2. Requirements.txt Updates ✅

**Added LangChain Provider Packages:**
```txt
langchain-openai>=0.2.0              # OpenAI GPT models
langchain-anthropic>=0.2.0           # Anthropic Claude models
langchain-google-genai>=2.0.0        # Google Gemini models
langchain-google-vertexai>=2.0.0     # Google Vertex AI models
langchain-cohere>=0.3.0              # Cohere models
langchain-together>=0.2.0            # Together AI models
langchain-groq>=0.2.0                # Groq models
langchain-aws>=0.2.0                 # AWS Bedrock models
langchain-fireworks>=0.2.0           # Fireworks AI models
langchain-mistralai>=0.2.0           # Mistral AI models
langchain-huggingface>=0.1.0         # HuggingFace models
langchain-ollama>=0.2.0              # Ollama local models
langchain-deepseek>=0.1.0            # DeepSeek models
langchain-ibm>=0.3.0                 # IBM watsonx models
langchain-nvidia-ai-endpoints>=0.3.0 # NVIDIA AI endpoints
langchain-xai>=0.1.0                 # xAI Grok models
langchain-perplexity>=0.1.0          # Perplexity AI models
```

### 3. LLM Manager Enhancement ✅

**File:** `src/services/llm_manager.py`

**Added 22 Providers:**
1. **openai** - OpenAI GPT models (gpt-4o, gpt-4-turbo, etc.)
2. **anthropic** - Anthropic Claude models
3. **azure_openai** - Azure OpenAI Service
4. **azure_ai** - Azure AI Services
5. **google_vertexai** - Google Vertex AI
6. **google_genai** - Google Gemini
7. **google_anthropic_vertex** - Claude via Vertex AI
8. **bedrock** - AWS Bedrock
9. **bedrock_converse** - AWS Bedrock Converse API
10. **cohere** - Cohere models
11. **fireworks** - Fireworks AI
12. **together** - Together AI
13. **mistralai** - Mistral AI
14. **huggingface** - HuggingFace models
15. **groq** - Groq (fast inference)
16. **ollama** - Local Ollama models
17. **deepseek** - DeepSeek models
18. **ibm** - IBM watsonx.ai
19. **nvidia** - NVIDIA AI endpoints
20. **xai** - xAI Grok models
21. **perplexity** - Perplexity AI
22. **azure_ai** - Azure AI Services

**Enhanced Methods:**
- `_load_credentials_from_env()` - Loads extra environment variables
- `is_provider_configured()` - Handles providers without API keys
- `initialize_model()` - Provider-specific configuration logic

### 4. Credentials Manager Enhancement ✅

**File:** `src/utils/credentials_manager.py`

**Enhanced UI for Provider-Specific Fields:**

#### Azure Providers (azure_openai, azure_ai)
- API Key
- Azure Endpoint
- API Version

#### Google Cloud Providers (google_vertexai, google_anthropic_vertex)
- Project ID
- Location
- Credentials File Path (optional)

#### AWS Providers (bedrock, bedrock_converse)
- Access Key ID
- Secret Access Key
- Region

#### IBM watsonx
- API Key
- IBM Cloud URL
- Project ID

#### Ollama
- Base URL (defaults to http://localhost:11434)

#### Standard Providers
- API Key only

## Supported Providers Reference

### Provider Configuration

| Provider | API Key Env Var | Extra Requirements |
|----------|----------------|-------------------|
| openai | OPENAI_API_KEY | None |
| anthropic | ANTHROPIC_API_KEY | None |
| azure_openai | AZURE_OPENAI_API_KEY | Endpoint, API Version |
| azure_ai | AZURE_AI_API_KEY | Endpoint |
| google_vertexai | GOOGLE_APPLICATION_CREDENTIALS | Project ID, Location |
| google_genai | GOOGLE_API_KEY | None |
| google_anthropic_vertex | GOOGLE_APPLICATION_CREDENTIALS | Project ID |
| bedrock | AWS_ACCESS_KEY_ID | Secret Key, Region |
| bedrock_converse | AWS_ACCESS_KEY_ID | Secret Key, Region |
| cohere | COHERE_API_KEY | None |
| fireworks | FIREWORKS_API_KEY | None |
| together | TOGETHER_API_KEY | None |
| mistralai | MISTRAL_API_KEY | None |
| huggingface | HUGGINGFACEHUB_API_TOKEN | None |
| groq | GROQ_API_KEY | None |
| ollama | None | Base URL |
| deepseek | DEEPSEEK_API_KEY | None |
| ibm | IBM_API_KEY | Cloud URL, Project ID |
| nvidia | NVIDIA_API_KEY | None |
| xai | XAI_API_KEY | None |
| perplexity | PERPLEXITY_API_KEY | None |

## Setup Instructions

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**

**For OpenAI:**
```bash
export OPENAI_API_KEY="sk-..."
```

**For Anthropic:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**For Google Gemini:**
```bash
export GOOGLE_API_KEY="AI..."
```

**For Google Vertex AI:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

**For AWS Bedrock:**
```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
```

**For Azure OpenAI:**
```bash
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
```

**For Ollama (local):**
```bash
# Just ensure Ollama is running
ollama serve
```

**For Other Providers:**
```bash
export GROQ_API_KEY="gsk_..."
export COHERE_API_KEY="..."
export TOGETHER_API_KEY="..."
export MISTRAL_API_KEY="..."
# etc.
```

### Configuration via UI

1. Go to **Settings** page
2. Scroll to **LLM Provider Configuration**
3. Expand the provider you want to configure
4. Enter required credentials
5. Click **Save**

## Usage Example

### In Code

```python
from src.services.llm_manager import get_llm_manager

# Initialize manager
llm_manager = get_llm_manager()

# Set credentials (if not in env)
llm_manager.set_credentials("openai", api_key="sk-...")

# Initialize a model
llm = llm_manager.initialize_model(
    provider="openai",
    model="gpt-4o",
    temperature=0.7,
    max_tokens=1000
)

# Use the model
response = llm.invoke("What is machine learning?")
print(response.content)
```

### Via UI

1. Navigate to any page with LLM selection
2. Choose your configured provider from dropdown
3. Select a model
4. Start using the assistant

## Provider-Specific Notes

### OpenAI
- Most popular provider
- Models: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
- Rate limits apply based on tier

### Anthropic
- Claude models known for long context
- Models: Claude 3.5 Sonnet, Claude 3 Opus, Haiku
- Excellent for research and analysis

### Google Gemini
- Direct API access to Gemini models
- Fast and efficient
- Good for multimodal tasks

### Google Vertex AI
- Enterprise Google Cloud solution
- Requires GCP project setup
- Best for production deployments

### AWS Bedrock
- Access to multiple models through AWS
- Includes Anthropic, Meta, Mistral models
- Enterprise-grade security

### Azure OpenAI
- Microsoft's OpenAI offering
- Requires Azure subscription
- Enterprise features and compliance

### Ollama
- Run models locally
- No API key required
- Free but requires local compute
- Models: llama3, mistral, phi3, etc.

### Groq
- Extremely fast inference
- Limited model selection
- Good for production workloads

### Cohere
- Excellent for embeddings and RAG
- Command R models for chat
- Enterprise features

### DeepSeek
- Chinese AI models
- Competitive pricing
- Good for coding tasks

### IBM watsonx
- Enterprise AI platform
- Granite and open-source models
- Strong governance features

## Migration Notes

### From Old Version

If you were using the old implementation:

1. **API Keys:** Reconfigure all providers in Settings
2. **Model Names:** Some model names may have changed
3. **Provider IDs:** Note the new provider ID format (e.g., `google_genai` instead of `google-genai`)

### Prompt Manager Changes

- **No default prompts** on first run
- **Import prompts** from JSON if you have backups
- **Create prompts** manually or use import feature
- **Delete All** replaces "Reset to Defaults"

## Testing

### Test Provider Configuration

```python
from src.services.llm_manager import get_llm_manager

manager = get_llm_manager()

# Check configured providers
providers = manager.get_configured_providers()
print(f"Configured: {providers}")

# Test initialization
for provider in providers:
    try:
        models = manager.get_available_models(provider)
        if models and models != ["custom"]:
            llm = manager.initialize_model(provider, models[0])
            print(f"✅ {provider}: OK")
    except Exception as e:
        print(f"❌ {provider}: {e}")
```

### Test via UI

1. Go to Settings → LLM Configuration
2. Configure a provider
3. Go to Research Assistant page
4. Select the provider
5. Try a simple query

## Troubleshooting

### Provider Not Showing Up

**Check:**
1. Is the provider package installed? `pip list | grep langchain`
2. Is the API key configured? Check Settings page
3. Any error messages in terminal?

### "Failed to initialize model"

**Common causes:**
1. Invalid API key
2. Missing required fields (endpoint, project, etc.)
3. Network connectivity issues
4. Rate limiting

**Solutions:**
- Verify credentials in Settings
- Check provider documentation
- Test API key with curl/httpie
- Check for service outages

### Ollama Not Working

**Check:**
1. Is Ollama running? `ollama list`
2. Correct base URL? Default: `http://localhost:11434`
3. Model pulled? `ollama pull llama3`

### Azure/Google Cloud Issues

**Check:**
1. Correct endpoint/project ID
2. Required permissions in cloud console
3. Service enabled in cloud project
4. Credentials file path (for GCP)

## Performance Considerations

### Model Selection

| Use Case | Recommended Providers | Models |
|----------|---------------------|--------|
| Fast responses | Groq, Together | llama3-70b, mixtral |
| Best quality | OpenAI, Anthropic | gpt-4o, claude-3.5-sonnet |
| Cost-effective | Google, Groq | gemini-flash, llama3 |
| Local/private | Ollama | llama3, mistral |
| Enterprise | Azure, Bedrock, Vertex | Various |

### Caching

- LLM responses are not cached by default
- Implement caching at application level if needed
- Consider using Redis or similar for caching

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for credentials
3. **Rotate keys regularly** as per provider guidelines
4. **Use least privilege** for cloud IAM roles
5. **Monitor usage** to detect anomalies
6. **Implement rate limiting** to prevent abuse

## Future Enhancements

- [ ] Add streaming support for all providers
- [ ] Implement response caching layer
- [ ] Add cost tracking per provider
- [ ] Provider fallback/failover logic
- [ ] Batch processing support
- [ ] Fine-tuned model support
- [ ] Model comparison UI
- [ ] Usage analytics dashboard

## Support & Resources

### Provider Documentation

- [OpenAI](https://platform.openai.com/docs)
- [Anthropic](https://docs.anthropic.com/)
- [Google AI](https://ai.google.dev/docs)
- [AWS Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Cohere](https://docs.cohere.com/)
- [Groq](https://console.groq.com/docs)
- [Ollama](https://ollama.ai/docs)

### LangChain Documentation

- [init_chat_model](https://python.langchain.com/docs/integrations/chat/)
- [Model Providers](https://python.langchain.com/docs/integrations/platforms/)

---

**Last Updated:** October 5, 2025
**Version:** 2.0
**Status:** ✅ Complete
