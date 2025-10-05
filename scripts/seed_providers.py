"""Seed LLM Providers to MongoDB"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.model_manager import ModelManager


def get_providers():
    """Get default provider configurations"""
    return [
        {
            "provider": "openai",
            "name": "OpenAI",
            "api_key_env": "OPENAI_API_KEY",
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "requires_api_key": True,
        },
        {
            "provider": "anthropic",
            "name": "Anthropic",
            "api_key_env": "ANTHROPIC_API_KEY",
            "models": [
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
            ],
            "requires_api_key": True,
        },
        {
            "provider": "azure_openai",
            "name": "Azure OpenAI",
            "api_key_env": "AZURE_OPENAI_API_KEY",
            "models": ["custom"],
            "requires_api_key": True,
            "requires_endpoint": True,
            "extra_env": ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_VERSION"],
        },
        {
            "provider": "azure_ai",
            "name": "Azure AI",
            "api_key_env": "AZURE_AI_API_KEY",
            "models": ["custom"],
            "requires_api_key": True,
            "requires_endpoint": True,
        },
        {
            "provider": "google_vertexai",
            "name": "Google Vertex AI",
            "api_key_env": "GOOGLE_APPLICATION_CREDENTIALS",
            "models": ["gemini-1.5-pro", "gemini-1.5-flash", "text-bison@002"],
            "requires_api_key": False,
            "requires_project": True,
            "extra_env": ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION"],
        },
        {
            "provider": "google_genai",
            "name": "Google Gemini",
            "api_key_env": "GOOGLE_API_KEY",
            "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
            "requires_api_key": True,
        },
        {
            "provider": "google_anthropic_vertex",
            "name": "Anthropic via Google Vertex AI",
            "api_key_env": "GOOGLE_APPLICATION_CREDENTIALS",
            "models": [
                "claude-3-5-sonnet@20240620",
                "claude-3-opus@20240229",
                "claude-3-haiku@20240307",
            ],
            "requires_api_key": False,
            "requires_project": True,
        },
        {
            "provider": "bedrock",
            "name": "AWS Bedrock",
            "api_key_env": "AWS_ACCESS_KEY_ID",
            "models": [
                "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "anthropic.claude-3-sonnet-20240229-v1:0",
                "meta.llama3-70b-instruct-v1:0",
                "mistral.mistral-large-2402-v1:0",
            ],
            "requires_api_key": True,
            "extra_env": ["AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        },
        {
            "provider": "bedrock_converse",
            "name": "AWS Bedrock Converse",
            "api_key_env": "AWS_ACCESS_KEY_ID",
            "models": [
                "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "anthropic.claude-3-sonnet-20240229-v1:0",
            ],
            "requires_api_key": True,
            "extra_env": ["AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        },
        {
            "provider": "cohere",
            "name": "Cohere",
            "api_key_env": "COHERE_API_KEY",
            "models": ["command-r-plus", "command-r", "command"],
            "requires_api_key": True,
        },
        {
            "provider": "fireworks",
            "name": "Fireworks AI",
            "api_key_env": "FIREWORKS_API_KEY",
            "models": [
                "accounts/fireworks/models/llama-v3p1-70b-instruct",
                "accounts/fireworks/models/mixtral-8x7b-instruct",
            ],
            "requires_api_key": True,
        },
        {
            "provider": "together",
            "name": "Together AI",
            "api_key_env": "TOGETHER_API_KEY",
            "models": [
                "meta-llama/Llama-3-70b-chat-hf",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
            ],
            "requires_api_key": True,
        },
        {
            "provider": "mistralai",
            "name": "Mistral AI",
            "api_key_env": "MISTRAL_API_KEY",
            "models": [
                "mistral-large-latest",
                "mistral-medium-latest",
                "mistral-small-latest",
            ],
            "requires_api_key": True,
        },
        {
            "provider": "huggingface",
            "name": "HuggingFace",
            "api_key_env": "HUGGINGFACEHUB_API_TOKEN",
            "models": [
                "HuggingFaceH4/zephyr-7b-beta",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
            ],
            "requires_api_key": True,
        },
        {
            "provider": "groq",
            "name": "Groq",
            "api_key_env": "GROQ_API_KEY",
            "models": [
                "llama-3.1-70b-versatile",
                "llama3-70b-8192",
                "mixtral-8x7b-32768",
            ],
            "requires_api_key": True,
        },
        {
            "provider": "ollama",
            "name": "Ollama",
            "api_key_env": None,
            "models": ["llama3", "mistral", "codellama", "phi3"],
            "requires_api_key": False,
            "requires_base_url": True,
            "default_base_url": "http://localhost:11434",
        },
        {
            "provider": "deepseek",
            "name": "DeepSeek",
            "api_key_env": "DEEPSEEK_API_KEY",
            "models": ["deepseek-chat", "deepseek-coder"],
            "requires_api_key": True,
        },
        {
            "provider": "ibm",
            "name": "IBM watsonx.ai",
            "api_key_env": "IBM_API_KEY",
            "models": [
                "ibm/granite-13b-chat-v2",
                "meta-llama/llama-3-70b-instruct",
            ],
            "requires_api_key": True,
            "extra_env": ["IBM_CLOUD_URL", "IBM_PROJECT_ID"],
        },
        {
            "provider": "nvidia",
            "name": "NVIDIA AI",
            "api_key_env": "NVIDIA_API_KEY",
            "models": [
                "meta/llama3-70b-instruct",
                "mistralai/mixtral-8x7b-instruct-v0.1",
            ],
            "requires_api_key": True,
        },
        {
            "provider": "xai",
            "name": "xAI (Grok)",
            "api_key_env": "XAI_API_KEY",
            "models": ["grok-beta", "grok-vision-beta"],
            "requires_api_key": True,
        },
        {
            "provider": "perplexity",
            "name": "Perplexity AI",
            "api_key_env": "PERPLEXITY_API_KEY",
            "models": [
                "llama-3.1-sonar-large-128k-online",
                "llama-3.1-sonar-small-128k-online",
            ],
            "requires_api_key": True,
        },
    ]


def main():
    """Seed providers to MongoDB"""
    try:
        model_manager = ModelManager()
        providers = get_providers()

        print(f"Seeding {len(providers)} providers...")

        for provider in providers:
            provider_id = provider["provider"]
            result = model_manager.add_provider(**provider)

            if result.get("success"):
                print(f"✓ {provider['name']}")
            else:
                # Try updating if it already exists
                result = model_manager.update_provider(
                    provider_id, {k: v for k, v in provider.items() if k != "provider"}
                )
                if result.get("success"):
                    print(f"✓ {provider['name']} (updated)")
                else:
                    print(f"✗ {provider['name']}: {result.get('message')}")

        print("\nDone!")
        model_manager.close()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
