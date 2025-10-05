"""Seed Embedding Providers to MongoDB"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.embedding_model_manager import EmbeddingModelManager


def get_embedding_providers():
    """Get default embedding provider configurations"""
    return [
        {
            "provider": "openai",
            "name": "OpenAI",
            "api_key_env": "OPENAI_API_KEY",
            "models": [
                {
                    "model_id": "text-embedding-3-large",
                    "name": "Text Embedding 3 Large",
                    "dimensions": 3072,
                    "max_input": 8191,
                    "description": "Most capable OpenAI embedding model",
                },
                {
                    "model_id": "text-embedding-3-small",
                    "name": "Text Embedding 3 Small",
                    "dimensions": 1536,
                    "max_input": 8191,
                    "description": "Efficient OpenAI embedding model",
                },
                {
                    "model_id": "text-embedding-ada-002",
                    "name": "Ada 002",
                    "dimensions": 1536,
                    "max_input": 8191,
                    "description": "Legacy embedding model",
                },
            ],
            "requires_api_key": True,
        },
        {
            "provider": "cohere",
            "name": "Cohere",
            "api_key_env": "COHERE_API_KEY",
            "models": [
                {
                    "model_id": "embed-english-v3.0",
                    "name": "Embed English v3.0",
                    "dimensions": 1024,
                    "max_input": 512,
                    "description": "English-optimized embedding model",
                },
                {
                    "model_id": "embed-english-light-v3.0",
                    "name": "Embed English Light v3.0",
                    "dimensions": 384,
                    "max_input": 512,
                    "description": "Lightweight English embedding",
                },
                {
                    "model_id": "embed-multilingual-v3.0",
                    "name": "Embed Multilingual v3.0",
                    "dimensions": 1024,
                    "max_input": 512,
                    "description": "Multilingual embedding (100+ languages)",
                },
                {
                    "model_id": "embed-multilingual-light-v3.0",
                    "name": "Embed Multilingual Light v3.0",
                    "dimensions": 384,
                    "max_input": 512,
                    "description": "Lightweight multilingual embedding",
                },
            ],
            "requires_api_key": True,
        },
        {
            "provider": "google_vertexai",
            "name": "Google Vertex AI",
            "api_key_env": "GOOGLE_APPLICATION_CREDENTIALS",
            "models": [
                {
                    "model_id": "textembedding-gecko@003",
                    "name": "Text Embedding Gecko",
                    "dimensions": 768,
                    "max_input": 3072,
                    "description": "Google's text embedding model",
                },
                {
                    "model_id": "textembedding-gecko-multilingual@001",
                    "name": "Multilingual Gecko",
                    "dimensions": 768,
                    "max_input": 3072,
                    "description": "Multilingual text embedding",
                },
            ],
            "requires_api_key": False,
            "requires_project": True,
        },
        {
            "provider": "google_genai",
            "name": "Google Gemini",
            "api_key_env": "GOOGLE_API_KEY",
            "models": [
                {
                    "model_id": "text-embedding-004",
                    "name": "Text Embedding 004",
                    "dimensions": 768,
                    "max_input": 2048,
                    "description": "Latest Gemini embedding model",
                },
            ],
            "requires_api_key": True,
        },
        {
            "provider": "bedrock",
            "name": "AWS Bedrock",
            "api_key_env": "AWS_ACCESS_KEY_ID",
            "models": [
                {
                    "model_id": "amazon.titan-embed-text-v1",
                    "name": "Titan Embeddings Text v1",
                    "dimensions": 1536,
                    "max_input": 8192,
                    "description": "Amazon Titan embedding model",
                },
                {
                    "model_id": "amazon.titan-embed-text-v2:0",
                    "name": "Titan Embeddings Text v2",
                    "dimensions": 1024,
                    "max_input": 8192,
                    "description": "Latest Titan embedding with improved performance",
                },
                {
                    "model_id": "cohere.embed-english-v3",
                    "name": "Cohere Embed English v3",
                    "dimensions": 1024,
                    "max_input": 512,
                    "description": "Cohere embedding via Bedrock",
                },
                {
                    "model_id": "cohere.embed-multilingual-v3",
                    "name": "Cohere Embed Multilingual v3",
                    "dimensions": 1024,
                    "max_input": 512,
                    "description": "Cohere multilingual embedding via Bedrock",
                },
            ],
            "requires_api_key": True,
            "extra_env": ["AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        },
        {
            "provider": "azure_openai",
            "name": "Azure OpenAI",
            "api_key_env": "AZURE_OPENAI_API_KEY",
            "models": [
                {
                    "model_id": "text-embedding-3-large",
                    "name": "Text Embedding 3 Large",
                    "dimensions": 3072,
                    "max_input": 8191,
                    "description": "OpenAI embedding on Azure",
                },
                {
                    "model_id": "text-embedding-3-small",
                    "name": "Text Embedding 3 Small",
                    "dimensions": 1536,
                    "max_input": 8191,
                    "description": "Efficient OpenAI embedding on Azure",
                },
                {
                    "model_id": "text-embedding-ada-002",
                    "name": "Ada 002",
                    "dimensions": 1536,
                    "max_input": 8191,
                    "description": "Legacy OpenAI embedding on Azure",
                },
            ],
            "requires_api_key": True,
            "requires_endpoint": True,
        },
        {
            "provider": "mistralai",
            "name": "Mistral AI",
            "api_key_env": "MISTRAL_API_KEY",
            "models": [
                {
                    "model_id": "mistral-embed",
                    "name": "Mistral Embed",
                    "dimensions": 1024,
                    "max_input": 8192,
                    "description": "Mistral AI's embedding model",
                },
            ],
            "requires_api_key": True,
        },
        {
            "provider": "voyageai",
            "name": "Voyage AI",
            "api_key_env": "VOYAGE_API_KEY",
            "models": [
                {
                    "model_id": "voyage-large-2",
                    "name": "Voyage Large 2",
                    "dimensions": 1536,
                    "max_input": 16000,
                    "description": "High-performance embedding model",
                },
                {
                    "model_id": "voyage-code-2",
                    "name": "Voyage Code 2",
                    "dimensions": 1536,
                    "max_input": 16000,
                    "description": "Code-optimized embedding model",
                },
                {
                    "model_id": "voyage-2",
                    "name": "Voyage 2",
                    "dimensions": 1024,
                    "max_input": 4000,
                    "description": "General purpose embedding model",
                },
            ],
            "requires_api_key": True,
        },
        {
            "provider": "huggingface",
            "name": "HuggingFace",
            "api_key_env": "HUGGINGFACEHUB_API_TOKEN",
            "models": [
                {
                    "model_id": "sentence-transformers/all-MiniLM-L6-v2",
                    "name": "All MiniLM L6 v2",
                    "dimensions": 384,
                    "max_input": 256,
                    "description": "Lightweight and fast sentence embedding",
                },
                {
                    "model_id": "sentence-transformers/all-mpnet-base-v2",
                    "name": "All MPNet Base v2",
                    "dimensions": 768,
                    "max_input": 384,
                    "description": "High-quality sentence embedding",
                },
                {
                    "model_id": "BAAI/bge-large-en-v1.5",
                    "name": "BGE Large English v1.5",
                    "dimensions": 1024,
                    "max_input": 512,
                    "description": "State-of-the-art English embedding",
                },
                {
                    "model_id": "BAAI/bge-base-en-v1.5",
                    "name": "BGE Base English v1.5",
                    "dimensions": 768,
                    "max_input": 512,
                    "description": "Efficient English embedding",
                },
                {
                    "model_id": "BAAI/bge-small-en-v1.5",
                    "name": "BGE Small English v1.5",
                    "dimensions": 384,
                    "max_input": 512,
                    "description": "Compact English embedding",
                },
            ],
            "requires_api_key": True,
        },
        {
            "provider": "ollama",
            "name": "Ollama",
            "api_key_env": None,
            "models": [
                {
                    "model_id": "nomic-embed-text",
                    "name": "Nomic Embed Text",
                    "dimensions": 768,
                    "max_input": 8192,
                    "description": "Open embedding model for local deployment",
                },
                {
                    "model_id": "mxbai-embed-large",
                    "name": "MixBread AI Embed Large",
                    "dimensions": 1024,
                    "max_input": 512,
                    "description": "High-quality local embedding",
                },
                {
                    "model_id": "all-minilm",
                    "name": "All MiniLM",
                    "dimensions": 384,
                    "max_input": 256,
                    "description": "Lightweight embedding for Ollama",
                },
            ],
            "requires_api_key": False,
            "requires_base_url": True,
            "default_base_url": "http://localhost:11434",
        },
    ]


def main():
    """Seed embedding providers to MongoDB"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Manage embedding providers in MongoDB"
    )
    parser.add_argument(
        "action",
        choices=["list", "seed", "force-seed"],
        help="Action to perform",
        nargs="?",
        default="seed",
    )
    parser.add_argument(
        "--mongodb-uri",
        help="MongoDB connection URI (defaults to MONGODB_URI env var)",
    )

    args = parser.parse_args()

    try:
        embedding_manager = EmbeddingModelManager(mongodb_uri=args.mongodb_uri)
        providers = get_embedding_providers()

        if args.action == "list":
            print("\n" + "=" * 70)
            print("EMBEDDING PROVIDERS IN MONGODB")
            print("=" * 70)

            existing = embedding_manager.get_all_providers()
            if not existing:
                print("❌ No embedding providers found")
            else:
                for prov in existing:
                    model_count = len(prov.get("models", []))
                    print(f"\n✅ {prov.get('name', 'Unknown')}")
                    print(f"   Provider: {prov.get('provider', 'N/A')}")
                    print(f"   Models: {model_count}")
                print(f"\n{'=' * 70}")
                print(f"Total providers: {len(existing)}")
                print("=" * 70)

        elif args.action in ["seed", "force-seed"]:
            force = args.action == "force-seed"

            if force:
                print("\n⚠️  WARNING: This will update all existing providers!")
                response = input("Continue? (yes/no): ")
                if response.lower() != "yes":
                    print("❌ Cancelled")
                    return

            print(f"\nSeeding {len(providers)} embedding providers...")

            for provider in providers:
                provider_id = provider["provider"]
                result = embedding_manager.add_provider(**provider)

                if result.get("success"):
                    print(f"✓ {provider['name']}")
                else:
                    if force:
                        result = embedding_manager.update_provider(
                            provider_id,
                            {k: v for k, v in provider.items() if k != "provider"},
                        )
                        if result.get("success"):
                            print(f"✓ {provider['name']} (updated)")
                        else:
                            print(f"✗ {provider['name']}: {result.get('message')}")
                    else:
                        print(f"⏭️  {provider['name']} (already exists)")

            print("\nDone!")

        embedding_manager.close()

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
