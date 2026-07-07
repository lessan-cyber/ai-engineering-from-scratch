import os
import json
import urllib.request
from google import genai
from google.genai import types
from pathlib import Path 
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

def find_project_root(marker:str=".env")->Path:
    """ Traverses upwards from the current file to find the project root"""
    current = Path(__file__).resolve()
    for parent in current.parents :
        if (parent/marker).exists():
            return parent
    raise FileNotFoundError(f"Could not find root directory containing {marker}")



class Settings(BaseSettings):
    GEMINI_API_KEY:str 
    model_config = SettingsConfigDict (
        env_file_encoding="utf-8",
        env_file=find_project_root()/".env",
        extra="ignore"
    )

settings = Settings()
def call_with_sdk():
    try:
        from google import genai
    except ImportError:
        print("Install the SDK: uv pip install google-genai")
        return

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=types.Part.from_text(text='Why is the sky blue?'),
    config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=20,
    ),
    )
    print(f" SDK response: {response}")
    #print(f"SDK response: {response.content[0].text}")
    #print(f"Tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out")


def call_raw_http():
   
    if not settings.GEMINI_API_KEY:
        print("Set GEMINI_API_KEY environment variable first")
        return

    # La clé d'API est passée en paramètre de requête (query parameter)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json",
    }

    # Structure du payload conforme à l'API de génération de contenu Gemini
    body = json.dumps(
        {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "What is a neural network in one sentence?"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 256,
            },
        }
    ).encode()

    req = urllib.request.Request(
        url, data=body, headers=headers, method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

        # Extraction de la réponse textuelle et des jetons consommés (tokens)
        text_response = result["candidates"][0]["content"]["parts"][0]["text"]
        input_tokens = result["usageMetadata"]["promptTokenCount"]
        output_tokens = result["usageMetadata"]["candidatesTokenCount"]

        print(f"Raw HTTP response: {text_response}")
        print(f"Tokens used: {input_tokens} in, {output_tokens} out")


if __name__ == "__main__":
    print("=== GETTING ENV VARIABLES ===")
    print("=== API Calls ===\n")
    print("1. Using the SDK:")
    # call_with_sdk()
    print("\n2. Using raw HTTP:")
    call_raw_http()


