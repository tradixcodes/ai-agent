import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

def main():
    # loads environment variables from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    verbose = "--verbose" in sys.argv

    prompt_parts = [arg for arg in sys.argv[1:] if arg != "--verbose"]

    if not prompt_parts:
        print("Usage: python main.py [--verbose] \"Your prompt text here\"")
        sys.exit(1)

    prompt = " ".join(prompt_parts)

    messages = [
        types.Content(
            role="user", 
            parts=[types.Part(text=prompt)]
        )
    ]
    
    iteration = 1
    for message in messages:
        print(f"This is message {iteration}: {message}")
        iteration += 1

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )

    print(response.text)
    
    if verbose:
        print(f"\nUser prompt: {prompt}")
        
        usage = response.usage_metadata
        if usage:
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
        else:
            print("Token usage metadata not available")

if __name__ == "__main__":
    main()
