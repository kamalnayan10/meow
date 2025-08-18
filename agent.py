from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
from pydantic import ValidationError
import ollama

from prompts import SYSTEM_PROMPT
from model import Response

load_dotenv()

gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def gemini_response(prompt):
    """
    returns response in the form of pydantic model for the user query
    """

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
                systemInstruction=SYSTEM_PROMPT,
                responseMimeType = "application/json",
                response_schema = list[Response],
            ),        
    )

    return response

def ollama_response(prompt):
    """
    returns response in the form of pydantic model for the user query using local LLM
    """
    try:
        response = ollama.generate(
            model="qwen3:4b",
            system=SYSTEM_PROMPT,
            prompt=prompt,
            format="json",
            stream=False
        )

        json_string = response.get('response')
        if not json_string:
            print("Error: AI did not return a response.")
    
        validated_response = Response.model_validate_json(json_string)
        return validated_response

    except ValidationError as e:
        print(f"Error: AI response did not match the required format.\n{e}")
        return None
    except Exception as e:
        print(f"An error occurred while communicating with Ollama: {e}")
        return None



if __name__ == "__main__":
    res = ollama_response("make folder in the current directory named hello")
    print(res)
    cmd = res.command
    desc = res.description
    print(" ")
    print(cmd)
    print(" ")
    print(desc)