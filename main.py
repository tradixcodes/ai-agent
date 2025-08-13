import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS

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

    if verbose:
        print(f"\nUser prompt: {prompt}")

    messages = [
        types.Content(
            role="user", 
            parts=[types.Part(text=prompt)]
        )
    ]
    
    #iteration = 1
    #for message in messages:
    #    print(f"This is message {iteration}: {message}")
    #   iteration += 1

    client = genai.Client(api_key=api_key)
    
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximun iterations ({MAX_ITERS}) reached.)")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                    print("Final response:")
                    print(final_response)
                    break
        except Exception as e:
            print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
        
    if verbose:
        usage = response.usage_metadata
        if usage:
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
        else:
            print("Token usage metadata not available")

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts or not
            function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
