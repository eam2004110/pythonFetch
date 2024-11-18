from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fetch', methods=['POST'])
def fetch_data():
    data = request.json
    url = data.get('url')
    options = data.get('options')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Make a request to the provided URL
        response = requests.get(url, headers=options['headers'])

        # Ensure we get a successful response
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch URL", "status": response.status_code}), 500

        return response.text  # Return the raw HTML content as a response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
