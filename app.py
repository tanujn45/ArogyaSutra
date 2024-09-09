from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)
# 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


@app.route('/get_remedies', methods=['POST'])
def get_remedies():
    symptom = request.json.get('symptom')
    prompt = f"""
Given the symptom: {symptom}, provide a list of home remedies
in an HTML-friendly format, with each remedy in a <li> element
within a <ul>. Additionally, provide a brief warning message in
an HTML-friendly format if this symptom might require immediate
medical attention. Use <strong> tags for emphasis where
needed. Format the response as follows:
<ul>
    <li>Remedy 1</li>
    <li>Remedy 2</li>
    <li>Remedy 3</li>
    <!-- Add more remedies as needed -->
</ul>

<p><strong>Warning:</strong> Brief warning message if applicable.</p>
if the warning also has bullets, then use tags where required.
Remember to keep the response for remedies to strictly home remedies.
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return jsonify({'remedies': response.choices[0].message.content})


@app.route('/get_warning', methods=['POST'])
def get_warning():
    symptom = request.json.get('symptom')
    prompt = f"Does {
        symptom} indicate a potentially severe condition that requires immediate medical attention?"
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return jsonify({'warning': response.choices[0].message.content})


if __name__ == '__main__':
    app.run(debug=True)
