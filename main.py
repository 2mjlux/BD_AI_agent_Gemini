import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.call_function import call_function


def main():
    print("Hello from ai-agent!")
    
    # load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # create a Gemini client
    client = genai.Client(api_key=api_key)
    
    # set up available functions
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    
    # generate content using the Gemini model
    if len(sys.argv)<2:
        print("Error, no prompt provided")
        sys.exit(1)
    else:
        # create list of types.Content (user messages)
        user_prompt = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
        # check if verbose flag is set
        is_verbose = len(sys.argv)>2 and sys.argv[2] == "--verbose"
        # agent to loop up to 20 times
        for iteration in range(20):
            try:
                print(f"\n--- Iteration {iteration+1} ---")
                # generate response with tools (config created inline)
                response = client.models.generate_content(
                    model='gemini-2.0-flash-001',
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions], system_instruction=system_prompt
                    )
                )
                # add AI response to conversation
                for candidate in response.candidates:
                    messages.append(candidate.content)
               
                if response.function_calls:
                    for fc in response.function_calls:
                
                        # call the function and capture the result
                        function_call_result = call_function(fc, verbose=is_verbose)
                
                        # Explore the object
                        print("\n=== EXPLORING OBJECT STRUCTURE ===")
                        print(f"Type: {type(function_call_result)}")
                        print(f"Dir: {[attr for attr in dir(function_call_result) if not attr.startswith('_')]}")
                        print(f"Parts type: {type(function_call_result.parts)}")
                        print(f"Parts[0] type: {type(function_call_result.parts[0])}")
                        print(f"Full object: {function_call_result}")
                        print("=== END EXPLORATION ===\n")
                
                        # check if result has expected structure
                        if not hasattr(function_call_result, 'parts') or len(function_call_result.parts) == 0:
                            raise Exception("Function call does not have parts")
                        if not hasattr (function_call_result.parts[0], 'function_response'):
                            raise Exception("Function call does not have function_response")
                        if not function_call_result.parts[0].function_response.response:
                            raise Exception("Function response is empty")
                    
                        # print the result
                        result_data = function_call_result.parts[0].function_response.response
                        if is_verbose:
                            print(f"-> {result_data}")
                        else:
                            # in non-verbose mode, just print the result directly
                            if 'result' in result_data:
                                print(result_data['result'])
                            elif 'error' in result_data:
                                print(result_data['error'])
                        
                        # add function result to messages (conversation)
                        messages.append(function_call_result)
                        
                # check if AI is done (i.e. gave final text response)
                elif response.text:
                    print(f"\nFinal response:")
                    print(response.text)
                    break # exit loop
            
            except Exception as e:
                print(f"\nError in iteration {iteration+1}: {e}")
                break # exit loop
        else:
            # Loop completed without breaking (hit max iterations)
            print("\nReached maximum iterations (20). Agent may not have completed the task.")
                        
        if is_verbose:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            

if __name__ == "__main__":
    main()


