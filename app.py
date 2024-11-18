from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_html(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.prettify()  # Return the formatted HTML

    except requests.exceptions.RequestException as e:
        return str(e)

@app.route('/fetch', methods=['POST'])
def fetch():
    try:
        data = request.get_json()
        url = data['url']
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        html_content = fetch_html(url)
        return jsonify({'html': html_content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
