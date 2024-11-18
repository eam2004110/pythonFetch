from flask import Flask, request, jsonify
import undetected_chromedriver.v2 as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def fetch_html(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU for better performance
    options.add_argument("--no-sandbox")  # Bypass sandbox for cloud platforms

    # Use the undetected-chromedriver to bypass bot protection
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Get the HTML content after the page has loaded
    html_content = driver.page_source
    driver.quit()
    return html_content

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
