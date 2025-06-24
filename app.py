
import os
from flask import Flask, request, render_template, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Setup Gemini client
client = genai.Client(api_key="paste your API KEY HERE")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        model = "gemini-1.5-flash"

        # Parse function and actual prompt
        if ':' in prompt:
            func_type, query = prompt.split(':', 1)
        else:
            func_type, query = 'qa', prompt

        # Prompt design based on function type
        if func_type == 'summary':
            formatted_prompt = f"Summarize the following text:\n{query.strip()}"
        elif func_type == 'creative':
            formatted_prompt = f"Write something creative:\n{query.strip()}"
        elif func_type == 'advice':
            formatted_prompt = f"Give advice on: {query.strip()}"
        else:
            formatted_prompt = query.strip()

        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=formatted_prompt)])
        ]

        config = types.GenerateContentConfig(response_mime_type="text/plain")

        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config
        ):
            response_text += chunk.text

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
