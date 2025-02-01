import requests
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
API = "API"
URL = "URL"
HEADERS = {
    "Content-Type": "application/json",
    "Apikey": f"Api-key {API}"
}


@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    payload = {"payload": user_message}
    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.ok:
            api_response = response.json()
            clean_text = api_response.get("text", "")
            return jsonify({'response': clean_text})
        else:
            return jsonify({'error': f"API request failed with status {response.status_code}: {response.text}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Request failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
