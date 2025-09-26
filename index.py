# Example of using the Portkey library to interact with language models
# Official Portkey documentation:
# https://portkey.ai/docs/introduction/what-is-portkey

# Libraries
from mistralai import Mistral  # type: ignore
import json
from portkey_ai import Portkey  # type: ignore
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY_PORTKEY = os.getenv("API_KEY_PORTKEY")
API_KEY_MISTRAL = os.getenv("API_KEY_MISTRAL") # Optional, only if you want to test Mistral directly without Portkey

# Direct test with Mistral AI without Portkey - Common way to use the library
if API_KEY_MISTRAL:
    print("#############################################################")
    print("Asking Mistral directly without Portkey")
    client = Mistral(api_key=API_KEY_MISTRAL)
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "user", "content": "Hello, what can you do? Give it to me in 1 sentence."}
        ]
    )
    print(response.choices[0].message.content)


# Example of using the Portkey library to interact with language models
provider_name_openai = "@test-openai"  # Provider name for OpenAI in Portkey

try:
    print("#############################################################")
    print("Asking OpenAI with Portkey")
    portkey = Portkey(
        api_key=API_KEY_PORTKEY,
        provider=provider_name_openai
    )

    response = portkey.responses.create(
        model="gpt-4.1",
        input="Tell me a three sentence bedtime story about a unicorn."
    )

    print(response)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Failed to connect with OpenAI provider")


# Test with the Mistral AI provider
try:
    print("#############################################################")
    print("Asking Mistral with Portkey")

    provider_name_mistral = "@test-mistral"  # Provider name for Mistral in Portkey

    portkey = Portkey(
        api_key=API_KEY_PORTKEY,
        provider=provider_name_mistral
    )

    chat_complete = portkey.chat.completions.create(
        model="mistral-tiny",  # or mistral-small / mistral-medium
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ]
    )

    print(chat_complete.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Failed to connect with Mistral provider")


# Test with multiple providers using fallback strategy
try:
    print("#############################################################")
    print("Asking multiple providers with Portkey")

    portkey = Portkey(
        api_key=API_KEY_PORTKEY
    )

    # Define fallback strategy
    config = {
        "strategy": {
            "mode": "fallback"
        },
        "targets": [
            {
                "provider": provider_name_openai,
                "override_params": {
                    "model": "gpt-4o"
                }
            },
            {
                "provider": provider_name_mistral,
                "override_params": {
                    "model": "mistral-tiny"
                }
            }
        ]
    }

    # Call with the fallback configuration
    response = portkey.chat.completions.create(
        messages=[{"role": "user", "content": "How many legs does a spider have?"}],
        extra_headers={
            "x-portkey-config": json.dumps(config)
        }
    )

    print(response.choices[0].message["content"])

except Exception as e:
    print(f"An error occurred: {e}")
    print("Failed to connect with providers")
