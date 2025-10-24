import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt


def main():
    print("Hello from ai-agent!")
    
    # load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # create a Gemini client
    client = genai.Client(api_key=api_key)
    
    # generate content using the Gemini model
    if len(sys.argv)<2:
        print("Error, no prompt provided")
        sys.exit(1)
    else:
        # create list of types.Content (user messages)
        user_prompt = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
        # generate response
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
        print(response.text)
        if len(sys.argv)>2 and sys.argv[2] == "--verbose":
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            

if __name__ == "__main__":
    main()


