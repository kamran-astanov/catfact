from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Fetch a random cat fact
@app.route('/catfact', methods=['GET'])
def get_cat_fact():
    response = requests.get('https://catfact.ninja/fact')
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({'error': 'Unable to fetch cat fact'}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
