from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from prompts import GEMINI_PROMPT
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
                systemInstruction=GEMINI_PROMPT,
                responseMimeType = "application/json",
                response_schema = list[Response],
            ),        
    )

    return response


if __name__ == "__main__":
    res = gemini_response("make folder in the current directory named hello")
    res: list[Response] = res.parsed
    print(res)
    cmd = res[0].command
    desc = res[0].description

    print(cmd)
    print(" ")
    print(desc)